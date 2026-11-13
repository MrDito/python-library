from pathlib import Path

def is_number(string: str) -> bool:
	"""
	Checks if a passed string represents a number that can be interpreted as float or integer.

	Parameters:
		string (str): String to check whether it represents a number (float or integer)

	Returns:
		bool: True if passed string represents a number (float or integer), otherwise False
	"""

	try:
		float(string)
		return True
	except (TypeError, ValueError):
		return False

def replace_by_mapping(file: Path, mapping_tsv: Path) -> None:
	"""
	Replaces all substrings in the specified file using the passed TSV mapping table.

	Parameters:
		file (Path):        Absolute path to the file to be processed
		mapping_tsv (Path): Absolute path to the TSV mapping table file
	"""

	if not file.is_absolute():
		raise Exception(f'Failed to read input file since the specified file path is not an absolute path: {file}')
	elif not file.is_file():
		raise Exception(f'Failed to read input file since the specified file path points to no existing file, is invalid or inaccessible: {file}')
	if not mapping_tsv.is_absolute():
		raise Exception(f'Failed to read TSV mapping table since the specified file path is not an absolute path: {mapping_tsv}')
	elif not mapping_tsv.is_file():
		raise Exception(f'Failed to read TSV mapping table since the specified file path points to no existing file, is invalid or inaccessible: {mapping_tsv}')
	elif not mapping_tsv.suffix != '.tsv':
		raise Exception(f'Failed to read TSV mapping table since the specified file is no tabulator separated values (TSV) file: {mapping_tsv}')
	else:
		text          =        file.read_text(encoding = 'utf-8')
		mapping_table = mapping_tsv.read_text(encoding = 'utf-8').split('\n')
		for entry in mapping_table:
			mapping = entry.split('\t')
			text = text.replace(mapping[0], mapping[1])
		file.write_text(text, encoding = 'utf-8')

def replace_invalid_filename_chars(filename: str) -> str:
	"""
	Replaces all character being invalid for Windows filenames by valid replacements and returns it.

	Parameters:
		filename (str): Windows filename to transform (must not contain path information)

	Returns:
		str: Valid Windows filename
	"""

	unicode_table = {
			34:  65282, # " > ＂
			42:  65290, # * > ＊
			47:  10744, # / > ⧸
			58:  65306, # : > ：
			60:  65308, # < > ＜
			62:  65310, # > > ＞
			63:  65311, # ? > ？
			92:  10745, # \ > ⧹
			124: 65372, # | > ｜
		}
	return filename.translate(unicode_table).replace('\t', ' - ')

def reverse_invalid_filename_chars(filename: str) -> str:
	"""
	Reverses replacement of all characters being invalid for Windows filenames and returns original filename.

	Parameters:
		filename (str): Windows filename including replacement characters (must not contain path information)

	Returns:
		str: Original filename
	"""

	unicode_table = {
			65282:  34, # ＂ > "
			65290:  42, # ＊ > *
			10744:  47, # ⧸ > /
			65306:  58, # ： > :
			65308:  60, # ＜ > <
			65310:  62, # ＞ > >
			65311:  63, # ？ > ?
			10745:  92, # ⧹ > \
			65372: 124, # ｜ > |
		}
	return filename.translate(unicode_table).replace(' - ', '\t')