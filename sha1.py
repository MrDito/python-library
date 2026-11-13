from pathlib import Path

def read(sha1: str | Path, relative_paths: bool = False) -> dict[str, str]:
	"""
	Reads the checksums from the specified SHA1 file and returns it as a dictionary.

	Parameters:
		sha1 (str | Path): Absolute path to the SHA1 file to read

		relative_paths (bool):
			- ***False***: Convert relative paths from SHA1 file to absolute paths
			- *True*:      Use relative paths from the SHA1 file

	Returns:
		dict: Dictionary of the read SHA1 file with
			- key:   File path
			- value: SHA1 checksum

	Raises:
		FileNotFoundError: If the specified SHA1 file does not exist
		ValueError:        If the layout of the SHA1 file does not match the expected format
	"""

	sha1 = Path(sha1)
	base_dir = sha1.parent
	checksums: dict[str, str] = {}

	with sha1.open('r', encoding = 'utf-8') as file:
		for line_number, line in enumerate(file, start = 1):
			# remove unnecessary spaces
			line = line.strip()

			# skip empty lines
			if not line:
				continue

			# parse SHA1 checksum and relative file path from line
			try:
				checksum, file_path = line.split(' *', maxsplit = 1)
			except ValueError as exc:
				raise ValueError(f'Invalid SHA1 file format in line {line_number}: {line!r}') from exc

			# if requested, convert the relative file path to an absolute path
			file_path = Path(file_path) if relative_paths else base_dir / file_path
			checksums[file_path] = checksum
	return checksums
