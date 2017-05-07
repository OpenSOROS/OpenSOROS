#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapers.reddit_scraper as rs 
import scrapers.fb_scraper as fs
import scrapers.twitter_scraper as ts
import models
import time
import argparse
import sys
import csv
import string
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import multiprocessing
import sklearn.manifold
import os.path
import os
import csv_utils
from gensim.models import doc2vec

IMAGE_DIR = "../images"
DATA_DIR = "../data"

PNG = ".png"
TSNE = "-T-SNE-"
MDS = "MDS"

TYPE_FB = "_fb"
TYPE_TWITTER = "_twitter"
TYPE_REDDIT = "_reddit"

HEADERS = ['x', 'y', 'label']

def visualizeSimilarities(subreddits, names, model, id, save_csv = False, name = ""):

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
    similarityMatrix = models.getDoc2VecSimilarityMatrix(model, id)
    if save_csv:
        csv_utils.similarity_to_csv(name, similarityMatrix, names)
    # using 1-similarity to convert to distance

    # some random colours for the scatterplot
    colours = cm.rainbow(np.linspace(0,1, len(names)))

    # Try t-SNE first 

    # In 2D... 

    tsne = sklearn.manifold.TSNE(n_components=2, metric = "precomputed")
    Y = tsne.fit_transform(similarityMatrix)

    if save_csv:
        csv_utils.plot_to_csv(name, Y, names)


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

    currentdatetime = str(str(time.localtime()[1])+"-"+str(time.localtime()[2])+"-"+str(time.localtime()[0])+"_"+str(time.localtime()[3]))

    parser = argparse.ArgumentParser()

    parser.add_argument('--sheetname', type=str, help='The name of the sheet where the list of sources is contained')
    parser.add_argument('--reddit', metavar='SUBREDDIT', type=str, nargs='+', help='list of subreddits to scrape')
    parser.add_argument('--fb', metavar='PAGE_ID', type=str, nargs='+', help='list of Facebook page ids to scrape')
    parser.add_argument('--twitter', metavar='TWITTER_HANDLE', type=str, nargs='+', help='list of Twitter handles to scrape')
    parser.add_argument('--name', default = currentdatetime, type=str, help='the name of the csv files that the data will be stored in')
    parser.add_argument('--num_comments', default = 50, type=int, help='the number of facebook comments to scrape per post')
    parser.add_argument('--num_reddit_comments', default = 5000, type=int, help='the maximum number of Reddit comments to scrape per post')
    parser.add_argument('--num_posts', default = 50, type=int, help='the number of facebook posts to scrape per page')

    args = parser.parse_args()
    sheet = args.sheetname
    if sheet is not None:
        args = parser.parse_args(csv_utils.parse_csv(sheet))

    comments = []
    titles = []
    tweets = []
    page_ids = []
    subreddits = []
    twitters = []

    if args.fb is not None:
        page_ids = args.fb
        for page_id in page_ids:
            comments_full = fs.get_comments_from_id(page_id, args.num_posts, args.num_comments)
            comments.append([(" ").join(fs.get_messages_from_comments(comments_full))])
            csv_utils.comments_to_csv(args.name, page_id, comments_full, TYPE_FB)

    if args.twitter is not None:
        twitters = args.twitter
        for twitter in twitters:
            tweets_full = ts.get_tweets_from_screenname(twitter)
            tweets.append([(" ").join(ts.get_messages_from_comments(tweets_full))])
            csv_utils.comments_to_csv(args.name, twitter, tweets_full, TYPE_TWITTER)

    if args.reddit is not None:
        subreddits = args.reddit
        for subreddit in subreddits:
            titles_full = rs.get_comments_from_subreddit(subreddit, args.num_reddit_comments)
            titles.append([(" ").join(rs.get_messages_from_comments(titles_full))])
            csv_utils.comments_to_csv(args.name, reddit, titles_full, TYPE_REDDIT)

    print("Done saving CSV")

    docs, id = models.preprocessDocs(comments+titles+tweets)
    model = models.trainDoc2Vec(docs)

    visualizeSimilarities(comments+titles+tweets, page_ids + subreddits+twitters, model, id, save_csv=True, name = args.name)

if __name__ == "__main__":
    main()