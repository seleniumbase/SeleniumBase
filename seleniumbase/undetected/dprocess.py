#!/usr/bin/env python3
import os
import sys
import atexit
import logging
from subprocess import PIPE

CREATE_NEW_PROCESS_GROUP = 0x00000200
DETACHED_PROCESS = 0x00000008
REGISTERED = []


def start_detached(executable, *args):
    """Starts a fully independent subprocess with no parent.
    :param executable: executable
    :param args: arguments to the executable,
        eg: ["--param1_key=param1_val", "-vvv"]
    :return: pid of the grandchild process """
    import multiprocessing

    reader, writer = multiprocessing.Pipe(False)  # Create pipe
    multiprocessing.Process(
        target=_start_detached,
        args=(executable, *args),
        kwargs={"writer": writer},
        daemon=True,
    ).start()
    # Receive pid from pipe
    pid = reader.recv()
    REGISTERED.append(pid)
    # Close pipes
    writer.close()
    reader.close()
    return pid


def _start_detached(executable, *args, writer=None):
    # Configure Launch
    kwargs = {}
    import platform
    from subprocess import Popen

    if platform.system() == "Windows":
        kwargs.update(
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        )
    else:
        kwargs.update(start_new_session=True)
    p = Popen(
        [executable, *args], stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs
    )
    # Send pid to pipe
    writer.send(p.pid)
    sys.exit()


def _cleanup():
    import signal

    for pid in REGISTERED:
        try:
            logging.getLogger(__name__).debug("cleaning up pid %d " % pid)
            os.kill(pid, signal.SIGTERM)
        except Exception:
            pass


atexit.register(_cleanup)
