This directory contains examples that demonstrate how to start TLS servers.

To run these examples, SSL certificate and private key files need to be
created. When running under CPython, the files should be in PEM format, named
`cert.pem` and `key.pem`. When running under MicroPython, they should be in DER
format, and named `cert.der` and `key.der`.

To quickly create a self-signed SSL certificate, use the following command:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

To convert the resulting PEM files to DER format for MicroPython, use these
commands:

```bash
openssl x509 -in cert.pem -out cert.der -outform DER
openssl rsa -in key.pem -out key.der -outform DER
```
