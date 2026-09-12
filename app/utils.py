from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_pwd , hashed_pwd):
    return pwd_context.verify(plain_pwd,hashed_pwd)