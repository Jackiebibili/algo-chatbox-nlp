from .general_kb.dataprep.prep_wiki import prepare_wiki_articles
from .qna_kb.dataprep.prep_qna import prepare_qna_pairs

if __name__ == "__main__":
   prepare_qna_pairs()
   prepare_wiki_articles()
