"""Optional voice I/O. Install requirements-voice.txt first."""
import pyttsx3
import speech_recognition as sr

_engine = pyttsx3.init()
_rec = sr.Recognizer()


def listen() -> str:
    with sr.Microphone() as mic:
        _rec.adjust_for_ambient_noise(mic)
        audio = _rec.listen(mic)
    try:
        return _rec.recognize_google(audio)
    except sr.UnknownValueError:
        return ""


def speak(text: str) -> None:
    _engine.say(text)
    _engine.runAndWait()
