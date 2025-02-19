# import nltk
# import spacy
# import wikipedia
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# from genai_4_dps_helper.base_obj import BaseObj

# # Load the spacy model for NER
# nlp = spacy.load("en_core_web_sm")


# nltk.download("punkt_tab")
# nltk.download("stopwords")
# nltk.download("wordnet")


# class WikipediaFactCheck(BaseObj):
#     def __init__(self):
#         super(WikipediaFactCheck, self).__init__()

#     def __search_wikipedia(self, query):
#         try:
#             results = wikipedia.search(query, results=10)
#             return results
#         except wikipedia.exceptions.DisambiguationError as e:
#             return e.options
#         except wikipedia.exceptions.PageError:
#             return None

#     def __get_page_content(self, title):
#         try:
#             page = wikipedia.page(title)
#             return page.content
#         except wikipedia.exceptions.DisambiguationError as e:
#             return e.options
#         except wikipedia.exceptions.PageError:
#             return None

#     def __compare_text(self, summary, content):
#         # Tokenize texts
#         summary_tokens = word_tokenize(summary.lower())
#         content_tokens = word_tokenize(content.lower())

#         # Remove stopwords
#         stop_words = set(stopwords.words("english"))
#         summary_tokens = [token for token in summary_tokens if token not in stop_words]
#         content_tokens = [token for token in content_tokens if token not in stop_words]

#         # Compare tokens
#         common_tokens = set(summary_tokens) & set(content_tokens)
#         similarity = len(common_tokens) / len(set(summary_tokens))

#         return similarity

#     def __advanced_compare_text(self, summary, content):
#         # Tokenize and lemmatize the texts
#         lemmatizer = WordNetLemmatizer()
#         summary_tokens = [
#             lemmatizer.lemmatize(word) for word in word_tokenize(summary.lower())
#         ]
#         content_tokens = [
#             lemmatizer.lemmatize(word) for word in word_tokenize(content.lower())
#         ]

#         # Remove stopwords
#         stop_words = set(stopwords.words("english"))
#         summary_tokens = [token for token in summary_tokens if token not in stop_words]
#         content_tokens = [token for token in content_tokens if token not in stop_words]

#         # Join the tokens back into strings
#         summary_text = " ".join(summary_tokens)
#         content_text = " ".join(content_tokens)

#         # Use TF-IDF to convert the texts into vectors
#         vectorizer = TfidfVectorizer()
#         tfidf = vectorizer.fit_transform([summary_text, content_text])

#         # Calculate the cosine similarity between the vectors
#         similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

#         # Use NER to identify and compare entities
#         summary_entities = [(ent.text, ent.label_) for ent in nlp(summary).ents]
#         content_entities = [(ent.text, ent.label_) for ent in nlp(content).ents]

#         # Calculate the entity similarity
#         entity_similarity = len(set(summary_entities) & set(content_entities)) / len(
#             set(summary_entities)
#         )

#         # Combine the TF-IDF and entity similarities
#         combined_similarity = (similarity[0][0] + entity_similarity) / 2

#         return combined_similarity

#     def fact_check(self, summary):
#         # Search Wikipedia
#         results = self.__search_wikipedia(summary)

#         # Get page content
#         if results:
#             page_title = results[0]
#             content = self.__get_page_content(page_title)

#             # Compare texts
#             if content:
#                 # similarity = self.__compare_text(summary, content)
#                 similarity = self.__advanced_compare_text(summary, content)
#                 return similarity
#         return None
