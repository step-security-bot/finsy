"Logging utilities."

# Copyright (c) 2022 Bill Fisher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import os
import sys
from functools import wraps

DEBUG = os.environ.get("FINSY_DEBUG")


class _CustomAdapter(logging.LoggerAdapter):
    """Custom log adapter to include the name of the current task."""

    def process(self, msg, kwargs):
        task_name = ""
        try:
            # current_task() will raise a RuntimeError if there is no running
            # event loop. It can also return None if there's a running event
            # loop but we aren't in a task (ie we're in a low-level callback).
            task = asyncio.current_task()
            if task:
                task_name = task.get_name()
                # Remove the "fy:" prefix from the task name before logging.
                if task_name.startswith("fy:"):
                    task_name = task_name[3:]
                task_name = f"[{task_name}] "
            else:
                task_name = "[] "  # low-level callback - no running task
        except RuntimeError:
            pass

        return f"{task_name}{msg}", kwargs


LOGGER = _CustomAdapter(logging.getLogger(__package__))
MSG_LOG = _CustomAdapter(logging.getLogger(f"{__package__}.msg"))
TRACE_LOG = _CustomAdapter(logging.getLogger(f"{__package__}.trace"))


def _exc():
    # TODO: replace sys.exc_info() with sys.exception() someday...
    return sys.exc_info()[1]


def _trace(func):
    @wraps(func)
    async def wrapper(*args, **kwd):
        try:
            TRACE_LOG.info("%s stepin", func.__qualname__)
            return await func(*args, **kwd)
        finally:
            TRACE_LOG.info("%s stepout ex=%r", func.__qualname__, _exc())

    return wrapper


def _trace_noop(func):
    return func


if DEBUG:
    TRACE = _trace
else:
    TRACE = _trace_noop
