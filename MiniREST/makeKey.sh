#!/bin/bash

prefix=$1

echo "GENERATING CA CERT"
#Generate CA key:
openssl genrsa -des3 -out $prefix.ca.key 4096
openssl req -new -x509 -days 3650 -key $prefix.ca.key -out $prefix.ca.crt

echo "GENERATING SERVER CERT"
# Generate private key
openssl genrsa -des3 -out $prefix.key 4096
# Create certificate signing request
openssl req -new -key $prefix.key -out $prefix.csr

echo "SIGNING SERVER CERT"
# Sign with key and certificate
openssl x509 -req -days 3650 -in $prefix.csr -CA $prefix.ca.crt -CAkey $prefix.ca.key -set_serial 01 -out $prefix.crt

echo "REMOVING SERVER CERT PASSWORD"
# Take password off key
openssl rsa -in $prefix.key -out $prefix.key.insecure
# Swap keys
mv $prefix.key $prefix.key.secure
mv $prefix.key.insecure $prefix.key
