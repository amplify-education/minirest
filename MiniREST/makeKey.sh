#!/bin/bash

prefix=$1
# Generate private key
openssl genrsa -des3 -out $prefix.key 4096
# Create certificate signing request
openssl req -new -key $prefix.key -out $prefix.csr
# Sign with key and certificate
openssl x509 -req -days 365 -in $prefix.csr -signkey $prefix.key -out $prefix.crt
# Take password off key
openssl rsa -in $prefix.key -out $prefix.key.insecure
# Swap keys
mv $prefix.key $prefix.key.secure
mv $prefix.key.insecure $prefix.key
