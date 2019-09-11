from pypi2nix.logger import Logger
from pypi2nix.logger import ProxyLogger
from pypi2nix.logger import StreamLogger


def get_logger_output(logger: Logger) -> str:
    def get_inner_logger(logger: Logger) -> StreamLogger:
        if isinstance(logger, StreamLogger):
            return logger
        elif isinstance(logger, ProxyLogger):
            inner_logger = logger.get_target_logger()
            if inner_logger is None:
                raise Exception("ProxyLogger is not connected, cannot get output")
            else:
                return get_inner_logger(inner_logger)
        else:
            raise Exception("Unhandled Logger implementation", type(logger))

    logger = get_inner_logger(logger)
    logger.output.seek(0)
    output = logger.output.read()
    logger.output.seek(0, 2)
    return output
