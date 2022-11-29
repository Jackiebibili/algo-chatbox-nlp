from pathlib import Path
from haystack.pipelines import Pipeline
# from haystack.utils import print_answers

query_threshold = 0.5
low_confidence_answer = "Could you please enter something else? I couldn't understand."

p_ensemble = Pipeline.load_from_yaml(Path("nlp_pipeline.yaml"))


def query(q: str):
   global p_ensemble, query_threshold, low_confidence_answer
   res = p_ensemble.run(query=q)
   top_ans = res["answers"][0] # type: ignore
   ans_text = ""
   if top_ans.score < query_threshold:
      ans_text = low_confidence_answer
   else:
      ans_text = top_ans.answer
   return ans_text
