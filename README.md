# UBIRCH Certificate Reference

A reference implementation for creating and verifying UBIRCH certificates in python.

## Setup

```commandline
python3 -m venv venv3
. venv3/bin/activate
pip install -r requirements.txt
```

## UBIRCH Certificate Creation

1. [Install dependencies](#setup)
2. Set the required [environment variables](#environment-variables-for-certificate-creation)
3. Run the [`create_certificate.py` script](src/create_certificate.py) passing the certificate payload data (JSON)
   as command line argument, see [example](#certification-example-call)

### Environment Variables for Certificate Creation

| Variable                    | Description                                                                            |
|-----------------------------|----------------------------------------------------------------------------------------|
| UBIRCH_CLIENT_CERT_PFX_FILE | client certificate file [*.pfx]                                                        |
| UBIRCH_CLIENT_CERT_PWD_FILE | file containing the client certificate password                                        |
| UBIRCH_IDENTITY_UUID        | UUID of the target identity                                                            |
| UBIRCH_ENV                  | _optional_: the UBIRCH backend environment ("dev" / "demo" / "prod"), default = "prod" |
| LOGLEVEL                    | _optional_: logging level ("DEBUG" / "INFO" / "WARNING" / "ERROR"), default = "INFO"   |

### Certification Example Call

> Certificate payload data has to be unique. Before running the example call, the input file has to be modified in order
> to create a unique hash. Otherwise, the script will exit with an error "This data has already been anchored before"

```commandline
UBIRCH_ENV=dev \
UBIRCH_CLIENT_CERT_PFX_FILE=<client certificate filename>.pfx \
UBIRCH_CLIENT_CERT_PWD_FILE=<client certificate password filename>.txt \
UBIRCH_IDENTITY_UUID=<target identity ID> \
python3 src/create_certificate.py "$(<example-payload/example.json)"
```

The resulting certificate will look like this:

```text
C01:6BFLUJ.VF374$6Q1W54L50NJ- 2FT1H1K-ACW92R0I6U7ST9%QR7XIJHDX4H8WV*LAY/UL0IA6J++UJ5QB0O-.VZ*LRJCFI921ERMS.UHTYIQYQ$FB/NSW:PI/0O.KGHG5.TMIN5F61CWV$UI45%K96QKZWICY05$0EN98E5%JAJ4LKCTE:I6KPB$P4*B%ZJD.JEFNTFKS*MXWO534IQDUIA-B9$JD+HESE6%OC*J2SBU 6TS9CYWP8LAAO9MF2A44$9MLICD*J:TU/YU3E2AHAMPKFB40+9J.K2E93Y80%I9KQZACOW6UILUGJQUTFE13RVYC52R9 H1%J6 TQ6RG731KLGUU5KYPZPGVT4.S0XAB52K.8B6LJ-B2W+GM28LQ6FQT MSVFM:PN:/VU IEQK+N2PS4S-7G Q7HNCS2 L6+E6 JG8LHG U2QEFRHVW2FPKSK3SSBQBV1US$17-24 1VKTGXZQFPD5JDAMTZD7OBQD%LOXDC065YRL*DJHFTACAKP 4FM H-M7% V/QAI4WZ71.UHHKSLIOBWK8WNUPH1*VTVBOTEK.P4QHO:2HB0B1DL5C
```

## UBIRCH Certificate Verification

1. [Install dependencies](#setup)
2. _(optional)_ Set the [environment variables](#environment-variables-for-certificate-verification)
3. Run the [`verify_certificate.py` script](src/verify_certificate.py) passing the certificate
   as command line argument, see [example](#verification-example-call)

### Environment Variables for Certificate Verification

| Variable                    | Description                                                                            |
|-----------------------------|----------------------------------------------------------------------------------------|
| UBIRCH_ENV                  | _optional_: the UBIRCH backend environment ("dev" / "demo" / "prod"), default = "prod" |
| LOGLEVEL                    | _optional_: logging level ("DEBUG" / "INFO" / "WARNING" / "ERROR"), default = "INFO"   |

### Verification Example Call

```commandline
UBIRCH_ENV=dev \
python3 src/verify_certificate.py 'C01:6BFLUJ.VF374$6Q1W54L50NJ- 2FT1H1K-ACW92R0I6U7ST9%QR7XIJHDX4H8WV*LAY/UL0IA6J++UJ5QB0O-.VZ*LRJCFI921ERMS.UHTYIQYQ$FB/NSW:PI/0O.KGHG5.TMIN5F61CWV$UI45%K96QKZWICY05$0EN98E5%JAJ4LKCTE:I6KPB$P4*B%ZJD.JEFNTFKS*MXWO534IQDUIA-B9$JD+HESE6%OC*J2SBU 6TS9CYWP8LAAO9MF2A44$9MLICD*J:TU/YU3E2AHAMPKFB40+9J.K2E93Y80%I9KQZACOW6UILUGJQUTFE13RVYC52R9 H1%J6 TQ6RG731KLGUU5KYPZPGVT4.S0XAB52K.8B6LJ-B2W+GM28LQ6FQT MSVFM:PN:/VU IEQK+N2PS4S-7G Q7HNCS2 L6+E6 JG8LHG U2QEFRHVW2FPKSK3SSBQBV1US$17-24 1VKTGXZQFPD5JDAMTZD7OBQD%LOXDC065YRL*DJHFTACAKP 4FM H-M7% V/QAI4WZ71.UHHKSLIOBWK8WNUPH1*VTVBOTEK.P4QHO:2HB0B1DL5C'
```

> Due to processing time in the UBIRCH backend, it is possible for the verification of a certificate to fail shortly
> after its creation.
