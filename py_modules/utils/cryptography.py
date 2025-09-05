from base64 import b64encode, b64decode


class Cryptography:
    """Class for access cryptography methods"""

    @staticmethod
    def initialize():
        pass

    @staticmethod
    def encrypt_string(plaintext: str) -> bytes:
        """Encrypt string"""
        b64_bytes = b64encode(plaintext.encode("utf-8"))
        b64_str = b64_bytes.decode("utf-8")
        return b64_str

    @staticmethod
    def decrypt_string(encrypted_text) -> str:
        """Decrypt string"""
        texto_bytes = b64decode(encrypted_text.encode("utf-8"))
        texto_original = texto_bytes.decode("utf-8")
        return texto_original
