from flask import Flask, request
from ..haystack.pipeline.pipeline import query
from flask_cors import CORS
from ..haystack.pipeline.load_comp_model import classify_query, compute_result

app = Flask(__name__)
CORS(app)

@app.route("/api/qna")
def qna():
   q = request.args.get("question")
   # classification
   if classify_query(q):
      return {"answer": compute_result(q)}
   # normal query
   if q is None:
      return "Question cannot be null.", 400
   return {"answer": query(q)}

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080)