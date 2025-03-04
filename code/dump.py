# Paste below into a formula column called 'dump'.

import inspect
from pprint import pformat

def dump(obj: object) -> str:
  return pformat({key: val for key, val in inspect.getmembers(obj)})



return dump
