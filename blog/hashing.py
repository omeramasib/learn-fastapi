from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bycrypt(password: str):
        return pwd_cxt.hash(password)