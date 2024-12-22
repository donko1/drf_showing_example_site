from rest_framework.throttling import SimpleRateThrottle


class AdminUserThrottle(SimpleRateThrottle):
    scope = "example-class"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated or not request.user.is_staff:
            return None

        return f"throttle_admin_{request.user.pk}"
