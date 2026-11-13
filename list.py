def chunks(list: list, size: int):
	"""
	Generator yielding evently-sized chunks.

	Parameters:
		list (list): List of items to split into chunks
		size (int):  Size of each chunk
	"""

	for i in range(0, len(list), size):
		yield list[i:i + size]