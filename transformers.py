#======================================================#
# Created by Filip Bunta for Lundegaard interview task #
#======================================================#
"""
Module is storing two custom transformes, converting function and few constants.
"""
import pandas as pd
import string
import numpy as np
import itertools
from sklearn.base import BaseEstimator, TransformerMixin

POSITIVE_FEEDBACK_WORDS = ["best","delicious","yummy","wonderful","healthy","perfect","amazing","fantastic","nice",
                           "happy","love","loves","awesome","favorite","great","good"]
NEGATIVE_FEEDBACK_WORDS = ["horrible","terrible","dissapointed","worst","disgusting","dissapointing","warning",
                           "awful","nasty","waste","misleading","expensive","unfortunately"]
FEEDBACK_WORDS = POSITIVE_FEEDBACK_WORDS + NEGATIVE_FEEDBACK_WORDS
MAX_POSITIVE_INDEX = len(POSITIVE_FEEDBACK_WORDS) - 1
STRIP = string.whitespace + string.punctuation + string.digits + "\""

def convert_text_to_vector(dataframe: pd.DataFrame) -> list:
    """Function returning a list in form of vector from a text input.

    Aim of the function is to convert the text string into a vector representing availability of pre-defined words.

    REQUIREMENTS:
    Input dataframe should have two text value columns 'Summary' and 'Text'.
    
    PARAMETERS:
    dataframe: input pandas dataFrame object
    """
    vector = list(itertools.repeat(0,len(FEEDBACK_WORDS)))
    text = dataframe["Summary"] + dataframe["Text"]
    for word in text.lower().split():
        word_strip = word.strip(STRIP)
        if word_strip in FEEDBACK_WORDS:
            i = FEEDBACK_WORDS.index(word_strip)
            vector[i] = -1 if i > MAX_POSITIVE_INDEX else 1
            break
    return vector

class VectorizeTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer class converting dataframe text column(s) into a vector."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        vectorize = X.apply(convert_text_to_vector,axis=1)
        return np.array(vectorize.tolist())

class CategorizeTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer class re-categorizing dataframe ratings column into good/bad (1/0) category."""
    def __init__(self,positive_rating_limit=3.0):
        self.positive_rating_limit = positive_rating_limit

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        categorize = X["Score"].apply(lambda x: 1 if x >= self.positive_rating_limit else 0)
        return np.array(categorize)
