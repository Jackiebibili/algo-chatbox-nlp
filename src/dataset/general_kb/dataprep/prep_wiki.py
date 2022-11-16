import os
from urllib.parse import quote
from .filter_wiki import filter_wiki_content
from .topics_store import wiki_topics
from lib.wikipediaapi.fetch_wiki_html import fetch_wiki_article
from lib.html2text.driver import convertHTMLtoText
from src.util.util import pipe

data_collection_dir = "src/dataset/general_kb/data"
data_collection_dir_abs_path = os.path.join(
    os.path.abspath(os.getcwd()), data_collection_dir)

def prepare_wiki_articles():
   for topic in wiki_topics:
      wiki_text = pipe(topic, [
         fetch_wiki_article,
         convertHTMLtoText,
         filter_wiki_content
         ])

      write_text_to_file(wiki_text, topic)
   pass

def write_text_to_file(text: str, filename: str):
   out_file = open(os.path.join(data_collection_dir_abs_path, quote(filename)), "w")
   out_file.write(text)
   out_file.close()
