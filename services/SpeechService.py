from vosk import Model, KaldiRecognizer
from utils.Helpers import GetBasePath

import json
import threading
import sounddevice as sd

class SpeechService:
    def __init__(self):
        # path location of the speech model
        self.modelPath = GetBasePath() / "speech" / "vosk-model-small-en-us-0.15"
        self.model = None
        self.recognizer = None
        self.stream = None
        self.thread = None
        self.callback = None
        self.isListening = False

    def start(self, callback):
        if self.isListening:
            return
        # set the necessary parameters for the thread
        if self.model is None:
            self.model = Model(str(self.modelPath))
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.callback = callback
        self.isListening = True
        self.thread = threading.Thread(
            target=self.listen,
            daemon=True
        )
        # start listening
        self.thread.start()

    def stop(self):
        self.isListening = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.thread = None
    
    # --- Listening thread ---

    def listen(self):
        def audio_callback(indata, frames, time, status):
            if self.recognizer.AcceptWaveform(indata):
                result = json.loads(
                    self.recognizer.Result()
                )
                text = result.get("text", "")
                if text:
                    if self.callback:
                        number = text_to_number(text)
                        self.callback(number)
        self.stream = sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=audio_callback
        )
        with self.stream:
            while self.isListening:
                sd.sleep(100)

    # --- Parsing ---

    def text_to_number(self, text):
        numbers = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90
        }
        text = text.lower().strip()
        words = text.split()
        # Single number:
        if len(words) == 1:
            return numbers.get(words[0], -1)
        # Two-part number: "twenty four"
        if len(words) == 2:
            first = numbers.get(words[0], -1)
            second = numbers.get(words[1], -1)
            # return if fail and not update, both numbers need to not be -1 basically
            if 20 <= first <= 90 and 0 <= second <= 9:
                return first + second
        return -1