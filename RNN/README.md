In this file, we will see the RNN, the pre_processor to clean up the data and the tf vectors, the glove_similarity to compare the corpus to current articles, and the webscraper to generate the dataset

1) pre_processor (jupyter notebook): cleans up the whole file to lower the dataset and make sure that the dataset has no variable length
2) fixedRNN (jupyter notebook): generates the RNN from an input corpus, or multiple is possible as well
3) glove_similarity (jupyter notebook): utilizes the cosin similarity + glove vectorization from google in order to compare similarity in sentiment
4) webscraper (jupyter notebook): utilizes the library Newspaper to get articles from various sites.


Some obvious deficiencies/steps to work on next: 

1) Although all activation functions were tried, we have no statistical evidence that one works better than another. We merely used the one that seemed best on a smaller dataset. 
2) It's difficult to assess which specific dataset has the most contribution for the next dataset
3) It's impossible to measure how language has changed over time with our analysis methods at the moment
4) Glove Similarity may not be the best method to measure similar sentiments. 
