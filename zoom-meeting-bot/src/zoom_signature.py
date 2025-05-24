import os
import time
import base64
import hashlib
import hmac
import json
from dotenv import load_dotenv

load_dotenv()

def generate_signature(meeting_number: str, role: int = 0) -> str:
    """
    :param meeting_number: ID конференції (string або number as string)
    :param role: 0 — учасник, 1 — хост
    :return: JWT-signature
    """
    sdk_key    = os.getenv("ZOOM_SDK_KEY")
    sdk_secret = os.getenv("ZOOM_SDK_SECRET")
    iat = int(time.time()) - 30
    exp = iat + 2 * 60 * 60

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sdkKey": sdk_key,
        "mn": str(meeting_number),
        "role": role,
        "iat": iat,
        "exp": exp,
        "appKey": sdk_key,
        "tokenExp": exp
    }

    header_enc  = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_enc = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    to_sign     = f"{header_enc}.{payload_enc}"

    signature    = hmac.new(sdk_secret.encode(), to_sign.encode(), hashlib.sha256).digest()
    signature_enc = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{to_sign}.{signature_enc}"
