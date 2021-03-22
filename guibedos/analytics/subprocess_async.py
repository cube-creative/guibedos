import sys
import asyncio
import platform


class _Buffer:
    """
    This was created to fix JetBrain's FlushingStringIO having no .buffer attribute (used for tests)
    https://github.com/JetBrains/teamcity-messages/blob/master/teamcity/common.py
    """
    def __init__(self, o):
        self.o = o

    def write(self, l):
        try:
            self.o.buffer.write(l)
        except AttributeError:
            self.o.write(l.decode())


async def _read_stream(stream, callback, buffer):
    while True:
        line = await stream.readline()
        if line:
            buffer.write(line)
            if callback is not None:
                callback(line)
        else:
            break


async def _stream_subprocess(command, stdout_callback, stderr_callback):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await asyncio.wait([
        _read_stream(process.stdout, stdout_callback, _Buffer(sys.stdout)),
        _read_stream(process.stderr, stderr_callback, _Buffer(sys.stderr))
    ])

    return await process.wait()


def run(command, stdout_callback=None, stderr_callback=None):
    if platform.system() == "Windows":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    exit_code = loop.run_until_complete(
        _stream_subprocess(
            command,
            stdout_callback,
            stderr_callback,
    ))
    loop.close()
    return exit_code
