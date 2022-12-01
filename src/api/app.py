from flask import Flask, request
from ..haystack.pipeline.pipeline import query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/qna")
def qna():
   q = request.args.get("question")
   if q is None:
      return "Question cannot be null.", 400
   return {"answer": query(q)}

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080)