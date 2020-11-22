import pandas as pd
import re
import nltk
from pyspark.sql import SparkSession
train = pd.read_csv("netflix_titles.tsv", header=0,  delimiter="\t", quoting=3)
#train = pd.read_csv("netflix_titles.csv", header=0,  delimiter="\t", quoting=3)
#print(train.id)




print(train.columns.values)
print(train["description"][0])
# Import BeautifulSoup into your workspace
from bs4 import BeautifulSoup
# Initialize the BeautifulSoup object on a single movie review
example1 = BeautifulSoup(train["description"][0] , "html.parser")
# Print the raw review and then the output of get_text(), for
# comparison
#print(train["review"][0])
#print(example1.get_text())
letters_only = re.sub("[^a-zA-Z]", " ", example1.get_text() ) 
# The text to search
#print(letters_only)
lower_case = letters_only.lower() # Convert to lower case
words = lower_case.split() # Split into words
#print(words)
# Download punkt english tokenizer
nltk.download('punkt')
# first tokenize by sentence, then by word
nltk_words = [word for sent in nltk.sent_tokenize(lower_case)
for word in nltk.word_tokenize(sent)]
# Download stop words
nltk.download('stopwords')
from nltk.corpus import stopwords # Import the stop word list
#print(stopwords.words("english"))
# Remove stop words from "words" using list comprehension
filtered_words = [w for w in words if not w in
stopwords.words("english")]
#print(filtered_words)
# load nltk's SnowballStemmer
from nltk.stem.snowball import SnowballStemmer
# Stemming is the process of breaking a word down into its root.
stemmer = SnowballStemmer('english')
# In Python, searching a set is much faster than searching
# a list, so convert the stop words to a set
stops = set(stopwords.words("english"))
def review_to_words( raw_description ):
 # Function to convert a raw review to a string of words
 # The input is a single string (a raw movie review), and
 # the output is a single string (a pre-processed movie
 # review)
 #
 # 1. Remove HTML

 review_text = BeautifulSoup(raw_description, "html.parser").get_text() 
 #
 # 2. Remove non-letters
 letters_only = re.sub("[^a-zA-Z]", " ", review_text)
 #
 # 3. Convert to lower case, split into individual words
 words = letters_only.lower().split()
 #
 # 4. Remove stop words
 meaningful_words = [w for w in words if not w in stops]
 #
 # 5. Stem words
 stemmed_meaningful_words = [stemmer.stem(w) for w in meaningful_words]
 #
 # 6. Join the words back into one string separated by space,
 # and return the result.
 return( " ".join( stemmed_meaningful_words )) 
clean_review = review_to_words( train["description"][0] )
print(clean_review)

# Get the number of reviews based on the dataframe column size
num_reviews = train["description"].size
print(num_reviews)
# Initialize an empty list to hold the clean reviews
clean_train_reviews = []
#clean_train_reviews.append( review_to_words(train["description"][0] ) )
#clean_train_reviews.append( review_to_words(train["description"][1] ) )
print("works")
# Loop over each review; create an index i that goes from 0 to
# the length of the movie review list
for i in range( 2000 ):
#for i in range( 0, 500 ):
 # Call our function for each one, and add the result to the
 # list of clean reviews
   clean_train_reviews.append( review_to_words(train["description"][i] ) )
print("Creating the bag of words...\n")
from sklearn.feature_extraction.text import CountVectorizer
# Initialize the "CountVectorizer" object, which is scikitlearn's bag of words tool.
vectorizer = CountVectorizer(analyzer = "word", \
 tokenizer = None, \
preprocessor = None, \
stop_words = None, \
max_features = 5000)
# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training
# data into feature vectors.
# Input to fit_transform(): a list of strings
# Output: a document-term sparse matrix [n_samples, n_features]
train_data_features = vectorizer.fit_transform(clean_train_reviews)
# Numpy arrays are easy to work with, so convert the result to an array
train_data_features = train_data_features.toarray()

#print(train_data_features.shape) 

# Take a look at the words in the vocabulary
vocab = vectorizer.get_feature_names()
#print(vocab)

import numpy as np
# Sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)
# For each, print the vocabulary word and the number of times it
# appears in the training set
for tag, count in zip(vocab, dist):
 print(count, tag)

from sklearn.feature_extraction.text import TfidfVectorizer
print("Creating the tf/idf...\n")
# Initialize the "TfidfVectorizer" object, which is scikitlearn's tf/idf tool.
tfidf_vectorizer = TfidfVectorizer(max_df=0.7, \
 max_features=5000, \
 min_df=0.01, \
stop_words=None, \
 use_idf=True, \
 tokenizer=None, \
ngram_range=(1,3))
# Tf-idf-weighted term-document sparse matrix
tfidf_train_data_features =tfidf_vectorizer.fit_transform(clean_train_reviews)
# Convert the result to nampy array
tfidf_train_data_features = tfidf_train_data_features.toarray()
print(tfidf_train_data_features.shape) # (25000, 48)
# Take a look at the words in the vocabulary
tfidf_vocab = tfidf_vectorizer.get_feature_names()
print(tfidf_vocab)



from sklearn.cluster import KMeans
# Perform k-means clustering
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters)
# Use k-keans to make sentiment label clustering
kmeans.fit(tfidf_train_data_features)
# get cluster assignments; a label (0 or 1) for each review
labels = kmeans.labels_.tolist()

# Fancy indexing and sorting on each cluster to identify which
# are the top n words that are nearest to the cluster centroid.
# This gives a good sense of the main topic of the cluster.
print("Top terms per cluster:")
print()
# Find which features contribute more to each cluster center.
# Sort in descending order by feature contribution and return indexes. For example:
# ascending: np.array([3, 4, 10, 1, 8]).argsort() returns array([3, 0, 1, 4, 2])
# descending: np.array([3, 4, 10, 1, 8]).argsort[::-1] returns array([2, 4, 1, 0, 3])
sorted_index_centroids = kmeans.cluster_centers_.argsort()[:,::-1]
for i in range(num_clusters):
 print("Cluster %d words:" % i, end='')
 print("word per cluster")
 #replace 10 with n words per cluster
 for ind in sorted_index_centroids[i, :10]:
    print(' %s' % tfidf_vocab[ind].split(' ')[0], end=',')
 print() #add whitespace
 print() #add whitespace

from sklearn.model_selection import train_test_split
# split features and labels (e.g. test = 20%, training = 80% )
# try both bag of words and tfidf features
x_train, x_test, y_train, y_test = train_test_split(tfidf_train_data_features,train['sentiment'].values, test_size=0.2)
print("Training the random forest...")
from sklearn.ensemble import RandomForestClassifier
# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100)
# Fit the forest to the training set, using the tfidf as
# features and the sentiment labels as the response variable
# This may take a few minutes to run
forest_model = forest.fit( x_train, y_train )
# Use the random forest model to make sentiment label predictions
y_pred = forest_model.predict( x_test )
# evaluate accuracy using hamming loss metric
from sklearn.metrics import hamming_loss
print(1-hamming_loss(y_pred, y_test))
