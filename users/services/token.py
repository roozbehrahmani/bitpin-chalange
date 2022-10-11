from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache


class TokenManager:
    REFRESH_KEY = "TOKEN_ACCESS_REFRESH_{}"
    CACHE_KEY_TEMPLATE = 'USER_PERMISSION_{}_{}'
    CACHE_TIME = 24 * 60 * 60

    def __init__(self, token):
        self.token = token

    @staticmethod
    def _save_token(user_id, access, refresh):
        # save_user_token.apply_async(args=[
        #     user_id,
        #     str(access),
        #     str(refresh)
        # ])
        cache.set(TokenManager._get_refresh_key(token=access), refresh, TokenManager.CACHE_TIME)

    @staticmethod
    def _get_refresh_key(token):
        return TokenManager.REFRESH_KEY.format(token)

    @staticmethod
    def _get_key(token, scope):
        return TokenManager.CACHE_KEY_TEMPLATE.format(scope, token)

    @staticmethod
    def _set_cache(token, scope, level):
        cache.set(TokenManager._get_key(token=token, scope=scope), level, TokenManager.CACHE_TIME)

    @staticmethod
    def _delete_cache(token, scope):
        cache.delete(TokenManager._get_key(token=token, scope=scope))

    @staticmethod
    def generate_refresh_token(user):
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        TokenManager._save_token(user_id=user.id, access=access_token, refresh=refresh_token)
        return (refresh_token, access_token)

    @staticmethod
    def generate_access(refresh):
        try:
            refresh = RefreshToken(refresh)
        except Exception as e:
            raise e
        access = str(refresh.access_token)
        cache.set(TokenManager._get_refresh_key(token=access), refresh, TokenManager.CACHE_TIME)
        authenticator = JWTAuthentication()
        valid_token = authenticator.get_validated_token(raw_token=access)
        user = authenticator.get_user(validated_token=valid_token)
        TokenManager._save_token(user_id=user.id, access=access, refresh=refresh)
        return access


    def get_layer(self, scope):
        return cache.get(TokenManager._get_key(token=self.token, scope=scope), None)

    def delete_state(self, scope):
        self._delete_cache(token=self.token, scope=scope)
