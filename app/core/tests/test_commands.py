"""
Django management commands
"""

# patch mocks the behavior of the django get_database function
from unittest.mock import patch
# Psycopg2Error is the error that is raised when the database is not available - possible error
from psycopg2 import OperationalError as Psycopg2Error
# call_command allows us to call the command from the code
from django.core.management import call_command
# OperationalError is the error that is raised when the database is not available - possible error
from django.db.utils import OperationalError
# dont need mogrations and only need SimpleTestCase
from django.test import SimpleTestCase



# mocks the behavior
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        # when check is called, it will return True only
        patched_check.return_value = True
        # call the command executes codein the command
        call_command('wait_for_db')
        # checks that the correct db is called
        patched_check.assert_called_once_with(databases=['default'])
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting operational error"""
        # rraise and exception iusing side effectr. pass in an ecxception, and then the number of times to raise it
        # deifine different values for each time it is called
        patched_check.side_effect = [Psycopg2Error] * 2 +\
            [OperationalError] * 3 + [True]
        # call the command executes code in the command
        call_command('wait_for_db')
        # checks that call is made 6 times
        self.assertEqual(patched_check.call_count, 6)
        # checks that the correct db is called
        patched_check.assert_called_with(databases=['default'])
