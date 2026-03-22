from flask import Flask, render_template, request
from search_engine import SearchEngine
import time
import re

app = Flask(__name__)
engine = SearchEngine()

# 🔥 Highlight de términos
def highlight_terms(text, query):
    words = query.lower().split()
    highlighted = text

    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", highlighted)

    return highlighted


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    search_time = 0
    stats = engine.get_stats()

    if request.method == "POST":
        query = request.form["query"]

        start = time.time()
        search_results = engine.search(query)
        search_time = round((time.time() - start) * 1000, 2)

        for doc, score in search_results:
            text = doc["text"]
            snippet = text[:200] + "..." if len(text) > 200 else text
            snippet = highlight_terms(snippet, query)

            results.append({
                "title": doc["title"],
                "source": doc["source"],
                "score": round(score, 4),
                "text": snippet
            })

    return render_template(
        "index.html",
        results=results,
        query=query,
        stats=stats,
        search_time=search_time
    )


if __name__ == "__main__":
    app.run(debug=True)