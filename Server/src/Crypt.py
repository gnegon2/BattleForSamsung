from Crypto.Cipher import DES
 
class Crypt():
    @staticmethod
    def RebaseKey(key):
        fill = "ABCDEFGH"
        if len(key) < 8:
            key += fill[0: 8 - len(key)]
        return key
    
    @staticmethod
    def RebaseText(text):
        fill = "        "
        if len(text) < 8:
            text += fill[0: 8 - len(text)]
        return text
        
    @staticmethod
    def Encrypt(text, key):
        key = Crypt.RebaseKey(key)
        text = Crypt.RebaseText(text)
        des = DES.new(key, DES.MODE_ECB)
        cipher_text = des.encrypt(text)
        return cipher_text

    @staticmethod
    def Decrypt(cipher_text, key):
        key = Crypt.RebaseKey(key)
        cipher_text = Crypt.RebaseText(cipher_text)
        des = DES.new(key, DES.MODE_ECB)
        text = des.decrypt(cipher_text)
        text = text.strip()
        return text


