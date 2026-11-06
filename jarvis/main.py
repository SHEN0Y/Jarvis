import argparse

from dotenv import load_dotenv


def main():
    load_dotenv()
    from .brain import Brain

    p = argparse.ArgumentParser()
    p.add_argument("--voice", action="store_true", help="use microphone and speaker")
    args = p.parse_args()

    brain = Brain()
    if args.voice:
        from .voice import listen, speak

        get_input, output = listen, speak
    else:
        get_input, output = (lambda: input("You: ")), (lambda t: print(f"Jarvis: {t}"))

    print("Jarvis online. Say 'exit' to quit.")
    while True:
        text = get_input().strip()
        if not text:
            continue
        if text.lower() in {"exit", "quit"}:
            break
        output(brain.ask(text))
