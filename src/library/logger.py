import logging
from pathlib import Path

def configure_console_logging() -> None:
	"""
	Configures the application's logging system to output all messages to the console.
    This function should only be called once during application startup.
    The configuration is applied to the root logger.
	Every logger created in the application inherits this configuration unless propagation is explicitly disabled.
	"""

	logging.basicConfig(
		format = '%(asctime)s\t%(levelname)s\t%(message)s',
		datefmt = '%Y-%m-%d %H:%M:%S',
		level = logging.INFO,
		handlers = [logging.StreamHandler()]
	)

def configure_file_logging(log_file: str | Path) -> None:
	"""
	Configures the application's logging system to output all messages to the console and the specified log file.
    This function should only be called once during application startup.
    The configuration is applied to the root logger.
	Every logger created in the application inherits this configuration unless propagation is explicitly disabled.

	Parameters:
		log_file (str | Path): Absolute path to the log file to be used for logging
	"""

	logging.basicConfig(
		format = '%(asctime)s\t%(levelname)s\t%(message)s',
		datefmt = '%Y-%m-%d %H:%M:%S',
		level = logging.INFO,
		handlers = [
			logging.StreamHandler(),
			logging.FileHandler(log_file, encoding = 'utf-8')
		]
	)