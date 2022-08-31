import base64
import hashlib
import logging
import os
import sys

import msgpack

from compress import decompress_and_decode
from ubirch_verify import verify

CERT_HINT = 0xEE
CERT_PREFIX = "C01:"

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(format='%(asctime)s %(name)20.20s %(levelname)-8.8s %(message)s', level=LOGLEVEL)
logger = logging.getLogger()

env = os.getenv("UBIRCH_ENV", "prod")

usage = "usage:\n" \
        " python3 verify_certificate.py <ubirch certificate>"

if len(sys.argv) != 2:
    print(usage)
    sys.exit(1)

certificate = sys.argv[1]


def verify_certificate(cert: str) -> bool:
    logger.info("certificate:                   {}".format(cert))

    if not cert.startswith(CERT_PREFIX):
        raise ValueError("certificate does not have expected prefix {}".format(CERT_PREFIX))

    cert_msgpack = decompress_and_decode(cert.removeprefix(CERT_PREFIX))
    logger.debug("UPP with original data:        {}".format(cert_msgpack.hex()))

    unpacked_upp = msgpack.unpackb(cert_msgpack)

    if unpacked_upp[-3] != CERT_HINT:
        raise ValueError("invalid payload type {:02X}, must be {:02X}".format(unpacked_upp[-3], CERT_HINT))

    payload_msgpack = unpacked_upp[-2]
    logger.info("certificate payload [msgpack]: {}".format(payload_msgpack.hex()))

    # create sha256 hash of msgpack payload
    payload_hash = hashlib.sha256(payload_msgpack).digest()

    # get the base64 string representation of the payload hash
    payload_hash_base64 = base64.b64encode(payload_hash).decode()
    logger.info("payload hash [base64]:         {}".format(payload_hash_base64))

    # request if hash is known by the ubirch trust service
    if not verify(payload_hash_base64, env):
        logger.error("certificate payload data hash could not be verified by the ubirch trust service")
        return False

    logger.info("certificate verification successful")

    # display verified original data
    payload_json = msgpack.unpackb(payload_msgpack)
    logger.info("certificate payload [JSON]:    {}".format(payload_json))

    return True


if not verify_certificate(certificate):
    sys.exit(1)
