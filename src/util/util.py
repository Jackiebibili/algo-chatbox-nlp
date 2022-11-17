import re
from typing import Callable
from urllib.parse import quote

def pipe(init_input, fns: list[Callable]):
   fn_res = init_input
   for fn in fns:
      fn_res = fn(fn_res)
   return fn_res

def convert_filename(filename: str, ext=".txt"):
   regex = re.compile(r"\s+")
   name = regex.sub('__', filename)
   return name+ext
   