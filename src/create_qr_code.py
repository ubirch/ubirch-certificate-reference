import os
import sys

import pyqrcode
import logging

LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(format='%(asctime)s %(name)20.20s %(levelname)-8.8s %(message)s', level=LOGLEVEL)
logger = logging.getLogger()

qrcode_file_name = "qrcode.png"

usage = "usage:\n" \
        "  python3 create_qr_code.py base45-encoded cert [qrcode-file-name]"

if len(sys.argv) < 2:
    print(usage)
    sys.exit(1)

if len(sys.argv) > 2:
    qrcode_file_name = sys.argv[2]

cert = sys.argv[1]


def create_qrcode(qr_content_data, image_file_name):
    # create QR code from the data 
    qrcode = pyqrcode.create(f"{qr_content_data}", error='Q', mode='alphanumeric')
    qrcode.png(image_file_name, scale=4, quiet_zone=0)
    logger.info(f"wrote {image_file_name}")


create_qrcode(cert, qrcode_file_name)
