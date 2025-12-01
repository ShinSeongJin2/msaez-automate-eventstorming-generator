from .runs.run_command import run_command
from .terminal_tests.terminal_test_command import terminal_test_command
from .utils.util_command import util_command
from .helps.help_command import help_command

command_handlers = {
    "run": run_command,
    "test": terminal_test_command,
    "util": util_command,
    "help": help_command
}