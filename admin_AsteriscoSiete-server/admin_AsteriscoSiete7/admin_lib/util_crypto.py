# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from django.conf import settings


class CryptoAes(object):
    """
    """

    def __init__(self, key=None):
        """
        Construcctor que recibe como parametro predeterminado el key se setting,
        para con el instanciar el objeto usado para encriptar y desencriptar la
        variable de session.
        """
        super(CryptoAes, self).__init__()

        if key is None:
            key = settings.SECRET_KEY[:32]

        """
        En caso de que el key tenga una longitud menor a la establecida,
        se añadiran tantos '*' como sea necesario para completarla
        """
        key_len = len(key)
        if key_len < 32:  # 32 tamaño por defecto
            key = key + ('*' * (32 - key_len))

        if isinstance(key, str):
            key = key.encode('utf-8')

        # pycryptodome requiere mode explícito; usamos ECB para compatibilidad
        self._key = key
        self.encryption = AES.new(key, AES.MODE_ECB)

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
        # pycryptodome: se necesita una nueva instancia por operación en ECB
        cipher = AES.new(self._key, AES.MODE_ECB)
        return cipher.encrypt(self.ConvertMultiple16(texto).encode('utf-8'))

    def Decrypt(self, ciph):
        """
        Desencripta un hash recibido por parametro y devuelve el string correspondiente
        """
        cipher = AES.new(self._key, AES.MODE_ECB)
        return cipher.decrypt(ciph).decode('utf-8')
