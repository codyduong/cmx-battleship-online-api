from django.test import TestCase
from django.conf import settings


class CoreAppTest(TestCase):
    def test_app_in_test_runtime(self):
        runtime = settings.RUNTIME_ENVIRONMENT
        self.assertEqual(runtime, 'test', 'Application should have been bootstrapped in test runtime')
