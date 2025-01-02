# whatsapp/context_processors.py

from .models import SuperAdmin, User

def Super_Admin(request):
    username = request.session.get('username')
    if username:
        try:
            SA = SuperAdmin.objects.get(sa_username=username)
            return {'Super_Admin': SA}
        except SuperAdmin.DoesNotExist:
            pass
    return {'Super_Admin': None}

def Custom_User(request):
    username = request.session.get('username')
    if username:
        try:
            user = User.objects.get(username=username)
            return {'Custom_User': user}
        except User.DoesNotExist:
            pass
    return {'Custom_User': None}
