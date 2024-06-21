"""Main
main function and argument parsing (as applicable)
"""
from __future__ import annotations

import sys
import asyncio
import logging
import argparse

from collections import namedtuple

from typing import Callable, List

import commands

Task = namedtuple("Task", "func args kwargs")

def construct_task(func: Callable, *args, **kwargs):
    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    return Task(func=func, args=args, kwargs=kwargs)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s::%(levelname)s::%(module)s.%(funcName)s::%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__file__)


def argument_parsing(args: List[str]) -> argparse.Namespace:
    """Parse all arguments"""
    parser = argparse.ArgumentParser()
    return parser.parse_args(args)


def main(loop_tasks: List[Task] = None, pre_loop_tasks: List[Task] = None) -> None:
    """Run main loop"""
    loop = asyncio.new_event_loop()
    if pre_loop_tasks:
        for task in pre_loop_tasks:
            loop.run_until_complete(task.func(*task.args, **task.kwargs))
    for task in loop_tasks:
        loop.create_task(task.func(*task.args, **task.kwargs))
    loop.run_forever()
    

if __name__=="__main__":
    parsed_args = argument_parsing(sys.argv[1:])

    maintask = construct_task(commands.dispatcher.start_polling, commands.tgbot)

    loop_tasks = []
    loop_tasks.append(maintask)

    main(loop_tasks=loop_tasks)