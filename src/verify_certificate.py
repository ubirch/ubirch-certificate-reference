import base64
import hashlib
import logging
import os
import sys

import msgpack

from compress import decompress_and_decode
from ubirch_verify import verify

CERT_PREFIX = "C01:"
CERT_TYPE = 0xEE

UPP_TYPE_IDX = -3
UPP_PAYLOAD_IDX = -2

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(format='%(asctime)s %(name)20.20s %(levelname)-8.8s %(message)s', level=LOGLEVEL)
logger = logging.getLogger()

env = os.getenv("UBIRCH_ENV", "prod")
verification_token = os.getenv('UBIRCH_VERIFICATION_TOKEN')

usage = "usage:\n" \
        " python3 verify_certificate.py <ubirch certificate>"

if len(sys.argv) != 2:
    print(usage)
    sys.exit(1)

certificate = sys.argv[1]


def verify_certificate(cert: str) -> bool:
    logger.info("certificate:                   {}".format(cert))

    # assert certificate has the expected prefix
    if not cert.startswith(CERT_PREFIX):
        raise ValueError("certificate does not have expected prefix {}".format(CERT_PREFIX))

    # remove the prefix, then decode and decompress the certificate to get the
    # msgpack-encoded Ubirch Protocol Package (UPP)
    cert_msgpack = decompress_and_decode(cert.removeprefix(CERT_PREFIX))
    logger.debug("UPP with original data:        {}".format(cert_msgpack.hex()))

    # decode the msgpack-encoded UPP, the decoded UPP is an array with 5 elements
    # [version, uuid, type, certificate payload data, signature]
    unpacked_upp = msgpack.unpackb(cert_msgpack)

    # assert UPP has the expected type hint
    if unpacked_upp[UPP_TYPE_IDX] != CERT_TYPE:
        raise ValueError("invalid type hint {:02X}, must be {:02X}".format(unpacked_upp[UPP_TYPE_IDX], CERT_TYPE))

    # extract the msgpack-encoded certificate payload from the payload field
    payload_msgpack = unpacked_upp[UPP_PAYLOAD_IDX]
    logger.info("certificate payload [msgpack]: {}".format(payload_msgpack.hex()))

    # create sha256 hash of the msgpack-encoded certificate payload
    payload_hash = hashlib.sha256(payload_msgpack).digest()

    # get the base64 string representation of the payload hash
    payload_hash_base64 = base64.b64encode(payload_hash).decode()
    logger.info("payload hash [base64]:         {}".format(payload_hash_base64))

    # request if hash is known by the ubirch trust service
    if not verify(payload_hash_base64, env, verification_token):
        logger.error("certificate payload data hash could not be verified by the ubirch trust service")
        return False

    logger.info("certificate verification successful")

    # display the verified original certificate payload
    payload_json = msgpack.unpackb(payload_msgpack)
    logger.info("certificate payload [JSON]:    {}".format(payload_json))

    return True


if not verify_certificate(certificate):
    sys.exit(1)
