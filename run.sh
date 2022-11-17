# prepare wiki articles
python -m src.dataset.start
# archive files
zip wiki_algos_text.zip src/dataset/general_kb/data/* -j

# connect and write to the document store
# python -m src.haystack.elasticsearch.db