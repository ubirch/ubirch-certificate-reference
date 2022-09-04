import logging

import requests as r

logger = logging.getLogger()


def verify(data_hash_base64: str, stage: str, bearer_token: str) -> bool:
    """
    Request if a base64-encoded data hash can be verified by the UBIRCH verification service
     and return weather or not the verification was successful.

    :param data_hash_base64: the base64-encoded data hash string representation
    :param stage: the UBIRCH backend environment
    :param bearer_token: Bearer access token for the UBIRCH verification service
    :return: True for verification success, False otherwise.
    """
    url = f"https://verify.{stage}.ubirch.com/api/v2/upp/verify"

    res = r.post(url,
                 data=data_hash_base64,
                 headers={"content-type": "text/plain",
                          "Authorization": f"Bearer {bearer_token}"})

    if res.status_code != 200:
        logger.debug("verification at {} failed: {} {}".format(url, res.status_code, res.text))
        return False

    return True
