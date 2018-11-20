from pymongo import UpdateOne
from properties import num_bulk_operations

class DatabaseManager:
	"""
	Class that implements a database manager. It includes functions for a MongoDB database.
	"""
	def update_multiple(self, collection, documents, upsert = False):
		"""
		Perform multiple update operations in bulk.

		:param collection: the collection in which the documents are updated.
		:param documents: the documents to be updated.
		:param upsert: set to True to perform an insert if no documents match the filter.
		"""
		operations = []
		for document in documents:
			operations.append(UpdateOne({"_id": document["_id"]}, {"$set": document}, upsert = upsert))
			if len(operations) == num_bulk_operations:
				collection.bulk_write(operations, ordered = False)
				operations = []
		if len(operations) > 0:
			collection.bulk_write(operations, ordered = False)
