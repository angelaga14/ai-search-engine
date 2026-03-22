# AI Search Engine with BM25

## Student
Angela González Arredondo

## Domain
Artificial Intelligence and Machine Learning Articles

I chose this domain because it is highly relevant in today's technological world and provides a large amount of real and meaningful content for search queries.

## Enhancement
A - Term Highlighting

The search engine highlights query terms directly in the results, allowing users to quickly identify relevant content.

## Features
- Text preprocessing (tokenization, lowercase, stopwords, stemming)
- Inverted index with posting lists
- BM25 ranking algorithm
- Web interface using Flask
- Term highlighting
- Corpus statistics (documents, vocabulary size, search time)

## Project Structure
- `corpus.json` → document collection
- `search_engine.py` → search logic and BM25
- `app.py` → Flask web application
- `templates/` → HTML interface
- `static/` → CSS styles

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt