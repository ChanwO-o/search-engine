# Inverted Index Search Engine

A search engine built in my CS121 Information Retrieval course at UC Irvine.

The goal of this project was to create a system that can instantly return search results from a corpus of approximately 37000 files.
Data was collected by crawling file systems of UC Irvine web servers (designing the crawler was another previous project in this course)

The main data structure of the search engine is a dictionary that uses an inverted-index. This guarantees that a search with a single term can be returned in constant time O(1). The relevance of each search result could be ranked by calculating its tf-idf values.

My team customized our system by adding advanced search engine techniques (ignore stopwords, incorporating multiple terms in search phrase, etc.)
