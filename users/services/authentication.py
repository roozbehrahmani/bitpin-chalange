from users.services.token import TokenManager


def force_authenticate(request, user):
    refresh_token, access_token = TokenManager.generate_refresh_token(user=user)
    request._force_auth_token = access_token
    request._force_auth_user = user
    return (refresh_token, access_token)
