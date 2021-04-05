import asyncio
import signal

from ruamel.yaml import YAML, YAMLError

# noinspection PyUnresolvedReferences
from src.core.command import *
from src.core.utils.colors import colors
from src.core.base.BaseConsole import BaseConsole
from src.core.registry.CommandRegistry import global_command_registry
from src.core.registry.OptionsRegistry import OptionRegistry

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

_colors: dict = colors()
red = _colors['red']
bold = _colors['bold']
green = _colors['green']
reset = _colors['reset']

_prompt_style = Style.from_dict({"prompt": "ansired bold"})


class Console(BaseConsole):

    def __init__(self, config: str, prompt: str):
        self.prompt: str = prompt
        self.end_points: list = []
        self.print_queue: asyncio.Queue = asyncio.Queue()
        self.registry: OptionRegistry = OptionRegistry()

        self.__register(config, self.registry)

    @staticmethod
    def __register(_config: str, _registry: OptionRegistry) -> None:
        yaml = YAML()
        try:
            with open(_config, "r") as conf:
                _registry.register_options(yaml.load(conf))
        except YAMLError:
            print(f"Error occurred while processing configuration file: {_config}")
            exit(1)

    async def interactive_shell(self) -> None:
        session = PromptSession()
        while True:
            try:
                _input: str = await session.prompt_async(self.prompt, style=_prompt_style)
                if not _input:
                    continue

                for cls in global_command_registry:
                    if not asyncio.iscoroutinefunction(global_command_registry[cls].main):
                        continue
                    command: str = _input.partition(' ')[0]
                    if command == global_command_registry[cls].helper['name']:
                        await asyncio.gather(global_command_registry[cls](_input, self.print_queue).main())
            except (EOFError, KeyboardInterrupt):
                break

    async def print_processor(self) -> None:
        while True:
            try:
                while self.print_queue.empty() is not True:
                    _msg = await self.print_queue.get()
                    if isinstance(_msg, str):
                        print(f'{_msg}')
                    elif isinstance(_msg, tuple):
                        if _msg[0] == 'error':
                            print(f'{red}{_msg[1]}{reset}')
                        elif _msg[0] == 'success':
                            print(f'{green}{_msg[1]}{reset}')
                        elif _msg[0] == 'bold':
                            print(f'{bold}{_msg[1]}{reset}')
                        else:
                            print(f'{_msg[1]}')
                await asyncio.sleep(0.002)
            except asyncio.CancelledError:
                await self.shutdown(asyncio.get_running_loop())

    @staticmethod
    async def shutdown(_loop) -> None:
        print(f'Closing application gracefully!')
        print(f'Stopping all running tasks...')
        tasks = [t.cancel() for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        await asyncio.gather(*tasks)
        _loop.stop()

    async def main(self) -> None:
        asyncio.current_task().set_name('Task-Main')
        loop = asyncio.get_running_loop()
        signals = (signal.SIGINT, signal.SIGTERM)

        for s in signals:
            try:
                loop.add_signal_handler(s, lambda _s=s: asyncio.create_task(self.shutdown(loop)))
            except NotImplementedError:
                pass

        with patch_stdout():
            print_task = asyncio.create_task(self.print_processor(), name='Task-PrintQueue')
            try:
                await self.interactive_shell()
            except asyncio.CancelledError:
                pass
            finally:
                print_task.cancel()
