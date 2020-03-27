import bcrypt

class Encrypt:
    def encrypt_password(password:str):
        byte_password = str.encode(password) #converte string para bytes
        hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt(10))

        return hashed

    def validate_user_password(self,normal_password:str,encrypted_password:str):
        return True if bcrypt.checkpw(str.encode(normal_password),str.encode(encrypted_password)) else False





