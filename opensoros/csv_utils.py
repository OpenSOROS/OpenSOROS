from datetime import datetime
import csv
import numpy as np
import time
import sys
import os
import os.path


DATA_DIR = "data"
SIMILARITY = "_similarity_matrix"
USER_PARTY_TWEETS = "_user_party_tweets"


DATA_HEADERS = ["message", "id", "date"]
PLOT_HEADERS = ['x', 'y', 'label']


def comments_to_csv(name, id, comments,type):
	"""
	Saves all the comments from a given source into a csv file.

		Args:
			name(str) - the name of the file to save the data to
			id(str) - the name of the data source (i.e facebook page name, twitter handle)
			comments - the data to save; comments are expected to be in the format of a list of tuples (text (str) time_created (datetime))

	"""

	if not os.path.exists(os.path.join(os.getcwd(),DATA_DIR)):
		os.makedirs(os.path.join(os.getcwd(),DATA_DIR))

	file_dir = os.path.join(os.getcwd(), DATA_DIR, name + '.csv')

	# If no such file exists, create a new file

	if not os.path.exists(file_dir):
		with open(file_dir, 'w') as f:
			writer = csv.writer(f)
			writer.writerow(DATA_HEADERS)
			for comment in comments:
				try:
					writer.writerow([comment[0], id+type, comment[1].strftime('%c')])
				except Exception as e:
					pass

	# Otherwise append to the end of the old file (do not overwrite)
	else:
		with open(file_dir, 'a') as f:
			writer = csv.writer(f)
			for comment in comments:
				try:
					writer.writerow([comment[0], id+type, comment[1].strftime('%c')])
				except Exception as e:
					pass


def plot_to_csv(name, matrix, labels):
	"""
	Save the details of the dimensionality reduction vis into a csv file.

	Args:
		name (str): the name of the csv file to save the data to
		matrix (np.array): the matrix containing the x- and y- coordinates of each point in the plot
		labels (str[]): the labels for each point
	"""

	if not os.path.exists(os.path.join(os.getcwd(),DATA_DIR)):
		os.makedirs(os.path.join(os.getcwd(),DATA_DIR))

	file_dir = os.path.join(os.getcwd(), DATA_DIR, name + '.csv')

	# write csv --

	with open(file_dir, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(PLOT_HEADERS)
		for i in range(0,len(labels)):
			writer.writerow([str(matrix[i, 0]), str(matrix[i, 1]), labels[i]])


def similarity_to_csv(name, matrix, labels):
	"""
	Save similarity matrix of the vectors into a csv file.

	Args:
		name (str): the name of the csv file to save the data to
		matrix (np.array): the similarity matrix where matrix[i,j] contains the similarity score (0-1) between vectors i and j
		labels (str[]): the labels for each vector
	"""
	if not os.path.exists(os.path.join(os.getcwd(),DATA_DIR)):
		os.makedirs(os.path.join(os.getcwd(),DATA_DIR))

	file_dir = os.path.join(os.getcwd(), DATA_DIR, name + SIMILARITY + '.csv')

	# write csv --

	with open(file_dir, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(labels)
		for i in range(0,len(labels)):
			writer.writerow([matrix[i,j] for j in range(len(labels))])


def similarity_from_csv(name):
    """
    Loads similarity matrix written by similarity_to_csv

	Args:
		name (str): the name of the csv file to load the data from
    Returns:
		matrix (np.array): the similarity matrix where matrix[i,j] contains the similarity score (0-1) between vectors i and j
		labels (str[]): the labels for each vector
    """
    file_dir = os.path.join(os.getcwd(), DATA_DIR, name + SIMILARITY + '.csv')

    # read csv --

    matrix = []
    with open(file_dir, 'r') as f:
        reader = csv.reader(f)
        labels = None
        for row in reader:
            if labels is None:
                labels = row
            else:
                matrix.append([float(d) for d in row])
    return np.array(matrix), labels


def parties_from_csv(name):
    """
    Loads User -> Party mapping from csv

	Args:
		name (str): the name of the csv file to load the data from
    Returns:
        parties (Dictionary): Mapping of names (key) to parties (value).
    """
    file_dir = os.path.join(os.getcwd(), DATA_DIR, name + USER_PARTY_TWEETS + '.csv')

    # read csv --

    parties = {}
    with open(file_dir, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parties[row['user']] = row['affiliation']
    return parties


def parse_csv(name, startrow=0):

	file_dir = os.path.join(os.getcwd(), DATA_DIR, name + ".csv")

	args = {}

	idx = 0

	with open(file_dir, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if idx >= startrow:
				type = row[0]
				if type not in args:
					args[type] = [row[1]]
				else:
					args[type].append(row[1])
			idx += 1

	results = []
	for key in args:
		results.append("--" + key)
		results += args[key]

	return results

def read_data_from_csv(name, startrow = 1):

	file_dir = os.path.join(os.getcwd(), DATA_DIR, name + ".csv")

	names = []
	comments = []
	current_comment = ""
	current_name = ""
	idx = 0

	with open(file_dir, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if idx >= startrow and len(row) > 0:
				name = row[1]
				if name != current_name:
					if current_name != "":
						names.append(current_name)
						comments.append([current_comment])
						print(current_name + " done")
					current_name = name
					current_comment = ""
				current_comment += (" " + row[0])
			idx += 1

	print("Done.")

	return names, comments
