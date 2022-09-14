import boto3
import base64
from cryptography.fernet import Fernet

def handler(event, context):
    
    # My incredibly secret PII data!!
    message = "this is a top secret message!"

    # Generate a new datakey from a given alias.
    keyData = generateDataKey("alias/my-encryption-key")
    storableKey = keyData['b64encKey'].decode()
    
    # Encrypt the string and store it (as a string)!
    encMessage = encryptString(message, keyData['b64textKey'])
    storableMessage = encMessage.decode()
    
    # Insert to the database
    print("Ensure encypted byte strings are encoded as strings for DB...")
    print("Run this insert...")
    print(""" ... INSERT INTO myschema.mytable (id, piData, key) 
            VALUES (NULL, '%s', '%s'""" % (storableMessage, storableKey) )


    print("Fetch the encrypted data from database...")
    print (""" ... SELECT id, piData, key FROM myschema.mytable""")
    print("Convert the database strings into Python byte strings...")
    messageInDb = storableMessage.encode()
    keyInDb = storableKey.encode()
    
    decOldMessage = decryptString(messageInDb, keyInDb)
    print("Old message with saved key: ", decOldMessage)

    return True
    
def generateDataKey(keyId, keySpec="AES_256"):
    """ Call the KMS service to geneate a new datakey """
    
    kms_client = boto3.client("kms")
    response = kms_client.generate_data_key(KeyId=keyId, KeySpec=keySpec)
    
    # Get both the plaintext and encrypted versions of the key (base64 encoded).
    return {
            "b64encKey" : base64.b64encode(response["CiphertextBlob"]),
            "b64textKey" : base64.b64encode(response["Plaintext"])
        }

def encryptString(dataToEncrypt, encodedKey):
    """ Encrypt the string with a base64 encoded key """
    
    # Set up the encryption object and encrypte the data!
    fernet = Fernet(encodedKey)
    return base64.b64encode(fernet.encrypt(dataToEncrypt.encode()))
    
def decryptString(dataToDecrypt, encryptedKey):
    """ Decrypt the string with a encrypted, base64 encoded key """
    
    kms_client = boto3.client("kms")
    
    response = kms_client.decrypt(CiphertextBlob=base64.b64decode(encryptedKey))
    keyForDecrypt = base64.b64encode(response["Plaintext"])
    
    fernetDecrypter = Fernet(keyForDecrypt)

    # Try to decode and decrypt the message!
    encString = base64.b64decode(dataToDecrypt)
    return fernetDecrypter.decrypt(encString).decode()
 