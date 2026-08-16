import pyotp
import smtplib
from email.mime.text import MIMEText

def generate_otp(secret: str) -> str:
    """
    Generate a time-based OTP using the provided secret.

    Args:
        secret: Base32 secret key

    Returns:
        6-digit OTP string
    """
    # TODO: use pyotp.TOTP to generate current OTP
    pass

def send_otp_email(to_email: str, otp: str) -> None:
    """
    Send the OTP to the data subject via local SMTP (localhost:1025).

    Args:
        to_email: Recipient email address
        otp: The OTP code to send
    """
    # TODO: build MIMEText message with OTP
    # TODO: connect to smtplib.SMTP("localhost", 1025)
    # TODO: send message and close connection
    pass

def verify_otp(secret: str, user_input: str) -> bool:
    """
    Verify the OTP entered by the user against the secret.
    """
    # TODO: use pyotp.TOTP(secret).verify(user_input)
    pass

if __name__ == "__main__":
    secret = pyotp.random_base32()
    otp = generate_otp(secret)
    send_otp_email("subject@example.com", otp)
    print(f"OTP sent. Secret (for testing): {secret}")
