from django.utils.deprecation import MiddlewareMixin
from .models import regesteruser

class RegesterUserSessionMiddleware(MiddlewareMixin):
    """
    Middleware to set request.user to the logged-in regesteruser
    based on session data.
    """
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = regesteruser.objects.get(id=user_id)
            except regesteruser.DoesNotExist:
                request.user = None
        else:
            request.user = None
