# Jarvis

A starter repo for building your own Jarvis-style AI assistant: a Claude-powered brain, a plug-in tool system, and optional voice.

## Quick start

```bash
git clone <your-repo-url> && cd jarvis-assistant
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your ANTHROPIC_API_KEY
python -m jarvis            # text mode
python -m jarvis --voice    # voice mode (needs: pip install -r requirements-voice.txt)
```

## Structure

| File | Purpose |
|---|---|
| `jarvis/brain.py` | Chat loop with Claude + tool calling |
| `jarvis/tools.py` | Tool registry. Add a function with `@tool` to give Jarvis a new ability |
| `jarvis/voice.py` | Optional speech-to-text and text-to-speech |
| `jarvis/main.py` | CLI entry point |

## Adding a skill

```python
@tool("Turn on the lights in a room", {"room": {"type": "string"}})
def lights_on(room: str) -> str:
    # call your smart-home API here
    return f"Lights on in {room}"
```

## Roadmap ideas

- [ ] Wake word ("Hey Jarvis")
- [ ] Calendar and email tools
- [ ] Smart home integration
- [ ] Persistent memory
- [ ] Web/desktop UI

## Safety

Tools run on your machine. Keep them narrow, and add confirmation prompts before anything destructive.
