# pip install pycryptodome
#注意本地的’crypto‘文件明名应为’Crypto‘
from binascii import a2b_hex

from Crypto.Cipher import AES


class EncryptDecode:

 # 解密后，去掉补足的空格用strip() 去掉
 def decrypt(self, text):
     key = '1234567891234567'.encode('utf-8')
     iv = b'1234567891234567'
     mode = AES.MODE_CBC
     cryptos = AES.new(key, mode, iv)
     plain_text = cryptos.decrypt(a2b_hex(text))
     return bytes.decode(plain_text).rstrip('\0')

if __name__ == '__main__':
     e = 'a50ddfb1ec4155c28b912b49ab593537' # 加密
     d = EncryptDecode().decrypt(e) # 解密
     print("密文:", e)
     print("明文:", d)
     print(type(d))