import os

from django.test import TestCase

class CoreAppTests(TestCase):
    def test_app_in_test_runtime(self):
        runtime = os.getenv('RUNTIME_ENVIRONMENT')
        self.assertEqual(runtime, 'test', 'Application should have been bootstrapped in test runtime')
