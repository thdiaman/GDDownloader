import json
import codecs

class FileManager:

	def read_json_from_file(self, filename):
		"""
		Reads a file into a JSON object.

		:param filename: the filename of the file to be read.
		:returns: the JSON object that is contained in the file.
		"""
		with codecs.open(filename, 'r') as infile:
			data = json.load(infile)
		return data

	def write_json_to_file(self, filename, data):
		"""
		Writes a JSON object to file.
		
		:param filename: the filename of the file to be written.
		:param data: the JSON data to be written to file.
		"""
		with codecs.open(filename, 'w', 'utf-8') as outfile:
			json.dump(data, fp = outfile, sort_keys = True, indent = 3, ensure_ascii = False)

