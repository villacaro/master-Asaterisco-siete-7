import binascii

import rsa
from ws_sportparley.settings import KEY_RSA_LEN


def byteToHex(varBytes):
    if hasattr(varBytes, 'hex'):
        return varBytes.hex()
    else:
        return binascii.hexlify(varBytes).decode('utf8')


class CryptoRSA(object):

    @staticmethod
    def newkeys():
        return rsa.newkeys(KEY_RSA_LEN)

    @staticmethod
    def verify(message_recv, signatureHex, pub_key_pkcs1):
        signature = bytearray.fromhex(signatureHex)
        pub_key = rsa.PublicKey.load_pkcs1((pub_key_pkcs1).encode())
        try:
            rsa.verify(message_recv.encode(), signature, pub_key)
            return True
        except rsa.pkcs1.VerificationError:
            return False

    @staticmethod
    def sign(body, priv_key_pkcs1):
        return byteToHex(
            rsa.sign(
                body.encode(),
                rsa.PrivateKey.load_pkcs1(priv_key_pkcs1.encode()),
                'SHA-1'
            )
        )

    @staticmethod
    def encrypt(text, pub_key_pkcs1):
        return byteToHex(
            rsa.encrypt(
                text,
                rsa.PublicKey.load_pkcs1(pub_key_pkcs1.encode())
            )
        )

    @staticmethod
    def decrypt(text, priv_key_pkcs1):
        return rsa.decrypt(
            bytearray.fromhex(text),
            rsa.PrivateKey.load_pkcs1(priv_key_pkcs1.encode())
        ).decode('utf8')
