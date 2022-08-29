import requests as r


def verify(data_hash_base64: str, stage: str) -> bool:
    url = f"https://verify.{stage}.ubirch.com"

    res = r.post(f"{url}/api/upp/verify", data=data_hash_base64,
                 headers={"content-type": "text/plain"})
    return res.status_code == 200
