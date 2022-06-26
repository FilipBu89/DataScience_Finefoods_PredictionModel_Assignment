#===================================================================#
# Created by Filip Bunta for Lundegaard data science interview task #
#===================================================================#
import string
import collections
from typing import List, Tuple

"""
Module is storing a small function used to identify unique words and their frequency.
"""

def count_unique_words(reviews: List[str], ratings: List[float], 
                        limit_filter: Tuple[float]= None, limit_output: int=100) -> None:
    """Function is printing out unique words and their count

    PARAMETERS:
    text: List of reviews.
    rating: List of ratings.
    limit_filter: Specifying ratings for which words should be printed.
                  Default is None, meaning all ratings will be included in output.
    limit_output: Specifying how many words should be printed. Default is 100.
    """
    words = collections.defaultdict(int)
    strip = string.whitespace + string.punctuation + string.digits + "\""
    for review, rating in zip(reviews, ratings):
        for word in review.lower().split():
            word = word.strip(strip)
            if len(word) > 3:
                words[word,rating] += 1
    filter_data = sorted_data = reversed(sorted(words.items(),key=lambda x: (x[1],x[0][1])))
    if limit_filter is not None:
        filter_data = (x for x in sorted_data if x[0][1] in limit_filter)
    for i, word in enumerate(filter_data):
        print(f"'{word[0][0]}' with rating {word[0][1]} appears in file {word[1]}-times")
        if i > limit_output:
            break
