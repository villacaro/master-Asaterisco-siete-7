# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from django.conf import settings


class CryptoAes(object):
    """
    """

    def __init__(self, key=settings.SECRET_KEY[:32]):
        """
        Construcctor que recibe como parametro predeterminado el key se setting,
        para con el instanciar el objeto usado para encriptar y desencriptar la
        variable de session.
        """
        super(CryptoAes, self).__init__()

        """
        En caso de que el key tenga una longitud menor a la establecida,
        se añadiran tantos '*' como sea necesario para completarla
        """
        key_len = len(key)
        if key_len < 32:  # 32 tamaño por defecto
            key = key + ('*' * (32 - key_len))

        # Creamos el
        self.encryption = AES.new(key)

    def ConvertMultiple16(self, texto):
        mismatch = len(texto) % 16
        if mismatch != 0:
            padding = (16 - mismatch) * ' '
            texto += padding
        return texto

    def Encrypt(self, texto):
        """
        Encripta el texto recibido, primero verifica que sea de multiplo 16,
        de no serlo le agrega un pading y procede a ejecutar el algoritmo
        AES de encriptacion.

        Retorna un texto encriptado
        """
        return self.encryption.encrypt(self.ConvertMultiple16(texto).encode('utf-8'))

    def Decrypt(self, ciph):
        """
        Desencripta un has recibifo por parametro y devuelve el string correspondiente
        """
        return self.encryption.decrypt(ciph).decode('utf-8')
