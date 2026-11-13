from sort import natural_sort_key
from str  import is_number

def integer_string_keys_to_integer_keys(dictionary: dict) -> dict:
	"""
	Converts all positive integer string keys of the passed dictionary to integer keys and returns the resulting dictionary.

	Parameters:
		dictionary (dict): Input dictionary
	"""

	# check if key is a positive integer string (thus convertible)
	return {(int(key) if key.isdecimal() else key): dictionary[key] for key in dictionary if isinstance(key, str)}

def get_value(dictionary: dict, *keys, default = None):
	"""
	Returns the nested value of the passed keys in the specified dictionary if available or the replacement value otherwise (if defined else None).

	Parameters:
		dictionary (dict): Input dictionary
		keys:              Dictionary keys identifying the requested nested value
		default:           Value to return if requested nested value is not available (None by default)

	Returns:
		Nested value if available or the replacement value otherwise (if defined else None)
	"""

	if len(keys) > 1:
		if keys[0] in dictionary:
			return get_value(dictionary[keys[0]], *keys[1:], default = default)
		else:
			return default
	elif len(keys) == 1:
		return dictionary.get(keys[0], default)

def merge(dict1: dict, dict2: dict) -> dict:
	"""
	Merges the passed dictionaries and returns it.

	Parameters:
		dict1 (dict): Dictionary 1
		dict2 (dict): Dictionary 2

	Returns:
		dict: Merged dictionary
	"""

	if not dict1:
		mergedDict = dict2.copy()
	elif not dict2:
		mergedDict = dict1.copy()
	else:
		keys = sorted(dict1.keys() | dict2.keys())
		mergedDict = {}
		for key in keys:
			# if key is missing in dict1 but present in dict2
			if key not in dict1 and key in dict2:
				mergedDict[key] = dict2[key]
			# if key is missing in dict2 but present in dict1
			# or values equals for dict1 and dict2
			elif (key in dict1 and key not in dict2) or dict1[key] == dict2[key]:
				mergedDict[key] = dict1[key]
			# if key is present in both dictionaries but differs
			else:
				# if both dictionaries contain values of the same type for this key try to merge them
				if   isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
					mergedDict[key] = merge(dict1[key], dict2[key])
				elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
					mergedDict[key] = dict1[key] + [item for item in dict2[key] if item not in dict1[key]]
				elif isinstance(dict1[key], set)  and  isinstance(dict2[key], set):
					mergedDict[key] = dict1[key].union(dict2[key])
				else:
					raise Exception(f'Unsupported value types for merge of dictionary key "{key}": "{type(dict1[key])}" and "{type(dict2[key])}"')
	return mergedDict

def set_value(dictionary: dict, value, *keys):
	"""
	Sets the nested value according to the passed keys in the specified dictionary.

	Parameters:
		dictionary (dict): Target dictionary
		value:             Nested value to set
		keys:              Dictionary keys identifying the requested nested value to set
	"""

	if len(keys) > 1:
		if keys[0] not in dictionary:
			dictionary[keys[0]] = {}
		set_value(dictionary[keys[0]], value, *keys[1:])
	elif len(keys) == 1:
		dictionary[keys[0]] = value

def sort_by_keys(unsorted_dictionary: dict, reversed: bool = False) -> dict:
	"""
	Sorts the passed dictionary lexicographically by its keys and returns it.

	Parameters:
		unsorted_dictionary (dict): Dictionary to sort
		reversed (bool):
			- ***False***: Ascending sort order
			- *True*:      Descending sort order

	Returns:
		dict: Dictionary sorted lexicographically by its keys
	"""

	# check if all dictionary keys are numeric (float, integers or strings of numeric characters only)
	if all(isinstance(key, (int, float))                   for key in unsorted_dictionary) \
	or all(isinstance(key, str) and is_number(key) for key in unsorted_dictionary):
		# apply float sorting (13 < 123 < '123.4' < 123.45) instead of string sorting ('123' < '13')
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: int(item[0]), reverse = reversed))
	elif all(isinstance(key, str) for key in unsorted_dictionary):
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: item[0].lower(), reverse = reversed))
	else:
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), reverse = reversed))
	return sorted_dictionary

def sort_by_keys_natural(unsorted_dictionary: dict, reversed: bool = False) -> dict:
	"""
	Sorts the passed dictionary naturally by its keys and returns it.

	Parameters:
		unsorted_dictionary (dict): Dictionary to sort
		reversed (bool):
			- ***False***: Ascending sort order
		    - *True*:      Descending sort order

	Returns:
		dict: Dictionary sorted naturally by its keys
	"""

	# check if all dictionary keys are numeric (float, integers or strings of numeric characters only)
	if all(isinstance(key, (int, float))                   for key in unsorted_dictionary) \
	or all(isinstance(key, str) and is_number(key) for key in unsorted_dictionary):
		# apply float sorting (13 < 123 < '123.4' < 123.45) instead of string sorting ('123' < '13')
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: int(item[0]), reverse = reversed))
	elif all(isinstance(key, str) for key in unsorted_dictionary):
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: natural_sort_key(item[0]), reverse = reversed))
	else:
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: natural_sort_key(str(item[0])), reverse = reversed))
	return sorted_dictionary

def sort_by_key_values(unsorted_dictionary: dict, key: str, reversed: bool = False) -> dict:
	"""
	Sorts the passed dictionary lexicographically by its values of the passed key and returns it.

	Parameters:
		unsorted_dictionary (dict): Dictionary to sort
		key (str):                  Dictionary key of the value to sort by
		reversed (bool):
			- ***False***: Ascending sort order
		    - *True*:      Descending sort order

	Returns:
		dict: Dictionary sorted lexicographically by its key values
	"""

	# check if all dictionary key values are numeric (float, integers or strings of numeric characters only)
	if all(isinstance(value[key], (int, float)) or is_number(value[key]) for value in unsorted_dictionary.values()):
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: float(item[1][key]), reverse = reversed))
	elif all(isinstance(value[key], str) for value in unsorted_dictionary.values()):
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: item[1][key].lower(), reverse = reversed))
	else:
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: item[1][key], reverse = reversed))
	return sorted_dictionary

def sort_by_values(unsorted_dictionary: dict, reversed: bool = False) -> dict:
	"""
	Sorts the passed dictionary lexicographically by its values and returns it.

	Parameters:
		unsorted_dictionary (dict): Dictionary to sort
		reversed (bool):
			- ***False***: Ascending sort order
		    - *True*:      Descending sort order

	Returns:
		dict: Dictionary sorted lexicographically by its values
	"""

	# check if all dictionary values are numeric (float, integers or strings of numeric characters only)
	if all(isinstance(value, (int, float))                     for value in unsorted_dictionary.values()) \
	or all(isinstance(value, str) and is_number(value) for value in unsorted_dictionary.values()):
		# apply float sorting (13 < 123 < '123.4' < 123.45) instead of string sorting ('123' < '13')
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: float(item[1]), reverse = reversed))
	elif all(isinstance(value, str) for value in unsorted_dictionary.values()):
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: item[1].lower(), reverse = reversed))
	else:
		sorted_dictionary = dict(sorted(unsorted_dictionary.items(), key = lambda item: item[1], reverse = reversed))
	return sorted_dictionary