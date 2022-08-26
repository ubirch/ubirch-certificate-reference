# UBIRCH Certificate Reference

A reference implementation for creating and verifying UBIRCH certificates in python.

## How to create a UBIRCH certificate

1. [Install dependencies](#setup)
2. Set the required [environment variables](#environment-variables)
3. Run the [`certify.py` script](src/certify.py) with a JSON file as command line argument, see [example](#example)

### Setup

```commandline
python3 -m venv venv3
. venv3/bin/activate
pip install -r requirements.txt
```

### Environment Variables

| Variable                    | Description                                                                            |
|-----------------------------|----------------------------------------------------------------------------------------|
| UBIRCH_CLIENT_CERT_PFX_FILE | client certificate file [*.pfx]                                                        |
| UBIRCH_CLIENT_CERT_PWD_FILE | file containing the client certificate password                                        |
| UBIRCH_IDENTITY_UUID        | UUID of the target identity                                                            |
| UBIRCH_ENV                  | _optional_: the UBIRCH backend environment ("dev" / "demo" / "prod"), default = "prod" |

### Example

> Certificate payload data has to be unique. Before running the example call, the input file has to be modified in order
> to create a unique hash. Otherwise, the script will exit with an error "This data has already been anchored before"

```commandline
UBIRCH_ENV=dev \
UBIRCH_CLIENT_CERT_PFX_FILE=<client certificate filename>.pfx \
UBIRCH_CLIENT_CERT_PWD_FILE=<client certificate password filename>.txt \
UBIRCH_IDENTITY_UUID=<target identity ID> \
python3 src/certify.py example-payload/example.json
```
