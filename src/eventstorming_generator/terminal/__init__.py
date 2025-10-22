from .runs.run_command import run_command
from .helps.help_command import help_command

command_handlers = {
    "run": run_command,
    "help": help_command
}