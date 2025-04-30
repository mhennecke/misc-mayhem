# Create self-signed certificate

To be used as client certificate for OPC UA communication. The OPC UA server on edge controllers requires "Sign" and "CRL: Sign" key extensions in the certificate. It seems that the OPC UA server expects an issuing CA certificate.
 
```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out cert.crt -config openssl.cnf -extensions v3_req
```

