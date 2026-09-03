from vosk import Model
from utils.Helpers import GetBasePath

class SpeechService:
    def __init__(self):
        # path location of the speech model
        self.modelPath = GetBasePath() / "speech" / "vosk-model-small-en-us-0.15"
        self.model = None

    def get_model(self):
        if self.model is None:
            self.model = Model(str(self.modelPath))
        return self.model