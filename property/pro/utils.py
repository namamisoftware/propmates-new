from django.core.cache import cache
import random
from .models import regesteruser
# from twilio.rest import Client


# Twilio credentials (add these to your environment variables for security)
TWILIO_ACCOUNT_SID = "SKa67f01f64096b1053fa3eb3ecb69e123"
TWILIO_AUTH_TOKEN = "kCdxKjpKg4jPC5TaOzSsJAVe8K7KEhz5"
TWILIO_PHONE_NUMBER = "(229) 471-5171"  # Your Twilio number

def generate_otp(phone):
    """
    Generate a 6-digit OTP, store in cache, and send via Twilio SMS
    """
    otp = str(random.randint(100000, 999999))
    cache.set(f"otp_{phone}", otp, timeout=900)  # 15 minutes
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP code is: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        print(f"Sent OTP to {phone}: {otp}")  # Debug only
    except Exception as e:
        print(f"Error sending OTP to {phone}: {e}")
    
    return otp

def verify_otp(phone, otp):
    """
    Verify the OTP entered by the user
    """
    saved_otp = cache.get(f"otp_{phone}")
    if saved_otp and saved_otp == otp:
        cache.delete(f"otp_{phone}")
        return True
    return False

def get_logged_in_user(request):
    """
    Retrieve session-based logged-in user
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return regesteruser.objects.get(id=user_id)
    except regesteruser.DoesNotExist:
        return None
