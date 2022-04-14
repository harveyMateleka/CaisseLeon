import base64, re
from Crypto.Cipher import AES
from Crypto import Random


import codecs

# make utf8mb4 recognizable.
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


class AESCipher:

    def __init__(self, key, blk_sz):
        self.key = key
        self.blk_sz = blk_sz

    def encrypt( self, raw ):
        # raw is the main value
        if raw is None or len(raw) == 0:
            raise NameError("No value given to encrypt")
        raw = raw + '\0' * (self.blk_sz - len(raw) % self.blk_sz)
        raw = raw.encode('utf8mb4')
        # Initialization vector to avoid same encrypt for same strings.
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key.encode('utf8mb4'), AES.MODE_CFB, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ).decode('utf8mb4')

    def decrypt( self, enc ):
        # enc is the encrypted value
        if enc is None or len(enc) == 0:
            raise NameError("No value given to decrypt")
        enc = base64.b64decode(enc)
        iv = enc[:16]
        # AES.MODE_CFB that allows bigger length or latin values
        cipher = AES.new(self.key.encode('utf8mb4'), AES.MODE_CFB, iv )
        return re.sub(b'\x00*$', b'', cipher.decrypt( enc[16:])).decode('utf8mb4')