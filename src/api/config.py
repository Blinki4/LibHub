from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_SECRET_KEY = 'LIB_HUB_SECRET'
config.JWT_ACCESS_COOKIE_NAME = 'access_token'
config.JWT_TOKEN_LOCATION = ['cookies']


security = AuthX(config=config)