from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config import DEFAULT_REQUEST_LIMIT

# Applying limit to request by ip
ipLimiter = Limiter(key_func=get_remote_address, default_limits=[DEFAULT_REQUEST_LIMIT])
