import os
import re
import string
import math
import random
from newsplease import NewsPlease

DATA_DIR = './'
target_names = ['right', 'left']
 
def get_data(DATA_DIR):
	data = []
	target = []
	# left
	left_files = os.listdir(os.path.join(DATA_DIR, 'left'))
	for left_file in left_files:
		if left_file == '.DS_Store':
			continue
		with open(os.path.join(DATA_DIR, 'left', left_file), encoding="latin-1") as f:
			data.append(f.read())
	
		target.append(1)

	# right
	right_files = os.listdir(os.path.join(DATA_DIR, 'right'))
	for right_file in right_files:
		if right_file == '.DS_Store':
			continue
		with open(os.path.join(DATA_DIR, 'right', right_file), encoding="latin-1") as f:
			data.append(f.read())
	
		target.append(0)

	return data, target

def shuffle_data(data, target):
	dict_data = {}
	for i in range(len(data)):
		dict_data[data[i]] = target[i]

	to_be_shuffled = list(dict_data.items())
	random.shuffle(to_be_shuffled)
	shuffled_dict = dict(to_be_shuffled)
	return map(list, (shuffled_dict.keys(), shuffled_dict.values()))

class leftDetector(object):
	"""Implementation of Naive Bayes for binary classification"""
	def clean(self, s):
		translator = str.maketrans("", "", string.punctuation)
		return s.translate(translator)
 
	def tokenize(self, text):
		text = self.clean(text).lower()
		return re.split("\W+", text)
 
	def get_word_counts(self, words):
		word_counts = {}
		for word in words:
			word_counts[word] = word_counts.get(word, 0.0) + 1.0
		return word_counts

	def fit(self, X, Y):
		self.num_messages = {}
		self.log_class_priors = {}
		self.word_counts = {}
		self.vocab = set()

		n = len(X)
		self.num_messages['left'] = sum(1 for label in Y if label == 1)
		self.num_messages['right'] = sum(1 for label in Y if label == 0)
		self.log_class_priors['left'] = math.log(self.num_messages['left'] / n)
		self.log_class_priors['right'] = math.log(self.num_messages['right'] / n)
		self.word_counts['left'] = {}
		self.word_counts['right'] = {}
	 
		for x, y in zip(X, Y):
			c = 'left' if y == 1 else 'right'
			counts = self.get_word_counts(self.tokenize(x))
			for word, count in counts.items():
				if word not in self.vocab:
					self.vocab.add(word)
				if word not in self.word_counts[c]:
					self.word_counts[c][word] = 0.0
	 
				self.word_counts[c][word] += count

		# print(self.vocab)

	def predict(self, X):
		result = []
		for x in X:
			counts = self.get_word_counts(self.tokenize(x))
			left_score = 0
			right_score = 0
			for word, _ in counts.items():
				if word not in self.vocab: continue
				
				# add Laplace smoothing
				log_w_given_left = math.log( (self.word_counts['left'].get(word, 0.0) + 1) / (self.num_messages['left'] + len(self.vocab)) )
				log_w_given_right = math.log( (self.word_counts['right'].get(word, 0.0) + 1) / (self.num_messages['right'] + len(self.vocab)) )
	 
				left_score += log_w_given_left
				right_score += log_w_given_right
	 
			left_score += self.log_class_priors['left']
			right_score += self.log_class_priors['right']

			if left_score > right_score:
				accuracy = abs((abs(left_score) - abs(right_score)) / (left_score)) * 100
				result.append((1, accuracy))
			else:
				# print('Accuracy:', right_score / (left_score + right_score))
				accuracy = abs((abs(left_score) - abs(right_score)) / (right_score)) * 100
				result.append((0, accuracy))
		return result

def get_prediction(article_text):
	X, y = get_data(DATA_DIR)
	X, y = shuffle_data(X, y)
	# test_articles = get_test_data(TEST_DIR)
	MNB = leftDetector()

	MNB.fit(X[2000:], y[2000:])
 	
	pred, accuracy = MNB.predict([article_text])[0]
	# print(article.title)
	print('Liberal' if pred else 'Conservative')
	print('Confidence: ', accuracy) # take this line out if you don't want the confidence score
	# true = test_labels
 
	# accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i]) / float(len(pred))
	# print("{0:.4f}".format(accuracy))

get_prediction("Donald Trump is mainstream media impeachment trial")