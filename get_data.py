#===================================================================#
# Created by Filip Bunta for Lundegaard data science interview task #
#===================================================================#
import os
import re
import string
import gzip
import shutil
import io
import urllib.request
import pandas as pd
from pandas import DataFrame
import collections
"""
Module is storing small functions for retrieving and loading input data.
"""

DOWNLOAD_ROOT = "http://snap.stanford.edu/data"
FINEFOODS_PATH = os.path.join("datasets","finefoods")
FINEFOODS_COMPRESS_FILENAME = "finefoods.txt.gz"
FINEFOODS_TXT_FILENAME = "finefoods.txt"

def fetch_finefoods_data(finefoods_path: str = FINEFOODS_PATH, finefoods_url_path: str = DOWNLOAD_ROOT,
                       finefoods_compress_filename: str = FINEFOODS_COMPRESS_FILENAME,
                       finefoods_txt_filename: str = FINEFOODS_TXT_FILENAME) -> bool:
    """Fetch input data and return True if in/out and compressing actions on files were successfull, otherwise False.

    Function is scrapping dataset from web source and storing into local project directory.
    
    PARAMETERS:
    finefoods_path: Path to local directory, where downloaded file will be placed.
    finefoods_url_path: Web root storing the datasets.
    finefoods_compress_filename: Name of the actual web dataset.
    finefoods_txt_filename: Name of the output file, which will be stored in our local directory.
    """
    os.makedirs(finefoods_path,exist_ok=True)
    finefoods_url = finefoods_url_path + "/"+ finefoods_compress_filename
    gz_path = os.path.join(finefoods_path, finefoods_compress_filename)
    txt_path = os.path.join(finefoods_path,finefoods_txt_filename)
    urllib.request.urlretrieve(finefoods_url,gz_path)
    try:
        with open(gz_path,'rb') as fh_in, open(txt_path,'w',encoding="windows-1252") as fh_out:
            decomp_str = gzip.decompress(fh_in.read()).decode("windows-1252")
            fh_out.write(decomp_str)
    except EnvironmentError as err:
        print(f"File not converted successfully:\n{err}")
        return False
    return True

def convert_to_dataframe(file: str) -> pd.DataFrame:
    """Function converting a key-value pair text file into a pandas dataframe object.

    PARAMETERS:
    file: path to input text file.

    REQUIREMENTS:
    Format of the key-value pair(s) must fit the amazons fine foods text format specification.
    """
    with open(file, encoding="windows-1252") as fh:
        my_text = fh.read()
        
    product_id_regex = re.compile(r"""
        \bproduct/productId:\s(?P<product_id>.*)\n
        \breview/userId:\s(?P<user_id>.*)\n
        \breview/profileName:\s(?P<profile_name>.*)\n
        \breview/helpfulness:\s(?P<helpfulness>.*)\n
        \breview/score:\s(?P<score>.*)\n
        \breview/time:\s(?P<time>.*)\n
        \breview/summary:\s(?P<summary>.*)\n
        \breview/text:\s(?P<text>.*)\n
        """, re.VERBOSE)
    
    product_id = []
    user_id = []
    profile_name = []
    helpfulness = []
    score = []
    time = []
    summary = []
    text = []
    for match in product_id_regex.finditer(my_text):
        product_id.append(match.group("product_id"))
        user_id.append(match.group("user_id"))
        profile_name.append(match.group("profile_name"))
        helpfulness.append(match.group("helpfulness"))
        score.append(match.group("score"))
        time.append(match.group("time"))
        summary.append(match.group("summary"))
        text.append(match.group("text"))
    
    data_dict = {"ProductID": product_id,
                "UserID": user_id,
                "ProfileName": profile_name,
                "Helpfulness": helpfulness,
                "Score": score,
                "Time": time,
                "Summary": summary,
                "Text": text}

    return pd.DataFrame(data_dict)


