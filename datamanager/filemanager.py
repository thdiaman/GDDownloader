import os
import json
import codecs

class FileManager:
	"""
	Class that implements a file manager. It includes functions for creating, reading, and
	writing from and to folders and JSON files. Note that all data are read and written in
	UTF-8 encoding.
	"""
	def create_folder_if_it_does_not_exist(self, foldername):
		"""
		Creates a folder in the filesystem if it does not already exist.

		:param foldername: the path to the folder to be created.
		"""
		if not os.path.exists(foldername):
			os.makedirs(foldername)

	def read_json_from_file_if_it_exists(self, filename):
		"""
		Reads a file into a JSON object if the file exists.

		:param filename: the filename of the file to be read.
		:returns: the JSON object of the file if the file exists, or an empty object otherwise.
		"""
		return self.read_json_from_file(filename) if os.path.exists(filename) else {}

	def read_jsons_from_folder(self, foldername, element_id):
		"""
		Reads the files of a folder into a dict of JSON objects. Given that a file
		has a JSON object e.g. element, the returned dict has as key the element_id
		field of the element (element[element_id]) and as value the element itself.

		:param foldername: the path to the folder from where JSON objects are read.
		:param element_id: the JSON key to be used as a key to the returned dict.
		:returns: a dict containing the JSON objects that are contained in the folder.
		"""
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
		with codecs.open(filename, 'r', 'utf-8') as infile:
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

