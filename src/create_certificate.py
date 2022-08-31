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

CERT_HINT = 0xEE
CERT_PREFIX = "C01:"

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(format='%(asctime)s %(name)20.20s %(levelname)-8.8s %(message)s', level=LOGLEVEL)
logger = logging.getLogger()

env = os.getenv("UBIRCH_ENV", "prod")
client_cert_filename = os.getenv("UBIRCH_CLIENT_CERT_PFX_FILE")
client_cert_pwd_file = os.getenv("UBIRCH_CLIENT_CERT_PWD_FILE")
identity_id = UUID(hex=os.getenv('UBIRCH_IDENTITY_UUID'))

with open(client_cert_pwd_file, 'r') as f:
    client_cert_password = f.read()

usage = "usage:\n" \
        " python3 create_certificate.py <JSON data map>"

if len(sys.argv) != 2:
    print(usage)
    sys.exit(1)

certificate_payload_data = sys.argv[1]


def create_certificate(payload_json: str) -> str:
    logger.debug("input: {}".format(payload_json))

    # parse JSON payload
    payload_dict = json.loads(payload_json)

    # assert valid input: JSON map
    if not isinstance(payload_dict, dict):
        raise TypeError(f"Invalid input: not a JSON map (dict), is {type(payload_dict)}")

    logger.info("certificate payload [JSON]:    {}".format(payload_dict))

    # convert JSON payload to msgpack
    payload_msgpack = msgpack.packb(payload_dict)
    logger.info("certificate payload [msgpack]: {}".format(payload_msgpack.hex()))

    # create sha256 hash of msgpack payload
    payload_hash = hashlib.sha256(payload_msgpack).digest()

    # get the base64 string representation of the payload hash
    payload_hash_base64 = base64.b64encode(payload_hash).decode()
    logger.info("payload hash [base64]:         {}".format(payload_hash_base64))

    # send payload hash to the ubirch trust service to create a signed ubirch protocol package (UPP)
    upp = certify(payload_hash_base64, identity_id, env, client_cert_filename, client_cert_password)
    logger.debug("UPP with hash:                 {}".format(upp.hex()))

    # unpack UPP (msgpack)
    unpacked_upp = msgpack.unpackb(upp)
    # replace hashed payload with original data (msgpack)
    unpacked_upp[-2] = payload_msgpack
    # set payload type hint accordingly
    unpacked_upp[-3] = CERT_HINT

    # convert UPP with original data payload to msgpack
    cert_msgpack = msgpack.packb(unpacked_upp)
    logger.debug("UPP with original data:        {}".format(cert_msgpack.hex()))

    # zlib-compress, base45-encode and prepend prefix for certificate
    cert = CERT_PREFIX + compress_and_encode(cert_msgpack).decode()
    logger.info("certificate:                   {}".format(cert))

    return cert


create_certificate(certificate_payload_data)
