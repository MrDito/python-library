import logging
# extern modules
import requests

session = requests.Session()
session.headers = {'User-Agent': 'Mozilla', 'Accept-Language': 'en-US,en;q=1.0'}

def request(url: str, abort_on_error: bool = True) -> str:
	"""
	Makes a HTTP GET request and returns the received data.

	Parameters:
		url (str):             Requested URL
		abort_on_error (bool):
		    - *False*:    In case of request failure (status code != 200) an error is logged and function returns an empty string
			- ***True***: In case of request failure (status code != 200) a ConnectionError exception is raised

	Returns:
		str: String of the received data or an empty string in case of request failure (if abort_on_error == False).

	Raises:
		ConnectionError: If abort_on_error == True and a HTTP GET request fails
	"""

	data = ''
	retries = 2
	response = session.get(url)
	# retry web HTML request if server reports a gateway timeout
	while response.status_code == 504 and retries > 0:
		logging.debug(f'Web HTML request for {url} failed with status code {response.status_code}.')
		retries -= 1
		response = session.get(url)
	if response.status_code == 200:
		logging.debug('Succesfully fetched web API data.')
		data = response.text
	elif abort_on_error:
		logging.warning(f'Web HTML request for {url} failed with status code {response.status_code}. Continues with an empty response.')
		raise ConnectionError(f'Web HTML request for {url} failed with status code {response.status_code}.')
	else:
		logging.debug(f'Web HTML request for {url} failed with status code {response.status_code}. Continues with an empty response.')
	return data