# kms-envelope-demo
Quick demo to test out KMS envelope encryption for database.

## My Demo Environment
- AWS Lambda (Python 3.8)
- AWS KMS Customer key
- Lambda role that has access to the CMK to decrypt/encrypt/generateDataKey

## What This Demo Does

**NOTE:** This demo is just meant to show some very basic code highlighting the 
envelope encryption method.  It is in no way meant to be run in production 
(hard-coded values, no error checking, etc), but just to give ideas on how it works.

This demo shows how to generate a data key, use that key to encrypt some data, encode
that data to make it safe to store in a MySQL text column, and then how to decrypt that
data with the encrypted key.

## Some References
- (https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html)
- (https://docs.aws.amazon.com/wellarchitected/latest/financial-services-industry-lens/use-envelope-encryption-with-customer-master-keys.html)
- (https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping)
