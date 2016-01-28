from django.test import TestCase, RequestFactory
from django.core.management import call_command

# Create your tests here.
class ManagementTest(TestCase):

	def test_import_defaults(self):
		call_command('import_defaults')
