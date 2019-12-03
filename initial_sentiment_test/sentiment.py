from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

analyser = SentimentIntensityAnalyzer()

def score_sentence(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))
    return Counter(score)

def score_passage(passage):
	sentence_array = [s.strip(' \n') for s in passage.split('.')]
	total_score = 0
	for sentence in sentence_array:
		total_score += score_sentence(sentence)
	print(total_score)
	return total_score

fin = open('passage.in', 'r')
article = fin.read()


# print(article)
score_passage(article)
