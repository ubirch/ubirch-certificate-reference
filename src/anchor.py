import base64
from uuid import UUID

import requests_pkcs12 as r


def anchor(data_hash: str, identity_id: UUID, stage: str, client_cert_filename: str,
           client_cert_password: str) -> bytes:
    if stage == "prod":
        url = "https://api.certify.ubirch.com"
    else:
        url = f"https://api.certify.{stage}.ubirch.com"

    res = r.post(f"{url}/api/v1/x509/anchor", data=data_hash,
                 headers={"X-Identity-Id": str(identity_id), "Content-Type": "text/plain"},
                 pkcs12_filename=client_cert_filename,
                 pkcs12_password=client_cert_password)
    if not res.status_code == 200:
        if res.status_code == 409:
            raise Exception("This data has already been anchored before: {} {}"
                            .format(res.status_code, res.json()))
        else:
            raise Exception("An error occurred communicating with the ubirch trust service: {} {}"
                            .format(res.status_code, res.json()))

    return base64.b64decode(res.json()["data"]["body"]["upp"])