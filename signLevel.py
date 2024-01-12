# external imports
import json
import hashlib

def signData(data):
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return signature

def checkSignature(data, signature):
    return signature == signData(data)

level = input("Level file: ")

with open (level, 'r') as file:
    saved_data = json.load(file)
    loaded_data = saved_data['data']
    saved_signature = saved_data['signature']
    if not checkSignature(loaded_data, saved_signature):
        print("Level file corrupted, resigning...")
        newSig = signData(loaded_data)
        with open(level, 'w') as file:
            json.dump({"data": loaded_data, "signature": newSig}, file)
    else:
        print("Level file is valid")