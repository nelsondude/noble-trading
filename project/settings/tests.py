import os
import sys

from unittest import TestCase

from .defines import Setting
from .models import Settings


__all__ = ('TornadoSettingsTestCase',)


class TornadoSettingsTestCase(TestCase):

    SETTING_NAME = 'SETTINGS_TEST'
    ENV_SETTING_NAME = '{prefix}_{name}'.format(prefix=Settings.ENV_PREFIX, name=SETTING_NAME)

    def setUp(self):
        self.assertNotIn(self.ENV_SETTING_NAME, os.environ)
        self._sys_argv = tuple(sys.argv)

    def test_settings(self):
        DEFAULT_VALUE = 10
        ENVIRON_VALUE = 20
        COMMAND_LINE_VALUE = 30

        defines = (
            Setting(name=self.SETTING_NAME, content_type=int, default=DEFAULT_VALUE, description="Test."),
        )
        settings = Settings(defines=defines)
        self.assertEqual(getattr(settings, self.SETTING_NAME), DEFAULT_VALUE)

        os.environ[self.ENV_SETTING_NAME] = str(ENVIRON_VALUE)
        settings = Settings(defines=defines)
        self.assertEqual(getattr(settings, self.SETTING_NAME), ENVIRON_VALUE)

        sys.argv.insert(1, '--{name}={value}'.format(name=self.SETTING_NAME, value=COMMAND_LINE_VALUE))
        settings = Settings(defines=defines)
        self.assertEqual(getattr(settings, self.SETTING_NAME), COMMAND_LINE_VALUE)

    def test_edit_setting(self):
        DEFAULT_VALUE = 10
        NEW_VALUE = 20

        defines = (
            Setting(name=self.SETTING_NAME, content_type=int, default=DEFAULT_VALUE, description="Test."),
        )
        settings = Settings(defines=defines)
        self.assertEqual(getattr(settings, self.SETTING_NAME), DEFAULT_VALUE)

        self.assertRaises(RuntimeError, setattr, settings, self.SETTING_NAME, NEW_VALUE)

        self.assertEqual(getattr(settings, self.SETTING_NAME), DEFAULT_VALUE)
        settings.update_setting(name=self.SETTING_NAME, value=NEW_VALUE)
        self.assertEqual(getattr(settings, self.SETTING_NAME), NEW_VALUE)

    def tearDown(self):
        if self.ENV_SETTING_NAME in os.environ:
            del os.environ[self.ENV_SETTING_NAME]
        sys.argv = list(self._sys_argv)
