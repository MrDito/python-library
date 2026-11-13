import re
from pathlib import Path

def natural_sort_key(string: str) -> list[int | str]:
	"""
	Key function for natural sorting alphanumerical strings.

	Parameters:
		string (str): String for which a key value should be determined

	Returns:
		list[int | str]: Key value for sorting by natural sort order
	"""

	# returns the list of substrings that results by splitting the input string at every integer
	# additionally all integer substrings are converted to integers
	# example: 'foo12bar3' -> ['foo', 12, 'bar', 3, '']
	return [int(substring) if substring.isdigit() else substring.lower() for substring in re.split(r'(\d+)', string)]

def natural_path_sort_key(path: str | Path) -> tuple:
	"""
	Key function for sorting paths primarily by path depth and secondarily by natural sorting.

	Parameters:
		path (str | Path): Path for which a key value should be determined

	Returns:
		tuple: Key value for sorting primarily by path depth and secondarily by natural sort order
	"""

	p = Path(path)
	path_depth = len(p.parts)   # count of segments in path
	return (path_depth, natural_sort_key(str(p)))