from pypi2nix.logger import Logger


def get_logger_output(logger: Logger) -> str:
    logger.output.seek(0)
    output = logger.output.read()
    logger.output.seek(0, 2)
    return output
