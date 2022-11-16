import re

sections_skipped = [
   "See also",
   "Notes",
   "References",
   "External links",
   "Original papers",
   "Original sources",
   "Secondary sources",
   "Further reading",
   ]


def get_regex(section_title: str):
   return re.compile(rf"#{{2,3}} {section_title}(.|\n)*?(?=(#{{2,3}})|(\Z))")


def filter_wiki_content_helper(text: str, section_title: str):
   regex = get_regex(section_title)
   return regex.sub('', text)


def filter_wiki_content(text: str):
   out_text = text
   for title in sections_skipped:
      out_text = filter_wiki_content_helper(out_text, title)
   
   return out_text
