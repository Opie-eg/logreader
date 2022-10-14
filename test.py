import base64
import json

def encrypt_password(message):
    
    encMessage =  base64.b64encode(message.encode("utf-8"))
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
        data["password"] = encMessage.decode("utf-8")

    with open("config.json", "w") as jsonFile:
        json.dump(data, jsonFile, indent= 4)

def decrypt_password():
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    decMessage = base64.b64decode(data["password"]).decode()
    
    return decMessage

x= encrypt_password("110LL#)))")
#print(x)~


y= decrypt_password()
print(y)




