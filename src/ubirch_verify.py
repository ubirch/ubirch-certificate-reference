import requests as r


def verify(data_hash_base64: str, stage: str, bearer_token: str) -> bool:
    url = f"https://verify.{stage}.ubirch.com"

    res = r.post(f"{url}/api/v2/upp/verify", data=data_hash_base64,
                 headers={"content-type": "text/plain",
                          "Authorization": f"Bearer {bearer_token}"})
    return res.status_code == 200
