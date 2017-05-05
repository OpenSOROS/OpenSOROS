#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapers.reddit_scraper as rs 
import scrapers.fb_scraper as fs
import models
import argparse
import sys
import string
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

    # In 2D... 

    tsne = sklearn.manifold.TSNE(n_components=2, metric = "precomputed")
    Y = tsne.fit_transform(similarityMatrix)


    fig, ax = plt.subplots()
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        plt.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend()


    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + TSNE + "2D" + PNG)
    plt.savefig(image_path)

    # ... and in 3D

    tsne = sklearn.manifold.TSNE(n_components=3, metric = "precomputed")
    Y = tsne.fit_transform(similarityMatrix)


    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        ax.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], Y[idx:next_idx, 2], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend(loc = 'best')


    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + TSNE + "3D" + PNG)
    plt.savefig(image_path)

    # Then MDS, in 2D

    mds = sklearn.manifold.MDS(n_components=2, dissimilarity = "precomputed")
    Y = mds.fit_transform(similarityMatrix)


    fig, ax = plt.subplots()
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        plt.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend()

    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + MDS + "2D" + PNG)
    plt.savefig(image_path)

    # ... and 3D

    mds = sklearn.manifold.MDS(n_components=3, dissimilarity = "precomputed")
    Y = mds.fit_transform(similarityMatrix)


    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    idx = 0
    for i in range(0,len(names)):
        next_idx = idx + len(subreddits[i])
        ax.scatter(Y[idx:next_idx,0], Y[idx:next_idx, 1], Y[idx:next_idx, 2], c = colours[i],  label = names[i])
        idx = next_idx
    ax.legend(loc = 'best')

    image_path = os.path.join(os.getcwd(), IMAGE_DIR, ("+").join(names) + MDS + "3D" + PNG)
    plt.savefig(image_path)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--reddit', metavar='SUBREDDIT', type=str, nargs='+', help='list of subreddits to scrape')
    parser.add_argument('--fb', metavar='PAGE_ID', type=str, nargs='+', help='list of Facebook page ids to scrape')
    parser.add_argument('--num_comments', default = 50, type=int, help='the number of facebook comments to scrape per post')
    parser.add_argument('--num_posts', default = 50, type=int, help='the number of facebook posts to scrape per page')
    args = parser.parse_args()

    comments = []
    titles = []

    if args.fb is not None:
        comments = [fs.get_comments_from_id(page_id, args.num_posts, args.num_comments) for page_id in args.fb]

    if args.reddit is not None:
        titles = [rs.printTitles(subreddit) for subreddit in args.reddit]

    docs, id = models.preprocessDocs(comments+titles)
    model = models.trainDoc2Vec(docs)

    visualizeSimilarities(comments+titles,args.fb+args.reddit, model, id)

if __name__ == "__main__":
    main()