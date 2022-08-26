import base45
import zlib


def compress_and_encode(binary_str):
    return base45.b45encode(zlib.compress(binary_str))


def decompress_and_decode(certificate_str):
    return zlib.decompress(base45.b45decode(certificate_str))
