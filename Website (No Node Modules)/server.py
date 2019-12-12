from flask import Flask, jsonify
from newspaper import Article
from flask import request
import re
import sqlite3
import importlib
import sys
import os
import pickle
from sentiment import *

app = Flask(__name__)

# takes and article from a url and evaluates it
def evaluateArticle(url):    
    # connect to table
    conn = sqlite3.connect("pastResults.db", check_same_thread=False)
    cur = conn.cursor()

    # check if the url already exists in the table
    cur.execute("SELECT * FROM ArticleInfo WHERE Link = ?", (str(url),))
    exists = cur.fetchall()

    # if it exists return it
    if len(exists) != 0:

        existingInfo = exists

        # close the table
        cur.close()
        conn.close()

        # return as a json
        return {
            "article": {
                "company": existingInfo[0][0],
                "title": existingInfo[0][1],
                "authors": existingInfo[0][2],
                "text": existingInfo[0][4],
                "bias": {
                    "conservative": float(existingInfo[0][5]),
                    "liberal": float(existingInfo[0][6])
                },
                "url": existingInfo[0][3]
            }
        }

    # strip the url of everything to get the source name
    company = url.strip('https://').strip('www.').strip()
    company = re.sub('\..*$', '', company)

    # get the article and parse it
    article = Article(url)
    article.download()
    article.parse()

    # get the info from the article
    title = article.title
    authors = article.authors
    text = article.text

    # do the sentiment anaylysis
    with open(os.getcwd()  + '/' + "right_corpus.txt", 'r') as file:
        right_corpus = file.read()

    with open(os.getcwd()  + '/' + "left_corpus.txt", 'r') as file:
        left_corpus = file.read()

    with open("glove_model.txt", "rb") as cachedModel:
        model = pickle.load(cachedModel)

    conservative = cosine_distance_wordembedding_method(model, text, right_corpus)
    liberal = cosine_distance_wordembedding_method(model, text, left_corpus)
    conservative = conservative
    liberal = liberal

    # store it in the database
    cur.execute("INSERT INTO ArticleInfo (Company, Title, Authors, Link, Text, Conservative, Liberal) \
        VALUES (?, ?, ?, ?, ?, ?, ?)", (str(company), str(title), str(authors), str(url), str(text), float(conservative), float(liberal)))
    
    # commit to table and close
    conn.commit()
    cur.close()
    conn.close()

    # return as a json
    return {
                "article": {
                    "company": company,
                    "title": title,
                    "authors": authors,
                    "text": text,
                    "bias": {
                        "conservative": conservative,
                        "liberal": liberal
                    },
                    "url": url
                }
            }

# return all of the past results
@app.route('/results', methods=['GET'])
def returnResults():
    # connect to table
    conn = sqlite3.connect("pastResults.db", check_same_thread=False)
    cur = conn.cursor()

    # select everything and store it
    cur.execute("SELECT * FROM ArticleInfo")
    pastResults = cur.fetchall()
    returnResults = {}

    # go through the past results and label them to return
    for i in range(0, len(pastResults)):    
        results = { i: {
                "article": {
                    "company": pastResults[i][0],
                    "title": pastResults[i][1],
                    "authors": pastResults[i][2],
                    "text": pastResults[i][4],
                    "bias": {
                        "conservative": pastResults[i][5],
                        "liberal": pastResults[i][6]
                    },
                    "url": pastResults[i][3]
                }
            }
        }
        returnResults.update(results)

    # close connection and return results
    cur.close()
    conn.close()
    resultsJson = jsonify(returnResults)
    resultsJson.headers.add('Access-Control-Allow-Origin', '*')
    return resultsJson


# return the informatino from an article
@app.route('/article', methods=['GET'])
def articleInfo():
    article = request.args.get('article', type=str)
    articleJson = jsonify(evaluateArticle(article))
    articleJson.headers.add('Access-Control-Allow-Origin', '*')
    return articleJson



if __name__ == '__main__':
    app.run(debug=True)