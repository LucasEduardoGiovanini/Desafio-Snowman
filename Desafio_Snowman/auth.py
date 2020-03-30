import bcrypt,jwt,datetime


class Encrypt:
    def encrypt_password(password:str):
        byte_password = str.encode(password) #converte string para bytes
        hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt(10))

        return hashed

    def validate_user_password(self,normal_password:str,encrypted_password:str):
        return True if bcrypt.checkpw(str.encode(normal_password),str.encode(encrypted_password)) else False

class Token:
    def create_json_web_token(self,encrypt_password:str):
        token = jwt.encode({'password': encrypt_password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},'johnnyboy')
        return (token.decode('UTF-8'))

    def decode_json_web_token(self,token:str,secret_key:str):
        print(jwt.decode(token,secret_key))
        return jwt.decode(token,secret_key)




