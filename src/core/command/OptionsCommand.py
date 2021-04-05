import asyncio

from src.core.utils.colors import colors
from src.core.utils.tables import create_table

from src.core.base.BaseCommand import BaseCommand
from src.core.registry.OptionsRegistry import OptionRegistry

_colors: dict = colors()
red = _colors['red']
reset = _colors['reset']


class CommandOptions(BaseCommand):

    helper = {
        'name': 'options',
        'help': 'This command prints all available options',
        'usage': 'options'
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
        self.registry: OptionRegistry = OptionRegistry()

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
        options: dict = self.registry.get_register_dict()
        for x in options.keys():
            await self.pq.put(f'\n{x}\n{"=" * len(x)}\n')
            field_names: list = [f'{"Option":<25}', f'{"Setting":<20}', f'{"Description":<30}']
            field_values: list = []
            for item in options[x].items():
                field_values.append([item[0], item[1][0], item[1][1]])
            output: str = create_table(field_names, field_values)
            await self.pq.put(output)
            await self.pq.put('')
