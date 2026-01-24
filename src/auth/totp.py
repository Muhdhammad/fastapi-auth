import io
import pyotp
from pyotp import TOTP
import qrcode

class TwoFactorAuth():

    @staticmethod
    def generate_secret_key() -> str:
        return pyotp.random_base32()
    
    @staticmethod
    def verify_totp_code(totp_code: str, secret: str) -> bool:
        totp = TOTP(secret)
        return totp.verify(totp_code, valid_window=1) # allow timedrift +- 30s
    
    @staticmethod
    def generate_qr_code(username: str, secret: str, issuer_name="Hammad 2FA") -> bytes:

        totp = pyotp.TOTP(secret)
        # generate uri for qrcode
        uri = totp.provisioning_uri(
            name=username,
            issuer_name=issuer_name
        )
        
        qr_code = qrcode.make(uri) #img
        img_byte_arr = io.BytesIO()
        qr_code.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return img_byte_arr.getvalue()