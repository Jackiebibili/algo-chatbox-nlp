import pandas as pd
import numpy as np
import os

topic_store_csv_filename = "wiki_topics_sheet.csv"
topic_store_wiki_titles_col = [3]


def generate_kb_text(dirpath: str):
    df = pd.read_csv(os.path.join(dirpath, topic_store_csv_filename))
    df_wiki_titles = df.iloc[0:, topic_store_wiki_titles_col]
    arrs = df_wiki_titles.values.tolist()
    return np.array(arrs).flatten().tolist()
