import os

from tornado import options

from .defines import DEFINES


__all__ = ('settings',)


class Settings:

    ENV_PREFIX = 'PROJECT'

    _setting_parsers = {}

    def __init__(self, defines):
        for setting_define in defines:
            if setting_define.name.upper() != setting_define.name:
                raise ValueError("Setting name must be uppercase.")
            if setting_define.content_type not in self._setting_parsers:
                raise ValueError("Unknown setting content type.")
            if setting_define.name in self.__dict__:
                raise ValueError("Invalid setting name.")

            default = os.getenv(
                '{prefix}_{attr}'.format(
                    prefix=self.ENV_PREFIX,
                    attr=setting_define.name),
                setting_define.default
            )

            parser = self._setting_parsers[setting_define.content_type]

            options.define(
                setting_define.name,
                type=parser.OPTIONS_TYPE,
                default=parser.decode(value=default),
                help=setting_define.description
            )

        options.parse_command_line()

    def __setattr__(self, key, value):
        if key in options.options:
            raise RuntimeError("Settings are immutable.")
        super(Settings, self).__setattr__(key=key, value=value)

    def __getattr__(self, item):
        return options.options[item]

    @classmethod
    def register_content_type(cls, content_type_name, content_type_cls):
        if content_type_name in cls._setting_parsers:
            raise ValueError("Duplicate setting content type.")
        cls._setting_parsers[content_type_name] = content_type_cls

    def update_setting(self, name, value):
        setattr(options.options, name, value)


class SettingTypeMeta(type):

    def __init__(cls, name, bases, attrs):
        super(SettingTypeMeta, cls).__init__(name, bases, attrs)
        if getattr(cls, 'CONTENT_TYPE_NAMES', None):
            for content_type_name in cls.CONTENT_TYPE_NAMES:
                Settings.register_content_type(content_type_name=content_type_name, content_type_cls=cls)


class SettingType(metaclass=SettingTypeMeta):

    CONTENT_TYPE_NAMES = None
    OPTIONS_TYPE = None


class IntegerSettingType(SettingType):

    CONTENT_TYPE_NAMES = (int, 'int', 'integer')
    OPTIONS_TYPE = int

    @classmethod
    def decode(cls, value):
        if isinstance(value, int):
            return value
        return int(value)


class StringSettingType(SettingType):

    CONTENT_TYPE_NAMES = (str, 'str', 'string')
    OPTIONS_TYPE = str

    @classmethod
    def decode(cls, value):
        if isinstance(value, str):
            return value
        return str(value)


class BooleanSettingType(SettingType):

    CONTENT_TYPE_NAMES = (bool, 'bool', 'boolean')
    OPTIONS_TYPE = bool

    @classmethod
    def decode(cls, value):
        if isinstance(value, bool):
            return value
        if str(value).lower() in ('t', 'true', 'y', 'yes'):
            return True
        return False


settings = Settings(defines=DEFINES)