import json
import logging
from pathlib import Path
# extern modules
import requests

session = requests.Session()
session.headers = {'User-Agent': 'Mozilla', 'Accept-Language': 'en-US,en;q=1.0'}

def read_json_file(json_file_path: Path) -> dict:
	"""
	Reads the specified JSON file and returns it as a dictionary.

	Parameters:
		json_file_path (Path): Absolute path to the JSON file to read

	Returns:
		dict: Dictionary of the read JSON file
	"""

	data = {}
	with open(json_file_path, 'r', encoding = 'utf-8') as jsonFile:
		# deserialize json file and read into a dictionary
		data = json.load(jsonFile)
		logging.info(f'Successfully read JSON file {json_file_path}.')
	return data

def safe_read_json_file(json_file_path: Path) -> dict:
	"""
	Reads the specified JSON file and returns it as a dictionary.

	Parameters:
		json_file_path (Path): Absolute path to the JSON file to read

	Returns:
		dict: Dictionary of the read JSON file
	"""

	data = {}
	try:
		with open(json_file_path, 'r', encoding = 'utf-8') as jsonFile:
			try:
				# deserialize json file and read into a dictionary
				data = json.load(jsonFile)
				logging.info(f'Successfully read JSON file {json_file_path}.')
			except json.decoder.JSONDecodeError:
				logging.warning('Cannot read JSON file since being empty or invalid. Continues with an empty dictionary.')
	except FileNotFoundError:
		logging.warning('Cannot read JSON file since being file not exists. Continues with an empty dictionary.')
	return data

def write_json_file(data: dict, json_file_path: Path):
	"""
	Writes the passed dictionary to the specified JSON file.

	Parameters:
		data (dict):           Dictionary to write
		json_file_path (Path): Absolute path to the destination JSON file
	"""

	# create directory if not existing yet
	json_file_path.parent.mkdir(parents = True, exist_ok = True)
	# serialize dictionary and write to the specified json file
	with open(json_file_path, 'w', encoding = 'utf-8') as jsonFile:
		json.dump(data, jsonFile, ensure_ascii = False, indent = '\t')
		logging.info(f'Successfully writed data to JSON file {json_file_path}.')

def request(url: str, abort_on_error: bool = True) -> dict:
	"""
	Makes a HTTP GET request and returns the received parsed JSON dictionary.

	Parameters:
		url (str):             Requested URL
		abort_on_error (bool):
		    - *False*:    In case of request failure (status code != 200) an error is logged and function returns an empty string
			- ***True***: In case of request failure (status code != 200) a ConnectionError exception is raised

	Returns:
		dict: Dictionary of the received parsed JSON data or an empty dictionary in case of request failure (if abort_on_error == False).

	Raises:
		ConnectionError: If HTTP GET request fails (if abort_on_error == True)
	"""

	response = session.get(url)
	data = {}
	if response.status_code == 200:
		logging.debug(f'Succesfully fetched web API JSON data for {url}.')
		data = response.json()
	elif abort_on_error:
		raise ConnectionError(f'Web API JSON request for {url} failed with status code {response.status_code}.')
	else:
		logging.warning(f'Web API JSON request for {url} failed with status code {response.status_code}. Continues with an empty response.')
	return data