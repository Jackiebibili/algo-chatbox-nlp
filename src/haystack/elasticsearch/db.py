import os
import logging
import pandas as pd
from dotenv import load_dotenv
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
# load environment variables
load_dotenv()

# config logging
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

# Get the host where Elasticsearch is running, default to localhost
host = os.getenv('es_host', 'localhost')
username = os.getenv('es_username', 'elastic')
pw = os.getenv('es_pw', 'secret')
port = int(os.getenv('es_port', 9200))

def store_qna_kb():
   index = "qna_document"
   document_store = ElasticsearchDocumentStore(
      host=host,
      scheme='https', 
      port=port, 
      index=index, 
      username=username, 
      password=pw,
      embedding_field="question_emb",
      embedding_dim=384,
      excluded_meta_data=["question_emb"],
      similarity="cosine")
   
   retriever = EmbeddingRetriever(
      document_store=document_store,
      embedding_model="sentence-transformers/all-MiniLM-L6-v2",
      use_gpu=True,
      scale_score=False,
   )

   # Get dataframe with columns "question", "answer" and some custom metadata
   file_path = os.path.join(os.getcwd(), "src/dataset/qna_kb/data/kb_qna_v1.csv")
   df = pd.read_csv(file_path)

   # Get embeddings for our questions from the FAQs
   questions = list(df["question"].values)
   df["question_emb"] = retriever.embed_queries(queries=questions).tolist()
   df = df.rename(columns={"question": "content"})

   # Convert Dataframe to list of dicts and index them in our DocumentStore
   docs_to_index = df.to_dict(orient="records")

   document_store.write_documents(docs_to_index)
   pass


def store_general_kb():
   index = "document"
   document_store = ElasticsearchDocumentStore(host=host, scheme='https', port=port, index=index, username=username, password=pw)
   # preprocessing documents
   doc_dir = os.path.join(os.getcwd(), "src/dataset/general_kb/data")
   # s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
   # fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

   # Convert files to dicts
   # You can optionally supply a cleaning function that is applied to each doc (e.g. to remove footers)
   # It must take a str as input, and return a str.
   docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

   # We now have a list of dictionaries that we can write to our document store.
   # If your texts come from a different source (e.g. a DB), you can of course skip convert_files_to_dicts() and create the dictionaries yourself.
   # The default format here is:
   # {
   #    'content': "<DOCUMENT_TEXT_HERE>",
   #    'meta': {'name': "<DOCUMENT_NAME_HERE>", ...}
   # }
   # (Optionally: you can also add more key-value-pairs here, that will be indexed as fields in Elasticsearch and
   # can be accessed later for filtering or shown in the responses of the Pipeline)

   # Let's have a look at the first 1 entries:
   # print(docs[:1])

   # Now, let's write the dicts containing documents to our DB.
   document_store.write_documents(docs)

store_qna_kb()
store_general_kb()
