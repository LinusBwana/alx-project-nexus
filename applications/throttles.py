from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled

class CustomUserThrottle(UserRateThrottle):
    rate = "5/minute" # Override the global
    
    def throttle_failure(self):
        # Custom error message
        message = "Too many attempts. Please wait before trying again."
        # Raise custom message
        raise Throttled(detail=message)