from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from collections import Counter

analyser = SentimentIntensityAnalyzer()

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

	for sentence in sentence_array:
		sentence_score = score_sentence(sentence)
		compound_score = sentence_score.get('compound', 0)
		
		if compound_score > 0:
			pos += compound_score
		elif compound_score < 0:
			neg -= compound_score

	return 'pos' if pos > neg else 'neg'


fin = open('passage.in', 'r')
article = fin.read()

print(score_passage(article))
