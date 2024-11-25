# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

from typing import Any, Dict, List, Optional

from rich.box import Box
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.status import Status

from synthora.callbacks.base_handler import BaseCallBackHandler
from synthora.types.enums import Result
from synthora.types.node import Node


HEAVY: Box = Box(
    """\
┏━┳┓
┃ ┃┃
┣━╋┫
┃ ┃┃
┣━╋┫
┣━╋┫
┃ ┃┃
┗━┻┛
"""
)


class RichOutputHandler(BaseCallBackHandler):
    def __init__(self, console: Optional[Console] = None) -> None:
        self.console: Console = console or Console()
        self.status_stack: List[str] = []
        self.status: Optional[Status] = None
        self.live: Optional[Live] = None
        self.cache: str = ""
        super().__init__()

    def stop(self):
        """
        Stops the Live status.
        """
        if self.status is not None:
            self.status.stop()

    def update_status(self, output: str, style: str = "[bold green]"):
        """
        Updates the status, push it into a stack.

        :param output: The output to update the status with.
        :type output: str
        :param style: The style to use for the output. Defaults to "[bold green]".
        :type style: str
        """
        self.status_stack.append(output)
        if self.status is not None:
            self.status.update(f"{style}{output}")
        else:
            self.status = self.console.status(f"{style}{output}")
        self.status.start()

    def thinking(self, name: str):
        """
        Shows that a name is thinking.

        :param name: The name of the entity that is thinking.
        :type name: str
        """
        self.status_stack.append(name)
        if self.status is not None:
            self.status.update(f"[bold green]{name} is thinking...")
        else:
            self.status = self.console.status(f"[bold green]{name} is thinking...")
        self.status.start()

    def done(self, _all=False):
        """
        Marks the status as done.

        :param _all: If True, marks all status as done. If False, marks only the last status as done. Defaults to False.
        :type _all: bool
        """
        if _all:
            self.status_stack = []
            self.status.stop()
        else:
            if len(self.status_stack) > 0:
                self.status_stack.pop()
            if len(self.status_stack) > 0:
                self.status.update(
                    f"[bold green]{self.status_stack[-1]} is thinking..."
                )
            else:
                self.status.stop()

    def stream_print(self, item: str):
        """
        Prints an item to the output as a stream.

        :param item: The item to print.
        :type item: str
        """
        self.console.print(item, end="")

    def json_print(self, item: Dict[str, Any]):
        """
        Prints an item to the output as a JSON object.

        :param item: The item to print.
        :type item: Dict[str, Any]
        """
        self.console.print_json(data=item)

    def panel_print(
        self,
        item: Any,
        title: str = "Output",
        stream: bool = False,
        style: str = "yellow",
    ):
        """
        Prints an item to the output as a panel.

        :param item: The item to print.
        :type item: Any
        :param title: The title of the panel. Defaults to "Output".
        :type title: str
        :param stream: If True, prints the item as a stream. If False, prints the item as a panel. Defaults to False.
        :type stream: bool
        """
        item = item if isinstance(item, str) else str(item)
        if not stream:
            self.console.print(
                Panel(Markdown(item), title=title, style=style, box=HEAVY)
            )
            return
        if self.live is None:
            self.cache = item
            self.live = Live(
                Panel(Markdown(self.cache), title=title, style=style, box=HEAVY),
                console=self.console,
                refresh_per_second=12,
            )
            self.live.start()
            return
        self.cache += item
        self.live.update(
            Panel(Markdown(self.cache), title=title, style=style, box=HEAVY)
        )

    def clear(self):
        """
        Clears the Live status and print cache.
        """
        if self.live is not None:
            self.live.stop()
            self.live = None
        self.cache = ""

    def on_tool_start(
        self, source: Optional[Node], *args: Any, **kwargs: Dict[str, Any]
    ) -> None:
        self.update_status(f"Calling Tool: {source.name if source else 'Unknown'}")

    def on_tool_end(
        self, source: Optional[Node], result: Result[Any, Exception]
    ) -> None:
        self.done()
        title = f"[cyan]{source.name}" if source else "[cyan]Unknown"
        self.panel_print(result.value, title=title, style="cyan")

    def on_tool_error(
        self, source: Optional[Node], result: Result[Any, Exception]
    ) -> None:
        self.done()
        title = f"[red]{source.name}" if source else "[red]Unknown"
        self.panel_print(result.error, title=title, style="red")

    def on_llm_start(self, source, messages, stream: bool = False, *args, **kwargs):
        self.thinking(source.name if source else "Unknown")

    def on_llm_chunk(self, source, message, *args, **kwargs):
        if message.chunk:
            if self.status is not None:
                self.status.stop()
            self.panel_print(
                message.chunk,
                title=source.name if source.name else "Unknow",
                stream=True,
            )

    def on_llm_end(self, source, message, stream: bool = False, *args, **kwargs):
        self.done()
        if not stream and message.content:
            self.panel_print(
                message.content, title=source.name if source.name else "Unknow"
            )
        self.clear()
        if self.status is not None:
            self.status.start()

    def on_llm_error(self, source, e, stream: bool = False, *args, **kwargs):
        self.done()
        self.panel_print(str(e), title=source.name if source.name else "Unknow")
        self.clear()
        if self.status is not None:
            self.status.start()

    def on_agent_start(self, source, message, *args, **kwargs):
        title = f"[bold blue]{source.name if source else 'Unknown'}' Task: "
        self.panel_print(message.content, title=title, style="blue")

    def on_agent_end(self, source, message, *args, **kwargs):
        title = f"[bold blue]{source.name if source else 'Unknown'}' Response: "
        self.panel_print(message.content, title=title, style="green")
        self.clear()
        self.done(True)

    def on_agent_error(self, source, e, *args, **kwargs):
        title = f"[bold blue]{source.name if source else 'Unknown'}' Error: "
        self.panel_print(str(e), title=title, style="red")
        self.clear()
        self.done(True)
