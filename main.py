from camera_analyzer import CameraAnalyzerInterface
from camera_analyzer import CameraReader

class SendMessage(CameraAnalyzerInterface):
    def __init__(self):
        pass

    def run(self):
        print("***\nMotion detected\n***")


if __name__ == "__main__":
    reader = CameraReader(display=False)
    reader.add_reaction(SendMessage())
    reader.run(fps=1)