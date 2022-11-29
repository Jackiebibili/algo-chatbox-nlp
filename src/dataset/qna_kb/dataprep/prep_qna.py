import os
import pandas as pd

data_collection_in_dir = "src/dataset/qna_kb/data/kb_qna_ori.csv"
data_collection_out_dir = "src/dataset/qna_kb/data/kb_qna_v1.csv"

data_collection_in_dir_abs_path = os.path.join(
    os.path.abspath(os.getcwd()), data_collection_in_dir)
data_collection_out_dir_abs_path = os.path.join(
    os.path.abspath(os.getcwd()), data_collection_out_dir)

def prepare_qna_pairs():
   df = pd.read_csv(data_collection_in_dir_abs_path)
   df.dropna(0, inplace=True)
   df["Question"] = df["Question"].apply(lambda x: x.strip())
   df = df.rename(columns={"Answers": "answer", "Question": "question"})
   df.to_csv(data_collection_out_dir_abs_path, index=False)
   return df
