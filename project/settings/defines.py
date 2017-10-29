from collections import namedtuple


__all__ = ('DEFINES',)


Setting = namedtuple(typename='Setting', field_names=('name', 'content_type', 'default', 'description'))


DEFINES = (
    Setting(name='DEBUG', content_type=bool, default=True, description="Enable debug mode."),
    Setting(name='PORT', content_type=int, default=80, description="Port, default: 8000."),
    Setting(
        name='COOKIE_SECRET',
        content_type=str,
        default='sm@g)(fbwdh5wc*xe@j++m9rh^uza5se9a57c5ptwkg*b@ki0x',
        description='Cookie Key')
)
