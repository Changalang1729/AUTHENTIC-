from numpy import dot
from numpy.linalg import norm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from collections import Counter
import sys

analyser = SentimentIntensityAnalyzer()
SCORE = 0.01

def score_sentence(sentence):
    score = analyser.polarity_scores(sentence)
    # print("{:-<40} {}".format(sentence, str(score)))
    return Counter(score)

def score_passage(passage):
	split_passage = sent_tokenize(passage)
	sentence_array = [s.strip(' \n') for s in split_passage]
	passage_length = len(''.join(s for s in sentence_array))
	total_score = Counter()
	pos = neg = 0
	HL = len(sentence_array) // 2

	for i, sentence in enumerate(sentence_array):
		sentence_score = score_sentence(sentence)
		compound_score = sentence_score.get('compound', 0)
		multiplier = (SCORE // 2) * ((i - HL) ** 2) + SCORE
		if compound_score > 0:
			# print('pos', sentence, multiplier)
			total_score += sentence_score
			pos += compound_score * multiplier
		elif compound_score < 0:
			# print('neg', sentence, multiplier)
			total_score += sentence_score
			neg -= compound_score * multiplier

	# print(total_score)
	# print (('pos', pos) if pos > neg else ('neg', -neg))
	return total_score
	# return ('pos', pos) if pos > neg else ('neg', -neg)

def convert_to_vector(score):
	# order = ['neu', 'neg', 'pos', 'compound']
	compound_score = score['compound']
	compound_converted = None

	if abs(compound_score) < 0.75:
		compound_converted = 0
	elif compound_score > 0.75:
		compound_converted = 1
	elif compound_score < -0.75:
		compound_converted = -1

	neg_pos = max(score['neg'], score['pos']) * (-1 if score['neg'] > score['pos'] else 1)

	return [compound_converted] + [neg_pos]

def get_similarity(passage1, passage2):
	a_score = convert_to_vector(score_passage(article1))
	b_score = convert_to_vector(score_passage(article2))

	cos_sim = dot(a_score, b_score)/ (norm(a_score) * norm(b_score))

	return cos_sim

if __name__ ==  '__main__':
	args = sys.argv

	if len(args) != 3:
		print('Error: Need 2 file arguments to get similarity.')
		exit(0)

	fin1 = open(args[1], 'r')
	fin2 = open(args[2], 'r')

	article1 = fin1.read()
	article2 = fin2.read()

	print(get_similarity(article1, article2))