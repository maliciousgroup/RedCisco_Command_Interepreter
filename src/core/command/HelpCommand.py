import asyncio

from src.core.utils.colors import colors
from src.core.utils.tables import create_table

from src.core.base.BaseCommand import BaseCommand
from src.core.registry.CommandRegistry import global_command_registry

_colors: dict = colors()
red = _colors['red']
reset = _colors['reset']


class HelpCommand(BaseCommand):

    helper = {
        'name': 'help',
        'help': 'This command prints all available help information',
        'usage': 'help'
    }

    def __init__(self, command: str, print_queue: asyncio.Queue):
        """
        Class "initializer"

        :param command: User-supplied input
        :param print_queue: Asynchronous print queue
        """
        super().__init__()
        self.command: str = command
        self.pq: asyncio.Queue = print_queue

    async def main(self) -> None:
        """
        Coroutine that starts command logic

        :returns: None
        """
        await self.execute()

    async def execute(self) -> None:
        """
        Coroutine that handles any execution logic

        :returns: None
        """
        await self.pq.put((red, f'\nCore Commands\n{"=" * 13}\n'))
        field_names = [f'{"Command":<25}', f'{"Usage":<20}', f'{"Description":<30}']
        field_values = []
        for cls in global_command_registry:
            info = global_command_registry[cls].helper
            field_values.append([info['name'], info['usage'], info['help']])
        output: str = create_table(field_names, field_values)
        await self.pq.put(f'{output}\n')
