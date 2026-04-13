from .models import FriendRequest

def notification_count(request):
    if request.user.is_authenticated:
        count = FriendRequest.objects.filter(
            receiver=request.user,
            accepted=False
        ).count()
        return {'pending_requests_count': count}
    return {'pending_requests_count': 0}