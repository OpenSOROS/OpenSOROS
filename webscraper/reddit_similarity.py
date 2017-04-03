#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redditscraper
import sys
import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import multiprocessing
import sklearn.manifold
import os.path
import os
from gensim.models import doc2vec

IMAGE_DIR = "../images"
PNG = ".png"
TSNE = "-T-SNE-"
MDS = "MDS"



def preprocessDocs(subreddits):
    """
    Convert the lists of sentences into a doc2vec suitable format.
    Args: 
        subreddits (String[][]) - array of arrays of sentences, where each sentence will constitute a doc for doc2vec
    Returns:
        docs (TaggedDocument[]) - array of TaggedDocument objects ready to be passed into doc2vec
        id (int) - number of doc vectors 
    """
    docs = []
    id = 0
    for subreddit in subreddits:
        for title in subreddit:
            docs.append(doc2vec.TaggedDocument(title.translate(title.maketrans('','', string.punctuation)).split(" "), [id]))
            id += 1

    return docs, id
            


def trainDoc2Vec(docs): 
    """
    Train the doc2vec model on an array of TaggedDocuments.
    """

    cores = multiprocessing.cpu_count()
    model = doc2vec.Doc2Vec(docs, size=100, window=10, min_count=2, workers=cores)

    return model

def visualizeSimilarities(subreddits, names, model, id):

    """
    Visualize the similarities between the subreddit data, labelling the points according to the subreddit they came from.
    Right now trying to plot the data using:
        a) t-SNE (good for finding clusters)
        b) MDS (good for finding global structure)
    and printing into the /images directory. 

    Args:
        subreddits(String[][]) - all the data by subreddit 
        names(String[]) - the name of each subreddit 
        model(Doc2Vec) - the trained doc2vec model
        id

    """


    # First get the similarity matrix using the doc2vec cosine similarity metric
    similarityMatrix = np.matrix([[np.max([0, 1 - model.docvecs.similarity(i,j)]) for i in range(id)] for j in range(id)]) 
    # using 1-similarity to convert to distance

    # some random colours for the scatterplot
    colours = cm.rainbow(np.linspace(0,1, len(names)))
    # Try t-SNE first 

    tsne = sklearn.manifold.TSNE(n_components=2, metric = "precomputed")
    Y = tsne.fit_transform(similarityMatrix)


    fig, ax = plt.subplots()
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        plt.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend()


    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + TSNE + PNG)
    plt.savefig(image_path)

    # Then MDS 

    mds = sklearn.manifold.MDS(n_components=2, dissimilarity = "precomputed")
    Y = mds.fit_transform(similarityMatrix)


    fig, ax = plt.subplots()
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        plt.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend()

    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + MDS + PNG)
    plt.savefig(image_path)


def main():
    subreddits = sys.argv[1:]
    titles = [redditscraper.printTitles(subreddit) for subreddit in subreddits]
    docs, id = preprocessDocs(titles)
    model = trainDoc2Vec(docs)
    visualizeSimilarities(titles,subreddits,model, id)

    #Sanity check
    for i in range(10):
        index = np.random.randint(id)
        inferred_vector = model.infer_vector(docs[index].words)
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        try:
            print("Test sentence: " + " ".join(docs[index][0]))
            print("Most similar sentence: " + " ".join(docs[sims[0][0]].words))
        except Exception as e:
            pass

if __name__ == "__main__":
    main()