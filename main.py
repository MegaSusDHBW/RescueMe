import json

from crypt import generateKeypair, encryptData, decryptData

#Test
data = '{"name": "Hans", "alter": 50}'
data = json.dumps(data).encode('utf-8')


fernet = generateKeypair()
encryptedJSON = encryptData(data, fernet)
print(encryptedJSON)

decryptedJSON = decryptData(encryptedJSON, fernet)
data = json.loads(decryptedJSON)
print(data)
#

#whats3word