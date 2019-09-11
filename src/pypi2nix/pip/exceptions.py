class PipFailed(Exception):
    def __init__(self, output: str) -> None:
        self.output = output
        super().__init__()
