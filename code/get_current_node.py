# Paste below into a formula column called 'get_current_node'.

import grist
import inspect

def get_current_node() -> str:
  stack = inspect.stack()
  starting_stack_level = 0
  for level in range(len(stack)-1, -1, -1):
    current = stack[level]
    current_table = current.frame.f_locals.get("table", None)
    last_input = current.frame.f_locals.get("value", None)
    current_record = current.frame.f_locals.get("rec", None)
    if isinstance(current_table, grist.UserTable) and not current_table.table.table_id.startswith("_"):
      current_column = current.function
      is_formula = True
      if current_column.startswith("_default_"):
        current_column = current_column[len("_default_"):]
        is_formula = False
      return current_table, current_column, current_record, is_formula, last_input
  return None, None, None, None



return get_current_node
