import json
import math
import re
from collections import defaultdict, Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# descargar recursos necesarios
nltk.download("punkt")
nltk.download("stopwords")


class SearchEngine:
    def __init__(self, corpus_file="corpus.json", k1=1.5, b=0.75):
        self.corpus_file = corpus_file
        self.k1 = k1
        self.b = b

        self.documents = []
        self.index = defaultdict(dict)   # term -> {doc_id: freq}
        self.doc_lengths = {}
        self.avg_doc_length = 0
        self.vocabulary = set()

        self.stop_words = set(stopwords.words("english"))
        self.stemmer = PorterStemmer()

        self.load_corpus()
        self.build_index()

    # 📥 cargar documentos
    def load_corpus(self):
        with open(self.corpus_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

    # 🧹 limpiar texto
    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        tokens = word_tokenize(text)

        tokens = [
            self.stemmer.stem(t)
            for t in tokens
            if t not in self.stop_words and t.strip()
        ]

        return tokens

    # 📚 crear índice invertido
    def build_index(self):
        total_length = 0

        for doc in self.documents:
            doc_id = doc["id"]
            tokens = self.preprocess(doc["text"])

            self.doc_lengths[doc_id] = len(tokens)
            total_length += len(tokens)

            freqs = Counter(tokens)

            for term, freq in freqs.items():
                self.index[term][doc_id] = freq
                self.vocabulary.add(term)

        if self.documents:
            self.avg_doc_length = total_length / len(self.documents)

    # 🧠 BM25
    def bm25_score(self, query, doc_id):
        query_terms = self.preprocess(query)
        score = 0

        N = len(self.documents)
        dl = self.doc_lengths[doc_id]

        for term in query_terms:
            if term not in self.index:
                continue

            if doc_id not in self.index[term]:
                continue

            df = len(self.index[term])
            tf = self.index[term][doc_id]

            idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (dl / self.avg_doc_length))

            score += idf * (numerator / denominator)

        return score

    # 🔍 buscar
    def search(self, query, top_k=10):
        results = []

        for doc in self.documents:
            doc_id = doc["id"]
            score = self.bm25_score(query, doc_id)

            if score > 0:
                results.append((doc, score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    # 📊 stats
    def get_stats(self):
        return {
            "total_documents": len(self.documents),
            "vocabulary_size": len(self.vocabulary),
            "avg_doc_length": round(self.avg_doc_length, 2)
        }

if __name__ == "__main__":
    engine = SearchEngine()

    results = engine.search("machine learning")

    for doc, score in results:
        print(doc["title"], score)