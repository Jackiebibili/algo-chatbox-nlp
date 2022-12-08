import os
# Google introduced an incompatibility into protobuf-4.21.0
# that is not backwards compatible with many libraries.  
# Once those libraries have updated to rebuild their _pb2.py files,
# this can be removed.
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from tensorflow import keras
import tensorflow_text as text
from ...tools.math_expr_comparable import get_ordered_functions_growth_rate
import re
import subprocess

threshold = 0.5

# train the model
subprocess.run(["python3", "src/haystack/pipeline/train_comp_model.py"])

# load the model
model_load = keras.models.load_model('src/haystack/pipeline/comp_nn_model')

def find_functions(query: str)->list[str]:
   # extract function expressions from the query text
   def repl(match: re.Match):
      m = match.group(0)
      return m[2:-1]
   query = re.sub(r"O\((?:\([^()]*\)|[^()])*\)", repl, query)
   return re.findall(r"\$([^\$]+)\$", query)


# def classify_comp_query_batch(queries: list[str]):
#    return model_load.predict(queries)

def classify_comp_query(query):
   return model_load.predict([query])[0][0]


# def classify_comp_query(query):
#    return 0.6

def classify_query(query):
   return classify_comp_query(query) >= threshold

def compute_result(query):
   fns = find_functions(query)
   try:
      ans = ", ".join(list(map(lambda x: f"$O({x})$", get_ordered_functions_growth_rate(fns))))
      ans = "Compared functions in ascending order: " + ans
      return ans
   except Exception as ex :
      return str(ex)
