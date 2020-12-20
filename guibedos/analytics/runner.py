import sys
import asyncio


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
        _read_stream(process.stdout, stdout_callback, sys.stdout.buffer),
        _read_stream(process.stderr, stderr_callback, sys.stderr.buffer)
    ])

    return await process.wait()


def execute(command, stdout_callback=None, stderr_callback=None):
    loop = asyncio.get_event_loop()
    exit_code = loop.run_until_complete(
        _stream_subprocess(
            command,
            stdout_callback,
            stderr_callback,
    ))
    loop.close()
    return exit_code
