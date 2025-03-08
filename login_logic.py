import pyotp
import qrcode
from PyQt5.QtGui import QPixmap
from io import BytesIO

def get_key(name, password):
    key = pyotp.random_base32()
    url = pyotp.totp.TOTP(key).provisioning_uri(name=name, issuer_name=password)  # Generate QR URI

    qr = qrcode.make(url)

    # Converting QR Code to a QPixmap
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.getvalue())  
    return key, pixmap  

def verify(key,otp):
    totp = pyotp.TOTP(key)
    return totp.verify(otp)

#print(verify("QWWKDAJICG7XCVGLHHLZPWHUGEZE5Q5K", 634920))
