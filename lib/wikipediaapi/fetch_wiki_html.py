import wikipediaapi

def fetch_wiki_article(article_title: str):
   wiki_wiki = wikipediaapi.Wikipedia(
      language='en',
      extract_format=wikipediaapi.ExtractFormat.HTML
   )

   p_wiki = wiki_wiki.page(article_title)
   
   return p_wiki.text
