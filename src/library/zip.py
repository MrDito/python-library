import zipfile
from pathlib import Path

def create_ZIP_archive(filename: str, input_path: Path, output_path: Path) -> None:
	"""
	Creates a ZIP archive of all files in the specified input directory (including their directory structure) and saves it to the output directory.

	Parameters:
		filename (str):     Filename of the ZIP file to create (excluding file extension)
		input_path (Path):  Path of the input directory containing the data to archive
		output_path (Path): Path of the output directory the resulting ZIP file shall be saved to
	"""

	if not input_path.exists():
		raise FileNotFoundError(f'Cannot create ZIP archive of the directory content {input_path} as the specified directory does not exist.')
	if not output_path.exists():
		output_path.mkdir(parents = True)
	with zipfile.ZipFile(Path(output_path, f'{filename}.zip'), 'w') as zip:
		for item in input_path.rglob('*'):
			if item.is_file():
				zip.write(item, item.relative_to(input_path))