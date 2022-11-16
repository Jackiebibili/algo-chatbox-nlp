from typing import Callable


def pipe(init_input, fns: list[Callable]):
   fn_res = init_input
   for fn in fns:
      fn_res = fn(fn_res)
   return fn_res
