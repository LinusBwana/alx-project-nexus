from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled

class LoginAnonThrottle(AnonRateThrottle):
    rate = "5/minute" # Override the global

    def throttle_failure(self):
        # Custom error message
        message = "Too many login attempts. Please wait before trying again."
        # Raise custom message
        raise Throttled(detail=message)

class RegisterAnonThrottle(AnonRateThrottle):
    rate = "5/minute" # Override the global

    def throttle_failure(self):
        # Custom error message
        message = "Too many register attempts. Please wait before trying again."
        # Raise custom message
        raise Throttled(detail=message)