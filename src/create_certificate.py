import base64
import hashlib
import json
import logging
import os
import sys
from uuid import UUID

import msgpack

from compress import compress_and_encode
from ubirch_certify import certify

CERT_TYPE = 0xEE

UPP_PAYLOAD_IDX = -2
UPP_TYPE_IDX = -3

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(format='%(asctime)s %(name)20.20s %(levelname)-8.8s %(message)s', level=LOGLEVEL, stream=sys.stderr)
logger = logging.getLogger()

env = os.getenv("UBIRCH_ENV", "prod")
client_cert_filename = os.getenv("UBIRCH_CLIENT_CERT_PFX_FILE")
client_cert_pwd_file = os.getenv("UBIRCH_CLIENT_CERT_PWD_FILE")
identity_id = UUID(hex=os.getenv('UBIRCH_IDENTITY_UUID'))

with open(client_cert_pwd_file, 'r') as f:
    client_cert_password = f.read()

usage = "usage:\n" \
        "  python3 create_certificate.py json-file [certificate-prefix]"

cert_prefix = "C01:"

if len(sys.argv) < 2:
    print(usage)
    sys.exit(1)

if len(sys.argv) > 2:
    cert_prefix = sys.argv[2]

with open(sys.argv[1], "r") as f:
    certificate_payload_data = f.read()


def create_certificate(payload_json: str, cert_prefix: str) -> str:
    logger.debug("input: {}".format(payload_json))

    # parse JSON certificate payload
    payload_dict = json.loads(payload_json)

    # assert valid input: JSON map
    if not isinstance(payload_dict, dict):
        raise TypeError(f"Invalid input: not a JSON map (dict), is {type(payload_dict)}")

    logger.info("certificate payload [JSON]:    {}".format(payload_dict))

    # msgpack-encode JSON certificate payload
    payload_msgpack = msgpack.packb(payload_dict)
    logger.info("certificate payload [msgpack]: {}".format(payload_msgpack.hex()))

    # create sha256 hash of msgpack-encoded certificate payload
    payload_hash = hashlib.sha256(payload_msgpack).digest()

    # get the base64 string representation of the payload hash
    payload_hash_base64 = base64.b64encode(payload_hash).decode()
    logger.info("payload hash [base64]:         {}".format(payload_hash_base64))

    # send payload hash to the ubirch trust service to create a signed Ubirch Protocol Package (UPP)
    upp = certify(payload_hash_base64, identity_id, env, client_cert_filename, client_cert_password)
    logger.debug("UPP with hash:                 {}".format(upp.hex()))

    # decode the msgpack-encoded UPP, the decoded UPP is an array with 5 elements
    # [version, uuid, type, certificate payload hash, signature]
    unpacked_upp = msgpack.unpackb(upp)

    # insert the msgpack-encoded certificate payload into the payload field and set type hint accordingly
    unpacked_upp[UPP_PAYLOAD_IDX] = payload_msgpack
    unpacked_upp[UPP_TYPE_IDX] = CERT_TYPE

    # msgpack-encode UPP with original certificate payload
    cert_msgpack = msgpack.packb(unpacked_upp)
    logger.debug("UPP with original data:        {}".format(cert_msgpack.hex()))

    # zlib-compress, base45-encode and prepend prefix for certificate
    cert = cert_prefix + compress_and_encode(cert_msgpack).decode()
    logger.info("certificate:                   {}".format(cert))

    return cert


cert = create_certificate(certificate_payload_data, cert_prefix)
print(cert)
