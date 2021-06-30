
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk

import JobAdsIO
from CustomStopwords import CustomStopwords, CompanyNames, Technologies, Punctuation

ApiKey      = JobAdsIO.GetAPIKey()
AdsFileName = "platsbanken-ads"

def GetTechAdsList():
    # Try to read job ads from file, or else call the API
    jobAds = None
    try:
        jobAds = JobAdsIO.GetJobsFromFile(AdsFileName)
    except IOError:
        jobAds = []
    finally:
        if jobAds is None or len(jobAds) <= 0:
            jobAds = JobAdsIO.GetAllJobAds(ApiKey)
    print("Loaded %i ads from Platsbanken." % len(jobAds))

    techJobAds = JobAdsIO.GetTechJobsAds(jobAds)
    print("Found %i ads in Data/IT." % len(techJobAds))

    return techJobAds


def StemTokenize(text: str):
    """A custom tokenizer that also stems the words, intended to be passed to constructor of TfidfVectorizer.
    It performs lancaster stemming, and filters out all stems that have a length less than or equal to 3."""
    lancaster = LancasterStemmer()
    stems = [lancaster.stem(word) for word in word_tokenize(text)]
    stems = list(filter(lambda token: len(token) > 3, stems))
    return stems


if __name__ == "__main__":
    nltk.download('punkt')  # Ensure installed
    nltk.download('stopwords')

    NUM_CLUSTERS = 4

    techJobAds = GetTechAdsList()

    # Retrieve text body of job ads
    jobAdsRawText = list(map(lambda ad: ad['description']['text'], techJobAds))

    # Create a set of stopwords, used in training and keyword extraction below
    myStopwords = set(stopwords.words('swedish') +
                      stopwords.words('english') +
                      list(punctuation) +
                      list(CustomStopwords) +
                      list(CompanyNames) +
                      list(Technologies) +
                      list(Punctuation))

    # Set max_df to a high value in [0.7, 1.0) to automatically filter out common words.
    # See: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    vectorizer = TfidfVectorizer(max_df=0.80, min_df=2, stop_words=myStopwords, tokenizer=StemTokenize)
    X = vectorizer.fit_transform(jobAdsRawText) # 2x2 matrix with: One row <=> one article, one column <=> one distinct word

    # Perform the actual clustering
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, init='k-means++', max_iter=100, n_init=1, verbose=True)
    kmeans.fit(X)

    # Metadata about the clustering
    (categories, numArticles) = np.unique(kmeans.labels_, return_counts=True)

    # Find most frequent words within each cluster

    aggregate = {} # Cluster number => aggregated text of all articles in given cluster
    for i, cluster in enumerate(kmeans.labels_):
        adText = jobAdsRawText[i]
        if cluster not in aggregate.keys():
            aggregate[cluster] = adText
        else:
            aggregate[cluster] += adText

    # Find top N words for text within each cluster
    N           = 100
    keywords    = {}
    counts      = {}    # Store the frequency distribution of each cluster
    for cluster in categories:
        tokenizedClusterText = word_tokenize(aggregate[cluster].lower())
        tokenizedClusterText = [word for word in tokenizedClusterText if word not in myStopwords]
        freq = FreqDist(tokenizedClusterText)
        keywords[cluster] = nlargest(N, freq, key=freq.get)
        counts[cluster] = freq

    # Find top M unique keywords of each cluster
    M = 10
    uniqueKeys = {}
    for cluster in categories:
        otherClusters       = list(set(categories) - set([cluster]))

        keysOtherClusters = set()
        for i in range(len(otherClusters)):
            keysOtherClusters = keysOtherClusters.union(set(keywords[otherClusters[i]]))

        unique = set(keywords[cluster])-keysOtherClusters
        uniqueKeys[cluster] = nlargest(M, unique, key=counts[cluster].get)

    print(uniqueKeys)

    print("Process finished. The number of ads in respective cluster was:")
    print(numArticles)
