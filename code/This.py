# Paste below into a formula column called 'This'.

import inspect
from types import FunctionType
from grist import UserTable, Record, RecordSet
from objtypes import AltText

class IsFormulaError(ValueError):
  def __init__(self):
    fn = "This function"
    try:
      fn = inspect.stack()[1].function
    except:
      pass
    super().__init__(f"Current column is a formula column. '{fn}' works only when used from trigger formulas.")



class ThisMeta(type):
  def __repr__(cls):
    return "The 'This' class can't be used statically. Make an instance with 'This()' instead."



class This(metaclass=ThisMeta):
  def __init__(self):
    self._node_info = None
    self._column = None
  
  def _update_node_info(self):
    if self._node_info is None:
      current_table, current_column_name, current_record, is_formula, last_input = $get_current_node()
      self._node_info = {
        "table": current_table,
        "column_name": current_column_name,
        "record": current_record,
        "is_formula": is_formula,
        "last_input": last_input,
      }
  
  def __getattr__(self, key):
    self._update_node_info()
    return self._node_info[key]
  
  @property
  def column(self):
    if self._column is None:
      self._column = $Column.get(self.table, self.column_name)
    return self._column
  
  @property
  def options(self):
    return $ColumnOptions.get(self.column)
  
  @property
  def info(self):
    self._update_node_info()
    return self._node_info | {
      "column": self.column,
      "options": self.options,
      "referrers": $Relation.get_referrers(self.record),
    }



return This
