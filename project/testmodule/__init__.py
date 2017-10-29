from project.common import settings


settings.register(name='DEBUG', content_type=settings.TYPE_BOOL, default_value=True)
settings.register(name='PORT', setting_type=settings.TYPE_INTEGER, default_value=8000)


from .handlers import *
from .urls import *
