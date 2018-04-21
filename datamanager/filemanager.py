import os
import json
import codecs

class FileManager:

	def create_folder_if_it_does_not_exist(self, foldername):
		if not os.path.exists(foldername):
			os.makedirs(foldername)

	def read_json_from_file_if_it_exists(self, filename):
		return self.read_json_from_file(filename) if os.path.exists(filename) else {}

	def read_jsons_from_folder(self, foldername, element_id):
		data = {}
		for filename in os.listdir(foldername):
			element = self.read_json_from_file(os.path.join(foldername, filename))
			data[element[element_id]] = element
		return data

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

