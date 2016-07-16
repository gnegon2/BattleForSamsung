from Crypto.Cipher import DES
 
def RebaseKey(key):
    fill = "ABCDEFGH"
    if len(key) < 8:
        key += fill[0: 8 - len(key)]
    return key

def RebaseText(text):
    fill = "        "
    if len(text) < 8:
        text += fill[0: 8 - len(text)]
    return text
    
def Encrypt(text, key):
    key = RebaseKey(key)
    text = RebaseText(text)
    des = DES.new(key, DES.MODE_ECB)
    cipher_text = des.encrypt(text)
    return cipher_text

def Decrypt(cipher_text, key):
    key = RebaseKey(key)
    cipher_text = RebaseText(cipher_text)
    des = DES.new(key, DES.MODE_ECB)
    text = des.decrypt(cipher_text)
    text = text.strip()
    return text