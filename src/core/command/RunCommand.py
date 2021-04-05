import asyncio
import netdev

from src.core.base.BaseCommand import BaseCommand
from src.core.registry.OptionsRegistry import OptionRegistry


class RunCommand(BaseCommand):

    helper = {
        'name': 'run',
        'help': 'This command will start the connection process',
        'usage': 'run'
    }

    def __init__(self, command: str, print_queue: asyncio.Queue):
        super().__init__()
        self.command: str = command
        self.print_queue: asyncio.Queue = print_queue
        self.options: OptionRegistry = OptionRegistry()
        self.end_points: list = []

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
        _options: dict = self.options.get_registry_pairs()
        await self.parse_options(_options)

    async def parse_options(self, options: dict) -> None:
        """
        Class Coroutine that parses the user-supplied options

        :param options: User-supplied options
        :return: None
        """

        """
        host: str = options['host'][0]
        username: str = options['username'][0]
        password: str = options['password'][0]
        secret: str = options['secret'][0]

        if not all([host, username, password, secret]):
            await self.print_queue.put(('error', f"Required target options are missing\n"))
            return

        try:
            socket.inet_aton(host)
        except socket.error:
            await self.print_queue.put(('error', f"The host address '{host}' is not a valid IP address.\n"))
            return

        params: dict = {
            'host': host,
            'username': username,
            'password': password,
            'device_type': 'cisco_ios',
            'secret': secret
        }

        enable_docker: str = options['enable_docker'][0]
        docker_host: str = options['docker_host'][0]
        enable_http: str = options['enable_http'][0]
        enable_http_port: str = options['enable_http_port'][0]
        enable_tftp: str = options['enable_tftp'][0]
        enable_tftp_port: str = options['enable_tftp_port'][0]

        if enable_docker == 'true':
            try:
                socket.inet_aton(docker_host)
            except socket.error:
                await self.print_queue.put(
                    ('error', f"The docker host address '{docker_host}' is not a valid IP address.\n"))
                return
            if enable_http == 'true':
                if not 1 <= int(enable_http_port) <= 65535:
                    await self.print_queue.put(
                        ('error', f"The HTTP port {enable_http_port} is out of range. (1-65535).\n"))
                    return
                tag: str = 'malicious_http'
                path: str = 'src/docker/services/http'
                ports: dict = {'8000/tcp': enable_http_port}
                builder = BuildHandler(self.print_queue)
                end_point = f"http://{docker_host}:{enable_http_port}/"
                if end_point not in self.end_points:
                    self.end_points.append(end_point)
                await builder.build_image(path, tag, ports)

            if enable_tftp == 'true':
                if not 1 <= int(enable_tftp_port) <= 65535:
                    await self.print_queue.put(
                        ('error', f"The Trivial FTP port {enable_tftp_port} is out of range. (1-65535).\n"))
                    return
                tag: str = 'malicious_tftp'
                path: str = 'src/docker/services/tftp'
                ports: dict = {'9069/udp': enable_tftp_port}
                builder = BuildHandler(self.print_queue)
                end_point = f"tftp://{docker_host}:{enable_tftp_port}/"
                if end_point not in self.end_points:
                    self.end_points.append(end_point)
                await builder.build_image(path, tag, ports)

        enable_remote: str = options['enable_remote'][0]
        remote_host: str = options['remote_host'][0]
        enable_remote_http: str = options['enable_remote_http'][0]
        enable_remote_http_port: str = options['enable_remote_http_port'][0]
        enable_remote_tftp: str = options['enable_remote_tftp'][0]
        enable_remote_tftp_port: str = options['enable_remote_tftp_port'][0]

        if enable_remote == 'true':
            try:
                socket.inet_aton(remote_host)
            except socket.error:
                await self.print_queue.put(
                    ('error', f"The remote host address '{remote_host}' is not a valid IP address.\n"))
                return
            if enable_remote_http == 'true':
                if not 1 <= int(enable_remote_http_port) <= 65535:
                    await self.print_queue.put(
                        ('error', f"The HTTP port {enable_remote_http_port} is out of range. (1-65535).\n"))
                    return
                end_point = f"http://{remote_host}:{enable_remote_http_port}/"
                if end_point not in self.end_points:
                    self.end_points.append(end_point)

            if enable_remote_tftp == 'true':
                if not 1 <= int(enable_remote_tftp_port) <= 65535:
                    await self.print_queue.put(
                        ('error', f"The Trivial FTP port {enable_remote_tftp_port} is out of range. (1-65535).\n"))
                    return
                end_point = f"tftp://{remote_host}:{enable_remote_tftp_port}/"
                if end_point not in self.end_points:
                    self.end_points.append(end_point)

        # Create Connection
        try:
            await self.print_queue.put(('bold', f"Attempting connection to the target device '{host}'"))
            async with netdev.create(**params) as ios:
                await self.print_queue.put(('success', f"Successfully connected to the target device '{host}'"))
                device: DeviceHandler = DeviceHandler(self.print_queue, self.end_points, params)

        except netdev.DisconnectError as e:
            await self.print_queue.put(('error', f"{e.__str__()}\n"))
            return
        except netdev.TimeoutError as e:
            await self.print_queue.put(('error', f"{e.__str__()}\n"))
            return
        except Exception as e:
            await self.print_queue.put(('error', f"{e.__str__()}\n"))
            return
        """
