
import pandas as pd
import numpy as np
import io
import sys
import os.path
import urllib.request
from tqdm import tqdm
from os import listdir
from PIL import Image
import glob

pd.set_option('display.max_colwidth', 1)
np.set_printoptions(threshold=sys.maxsize)

df = pd.read_csv("C:/Users/motis/Desktop/finallyProject/ElasticSearch/netflix_with_rating.csv",encoding='UTF8')
#print(df.shape)
df_2 = df[['imdbID','genre','imdbRating' ]]
print(df_2)

df_2.to_csv("MovieGenre_cleaned.csv", index = None)


