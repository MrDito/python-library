import logging
from csv     import reader
from pathlib import Path

def read_tsv_file(tsv: Path) -> list:
	"""
	Reads the passed TSV file into a list of records and returns it.

	Parameters:
		tsv (Path): Absolute path to the TSV file to read

	Returns:
		list: List of records
	"""

	records = []
	with open(tsv, 'r', encoding = 'utf-8') as file:
		records = list(reader(file, delimiter = '\t', quotechar = '"'))
		logging.info(f'Successfully read TSV file {tsv}.')
	return records

def read_mapping_table(tsv: Path) -> dict:
	"""
	Reads the mapping table from the passed TSV file into a dictionary and returns it.

	Parameters:
		tsv (Path): Absolute path to the TSV mapping table file to read

	Returns:
		dict: Mapping table
	"""

	mapping_table = {}
	with open(tsv, 'r', encoding = 'utf-8') as file:
		records = list(reader(file, delimiter = '\t', quotechar = '"'))
		if all(len(record) == 2 for record in records):
			mapping_table = {record[0]: record[1] for record in records}
			logging.info(f'Successfully read TSV mapping table file {tsv}.')
	return mapping_table