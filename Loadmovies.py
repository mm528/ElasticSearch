import pandas as pd
import re
# import nltk
import chardet
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from bs4 import BeautifulSoup # Import BeautifulSoup into your workspace

# #train = pd.read_csv("labeledTrainData.tsv", header=0,  delimiter="\t", quoting=3)
with open('netflix_titles.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
train = pd.read_csv('netflix_titles.csv', encoding=result['encoding'])
# #print(train.id)
print(train.shape)
print(train.columns.values)
# print(train)

# train['description'] = train['fullplot'].astype(str) + "\n" + train['plot'].astype(str)

train.head()

print(train["description"][0]) #>>>>>>>>>>>>>>>>>>String List (Text)
from nltk.corpus import stopwords # Import the stop word list
from nltk.stem.snowball import SnowballStemmer
# Stemming is the process of breaking a word down into its root.
stemmer = SnowballStemmer('english')
# In Python, searching a set is much faster than searching a list, so convert the stop words to a set
stops = set(stopwords.words("english"))

def plot_to_words( raw_plot ):
 # Function to convert a raw review to a string of words
 # The input is a single string (a raw movie review), and
 # the output is a single string (a pre-processed movie review)
 
 # 1. Remove HTML

 review_text = BeautifulSoup(raw_plot, "html.parser").get_text() 
 
 # 2. Remove non-letters
 letters_only = re.sub("[^a-zA-Z]", " ", review_text)
 
 # 3. Convert to lower case, split into individual words
 words = letters_only.lower().split()
 
#  # 4. Remove stop words
 meaningful_words = [w for w in words if not w in stops]
 
#  # 5. Stem words
 stemmed_meaningful_words = [stemmer.stem(w) for w in meaningful_words]
 
 # 6. Join the words back into one string separated by space and return the result.
 return( " ".join( words )) 
clean_review = plot_to_words( train["description"][0] )
print(clean_review)
print("----------------------------")
# # Get the number of reviews based on the dataframe column size
num_reviews = train["description"].size
print(num_reviews)
print("----------------------------")
# Initialize an empty list to hold the clean reviews
clean_train_reviews = []
# #clean_train_reviews.append( plot_to_words(train["plot"][0] ) )
# #clean_train_reviews.append( plot_to_words(train["plot"][1] ) )
# print("works")
# # Loop over each review; create an index i that goes from 0 to the length of the movie review list
for i in range( 0, num_reviews ):
    # Call our function for each one, and add the result to the list of clean reviews
    clean_train_reviews.append(plot_to_words(train["description"][i] ) ) #>>>>> HOW ITS LINK ! SINDESI ME TO TYPE TIS TAINIAS!

# print(clean_train_reviews)


print("Creating the bag of words...\n")
from sklearn.feature_extraction.text import CountVectorizer
# Initialize the "CountVectorizer" object, which is scikitlearn's bag of words tool.
vectorizer = CountVectorizer(analyzer = "word", \
                             tokenizer = None, \
                             preprocessor = None, \
                             stop_words = None, \
                             max_features = 1000)
# # fit_transform() does two functions: First, it fits the model and learns the vocabulary; second, it transforms our training
# # data into feature vectors.Input to fit_transform(): a list of strings
# # Output: a document-term sparse matrix [n_samples, n_features]
train_data_features = vectorizer.fit_transform(clean_train_reviews)
# # Numpy arrays are easy to work with, so convert the result to an array
train_data_features = train_data_features.toarray()

print(train_data_features.shape) 

# Take a look at the words in the vocabulary
vocab = vectorizer.get_feature_names()
# print(vocab)

import numpy as np
# Sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)
# For each, print the vocabulary word and the number of times it appears in the training set
# for tag, count in zip(vocab, dist):
#  print(count, tag)

from sklearn.feature_extraction.text import TfidfVectorizer
print("Creating the tf/idf...\n")
# Initialize the "TfidfVectorizer" object, which is scikitlearn's tf/idf tool.
tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=True, max_features=1000)

# Tf-idf-weighted term-document sparse matrix
tfidf_train_data_features = tfidf_vectorizer.fit_transform(clean_train_reviews)
# Convert the result to nampy array
tfidf_train_data_features = tfidf_train_data_features.toarray()
print(tfidf_train_data_features.shape) # (25000, 48)
# Take a look at the words in the vocabulary
tfidf_vocab = tfidf_vectorizer.get_feature_names()
# print(tfidf_vocab)



from sklearn.cluster import KMeans
# Perform k-means clustering
num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters)
# Use k-keans to make sentiment label clustering
kmeans.fit(tfidf_train_data_features)
# get cluster assignments; a label (0 or 1) for each review
labels = kmeans.labels_.tolist()
# # Fancy indexing and sorting on each cluster to identify which
# # are the top n words that are nearest to the cluster centroid.
# # This gives a good sense of the main topic of the cluster.
print("Top terms per cluster:")
print()
# # Find which features contribute more to each cluster center.
# # Sort in descending order by feature contribution and return indexes. For example:
# # ascending: np.array([3, 4, 10, 1, 8]).argsort() returns array([3, 0, 1, 4, 2])
# # descending: np.array([3, 4, 10, 1, 8]).argsort[::-1] returns array([2, 4, 1, 0, 3])
sorted_index_centroids = kmeans.cluster_centers_.argsort()[:,::-1]
for i in range(num_clusters):
 print("Cluster %d words:" % i, end='')
 #replace 10 with n words per cluster
 for ind in sorted_index_centroids[i, :10]:
   print('  %s' % tfidf_vocab[ind].split(' ')[0], end=',')
 print() #add whitespace
 print() #add whitespace


from sklearn.model_selection import train_test_split
# split features and labels (e.g. test = 20%, training = 80% ) try both bag of words and tfidf features
x_train, x_test, y_train, y_test = train_test_split(tfidf_train_data_features,train['description'].values,test_size=0.2) 
print("Training the random forest...")
from sklearn.ensemble import RandomForestClassifier
# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 20)
# Fit the forest to the training set, using the tfidf as
# features and the sentiment labels as the response variable
# This may take a few minutes to run
print("forest fix")
forest_model = forest.fit( x_train, y_train )
# Use the random forest model to make sentiment label predictions
print("predictions")
y_pred = forest_model.predict( x_test )
# evaluate accuracy using hamming loss metric
from sklearn.metrics import hamming_loss
print(1-hamming_loss(y_pred, y_test))
