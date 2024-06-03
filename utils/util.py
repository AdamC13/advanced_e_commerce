from datetime import datetime, timedelta, timezone
import jwt
import os

# Create a secret key constant variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': customer_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # Get the current time
        now = datetime.now(timezone.utc).timestamp()
        if payload.get('exp') < now:
            print('Token has expired')
            return None
        # Return the customer_id
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        print('Token has expired')
        return None
    except jwt.InvalidTokenError:
        print('Invalid token')
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None