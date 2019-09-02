import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import sklearn.manifold
import csv_utils

# Options for TSNE parameters to explore.
PERPLEXITY_OPTIONS = [10, 22, 33, 50, 80]
LEARN_RATE_OPTIONS = [10, 30, 100, 300, 1000]

IMAGE_DIR = "images"
PNG = ".png"
ALL_TSNE = "-ALL-T-SNE-"

def clean_subplots(r, c, pad=0.05):
    """
    Helper method: open a full-screen, r x c grid of graphs with minimal padding and no axes labels.
    """
    f = plt.figure()
    ax = []
    at = 1
    for i in range(r):
        row = []
        for j in range(c):
            axHere = f.add_subplot(r, c, at)
            axHere.get_xaxis().set_visible(False)
            axHere.get_yaxis().set_visible(False)
            row.append(axHere)
            at = at + 1
        ax.append(row)
    f.subplots_adjust(left=pad, right=1.0-pad, top=1.0-pad, bottom=pad, hspace=pad)
    try:
        plt.get_current_fig_manager().window.showMaximized()
    except AttributeError:
        pass # Can't maximize, sorry :(
    return ax


def show_tsne(ax, distances, perplexity, learnRate, colors):
    """
    Calculate TSNE placement, and draw scatter plot.

    Args:
        ax: The matplotlib axes to draw the result on.
        distances: Original distance matrix.
        perplexity: TSNE perplexity option.
        learnRate: Learning rate for TSNE.
        colors: Colors to use for each dot, in the same order as distances.
    """
    fitted = sklearn.manifold.TSNE(
        n_components=2, metric="precomputed", perplexity=perplexity, learning_rate=learnRate
    ).fit_transform(distances)

    ax.scatter(fitted[:, 0], fitted[:, 1], color=colors)


def party_color(party):
    """
    Convert a BC party to its color. Supports Greens, Liberal and NDP, the rest are grey.
    From https://en.wikipedia.org/wiki/Template:Canadian_politics/party_colours

    Args:
        party (str): Name of the party to convert.

    Returns:
        color (str): RGB hex code for the party color.
    """
    if party == 'BC Green Party':
        return '#2f873e'
    elif party == 'BC Liberal Party':
        return '#f08080'
    elif party == 'BC NDP':
        return '#f4a460'
    else:
        return '#dcdcdc'


def colors_for_people(name, people):
    """
    Given a list of people (with _twitter suffix), convert to a list of their party colors.

    Args:
        name (str): Identifier of the CSV containing the mapping to parties.
        people (str[]): Names of the people to convert to colors.
    """
    mapping = csv_utils.parties_from_csv(name)
    defaultColor = party_color(None)

    colors = []
    for person in people:
        personFixed = person[:len(person) - len("_twitter")]
        if personFixed in mapping:
            colors.append(party_color(mapping[personFixed]))
        else:
            colors.append(defaultColor)
    return colors


def main(name, save):
    print "Displaying for similarity matrix %s" % name
    similarityMatrix, people = csv_utils.similarity_from_csv(name)
    colours = colors_for_people(name, people)

    ax = clean_subplots(5, 5)
    for i, perplexity in enumerate(PERPLEXITY_OPTIONS):
        ax[i][0].get_yaxis().set_visible(True)
        ax[i][0].set_ylabel("Perplexity = %d" % perplexity)
        for j, learnRate in enumerate(LEARN_RATE_OPTIONS):
            if i == 0:
                ax[0][j].set_title("Learn rate = %d" % learnRate)
            show_tsne(ax[i][j], similarityMatrix, perplexity, learnRate, colours)

    if save:
        image_path = os.path.join(os.getcwd(), IMAGE_DIR, name + ALL_TSNE + "2D" + PNG)
        plt.gcf().set_size_inches(18.5, 10.5)
        plt.savefig(image_path)
        print "Image saved to %s" % str(image_path)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='5-17-2017_15', type=str, help='the name of the csv files that the data will be stored in')
    parser.add_argument('--save', default=False, type=bool, help='Whether to save the resulting plot to file')

    args = parser.parse_args()
    main(args.name, args.save)
