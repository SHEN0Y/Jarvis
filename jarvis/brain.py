import os

import anthropic

from .tools import TOOLS, run_tool

MODEL = os.getenv("JARVIS_MODEL", "claude-sonnet-5-5")
SYSTEM = (
    "You are Jarvis, a concise, witty, highly capable personal assistant. "
    "Use your tools when they help. Keep spoken-style answers short."
)


class Brain:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.history = []

    def ask(self, text: str) -> str:
        self.history.append({"role": "user", "content": text})
        while True:
            resp = self.client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM,
                tools=[t["schema"] for t in TOOLS.values()],
                messages=self.history,
            )
            self.history.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason != "tool_use":
                return "".join(b.text for b in resp.content if b.type == "text")
            results = [
                {
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": run_tool(b.name, b.input),
                }
                for b in resp.content
                if b.type == "tool_use"
            ]
            self.history.append({"role": "user", "content": results})
