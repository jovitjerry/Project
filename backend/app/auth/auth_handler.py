import time
from typing import Dict, Optional
from jose import jwt, JWTError
from ..config.config import settings

def token_response(access_token: str, refresh_token: str = None):
    response = {
        "access_token": access_token
    }
    if refresh_token:
        response["refresh_token"] = refresh_token
    return response

def signJWT(user_id: str, role: str) -> Dict[str, str]:
    # Access Token
    access_payload = {
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": time.time() + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Refresh Token (valid for 7 days)
    refresh_payload = {
        "user_id": user_id,
        "role": role,
        "type": "refresh",
        "exp": time.time() + (7 * 24 * 60 * 60)
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return token_response(access_token, refresh_token)

def decodeJWT(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except JWTError:
        return None

def verify_refresh_token(token: str) -> Optional[dict]:
    payload = decodeJWT(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None
