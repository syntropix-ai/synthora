from typing import List, Optional

from synthora.agents.base import BaseAgent


class WhatsApp:
    def send_messsage(self, to: str, text: str, image: Optional[str] = None, file: Optional[str] = None):
        pass
    def set_main_agent(self, agent: BaseAgent):
        pass
    def set_guard_agent(self, agent: BaseAgent):
        pass
    def run(self):
        pass

    def auto_reply(self, message: List[str], response: str, threshold: float = 0.5):
        pass