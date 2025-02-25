import pyotp
import qrcode

key = pyotp.random_base32()
url = pyotp.totp.TOTP(key).provisioning_uri(name="amaxhex56", issuer_name="test")

qrcode.make(url).save("qrcode.png")

totp = pyotp.TOTP(key)

def verify(opt):
    return totp.verify(opt)

if verify(input("Enter OTP: ")):
    print("OTP Verified")
else:
    print("OTP Verification Failed")