#used only for signing levels manually for testing purposes, not needed for the game

# external imports
import json # for reading and writing json files
import hashlib # for hashing the data

def signData(data): # signs some data
    signature = hashlib.sha256(json.dumps(data).encode()).hexdigest() # hash the data to a signature 
    return signature # return the signature

def checkSignature(data, signature): # checks if the signature is valid
    return signature == signData(data) # return if the signature passed in is equal to the data's hash

level = input("Level file: ") # get the level file to sign

with open (level, 'r') as file: # open the level file for reading
    saved_data = json.load(file) # load the data from the file
    loaded_data = saved_data['data'] # get the data from the file
    saved_signature = saved_data['signature'] # get the signature from the file
    if not checkSignature(loaded_data, saved_signature): # check if the signature is valid
        print("Level file corrupted, resigning...") # if not, resign the file
        newSig = signData(loaded_data) # get the new signature
        with open(level, 'w') as file: # open the file for writing
            json.dump({"data": loaded_data, "signature": newSig}, file) # write the new signature to the file
    else: # if the signature is valid
        print("Level file is valid") # print that the file is valid