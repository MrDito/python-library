from pathlib import Path
# local modules
from .sort import natural_sort_key

class InvalidFilePathError(Exception):
    """Base class for file path validation errors"""

class PathNotAbsoluteError(InvalidFilePathError):
    """Raised when the path is not absolute"""

class PathIsDirectoryError(InvalidFilePathError):
    """Raised when the path points to a directory"""

class ParentDirectoryNotFoundError(InvalidFilePathError):
    """Raised when the parent directory does not exist"""

class ParentIsNotDirectoryError(InvalidFilePathError):
    """Raised when the parent path is not a directory"""

class PathNotWritableError(InvalidFilePathError):
    """Raised when the file or target directory is not writable"""

def validate_file_path(file_path: str | Path) -> Path:
    """
    Validates the passed file path and returns a corresponding Path object.

    Validation rules:
        - The path must be resolvable.
        - The path must be absolute.
        - The path must point to a file.
        - If the file exists, it must be writable.
        - If the file does not exist, it must be creatable within the parent directory.

    Returns:
        Path: A Path object of the passed file path

    Raises:
        PathNotAbsoluteError
        PathIsDirectoryError
        ParentIsNotDirectoryError
        PathNotWritableError

		if not checksum_file.is_absolute():
			raise Exception(f'Failed to instantiate ChecksumFile object since the specified checksum file path is not an absolute path: {checksum_file}')
		elif not checksum_file.is_file():
			raise Exception(f'Failed to instantiate ChecksumFile object since the specified checksum file path points to no existing file, is invalid or inaccessible: {checksum_file}')
		else:
			self.file = checksum_file
    """

	# resolve home directory and symbolic links
    try:
        path = Path(file_path).expanduser().resolve()
    except RuntimeError as exc:
        raise ValueError(f'Unable to resolve home directory: {file_path}') from exc

    if not path.is_absolute():
        raise ValueError(f'Path is not absolute: {path}')

    if not path.is_file():
        raise ValueError(f'Path does not point to a file: {path}')

    if file_path.exists():
        if not file_path.is_file():
            raise InvalidFilePathError(f'Path does not refer to a regular file: {file_path}')

        try:
            with file_path.open('a'):
                pass
        except OSError as exc:
            raise PathNotWritableError(f'File is not writable: {file_path}') from exc

    else:
        parent_directory = file_path.parent
        created_directories: list[Path] = []

        try:
            created_directories = create_missing_directories(parent_directory)

            with NamedTemporaryFile(dir=parent_directory, delete=True):
                pass

        except OSError as exc:
            raise PathNotWritableError(f'Cannot create target directory or file: {file_path}') from exc

        finally:
            # Remove only directories that were created by this function.
            for directory_path in reversed(created_directories):
                try:
                    directory_path.rmdir()
                except OSError:
                    # Ignore cleanup failures (e.g. directory no longer empty).
                    pass

    return file_path

def create_directory_tree(directory: Path, prefix: str = '') -> str:
	"""
	Creates and returns a graphical tree of the specified directory to visualize the directory structure.

	Parameters:
		directory (Path): Absolute path to the directory for which a directory tree is to be created
		prefix (str):     Prefix resulting from parent directories ('' by default)

	Returns:
		str: Graphical tree of the specified directory
	"""
	# sorted list of all items contained in the directory
	# primary sorting criterion: directories before files
	# secondary sorting criterion: naturally sorted ascending item names
	items = sorted(directory.iterdir(), key = lambda item: [not item.is_dir()] + natural_sort_key(item.name))
	# every item gets a inner pointer '├─', only the last item gets a closing pointer '└─'
	pointers = ['├─ '] * (len(items) - 1) + ['└─ ']
	# tree root is the name of the directory
	folder_tree = '' if prefix else f'{directory.name}\n'
	# for every item, combine the passed prefix with its pointer and name before appending it to the folder tree
	for pointer, item in zip(pointers, items):
		folder_tree += f'{prefix}{pointer}{item.name}\n'
		if item.is_dir():
			# if item is a directory extend the current prefix depending on whether it is the last contained directory or not
			extension = '│  ' if pointer == '├─ ' else '   '
			# create the subtree of the directory using a recursive call
			folder_tree += create_directory_tree(item, prefix + extension)
	return folder_tree

def create_file_list(directory: Path) -> list:
	"""
	Creates and returns a file list of the specified directory.

	Parameters:
		directory (Path): Absolute path to the directory to be indexed

	Returns:
		list: File list of the specified directory
	"""
	return sorted([item.as_posix() for item in directory.rglob('*') if item.is_file()], key = lambda file: natural_sort_key(file))

def create_file_size_dict(directory: Path) -> dict:
	"""
	Creates and returns a file dictionary of the specified directory, representing the directory structure and indicating the size for each file.

	Parameters:
		directory (Path): Absolute path to the directory to be indexed

	Returns:
		dict: File dictionary representing the directory structure and indicating the size for each file
	"""
	file_dict = {}
	if directory.is_dir():
		for item in directory.iterdir():
			if item.is_dir():
				# create file dictionary of the subirectory using a recursive call
				file_dict[item.name] = create_file_size_dict(item)
			else:
				file_dict[item.name] = item.stat().st_size
	return file_dict

def replace_in_file(input_file: Path, mapping: dict, output_file: Path):
	"""
	Replaces all matching substrings in the specified input file by their replacement strings according to the passed mapping table and saves the resulting file to the specified file path.

	Parameters:
		input_file (Path):  Absolute path to the input file to be processed
		mapping (dict):     Mapping table to apply
		output_file (Path): Absolute path where the resulting file should be saved
	"""
	text = input_file.read_text(encoding = 'utf-8')
	for old, new in mapping.items():
		text = text.replace(old, new)
	output_file.write_text(text, encoding = 'utf-8', newline = '\n')