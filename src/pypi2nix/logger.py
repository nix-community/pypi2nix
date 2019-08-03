from typing import TextIO


class Logger:
    def __init__(self, output: TextIO):
        self.output = output

    def warning(self, text: str) -> None:
        for line in text.splitlines():
            print("WARNING:", line, file=self.output)

    def error(self, text: str) -> None:
        for line in text.splitlines():
            print("ERROR:", line, file=self.output)

    def info(self, text: str) -> None:
        for line in text.splitlines():
            print("INFO:", line, file=self.output)
