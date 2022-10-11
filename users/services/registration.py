from users.models import User


def is_username_used(username: str):
    return User.objects.filter(username=username).exists()
