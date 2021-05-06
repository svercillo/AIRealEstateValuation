import os
from binascii import hexlify

key = hexlify(os.urandom(40))
f = open(os.path.dirname(__file__) + '.env', "a+")
f.write(f"API_KEY={key.decode()}")
f.close()
    