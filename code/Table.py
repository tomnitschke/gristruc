# Paste below into a formula column called 'Table'.

import useractions
from grist import UserTable
from table import Table
from docmodel import global_docmodel as gdm

class Table:
  @classmethod
  def get(cls, table_name: str) -> UserTable:
    """Get a table (i.e. a Grist 'UserTable' object) by 'table_name'."""
    try:
      return gdm.get_table(table_name)
    except KeyError:
      raise KeyError(f"No such table '{table_name}'.")
  
  @classmethod
  def get_all(cls, exclude_internal: bool=True, exclude_uppercase: bool=True) -> list[UserTable]:
    """
    Get all tables in the document. By default, Grist-internal tables as well as tables named in all caps are excluded.
    Optionally, include these by setting any of 'exclude_internal' or 'exclude_uppercase' to False.
    """
    return [t.user_table for t in gdm._engine.tables.values() if not (exclude_internal and t.table_id.startswith("_")) and not (exclude_uppercase and t.table_id.isupper())]
  
  @classmethod
  def get_name(cls, table: UserTable=None) -> str:
    """Get the name of a 'table' (i.e. Grist UserTable object). Can be called without arguments to get the current table's name."""
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable):
      raise ValueError(f"table must be a UserTable, not {type(table)}.")
    return table.table.table_id
  
  #@classmethod
  #def create(cls, table_name: str, columns: list[dict]=None, should_be_visible: bool=False) -> UserTable:
  #  columns = columns if columns else [{'id': None, 'isFormula': True}]
  #  if not isinstance(columns, list|tuple) or not isinstance(columns[0], dict):
  #    raise ValueError(f"columns must be a list of dicts, where each has the format {{col_info_attribute: value}}")
  #  for i in range(len(columns)):
  #    columns[i]["id"] = None
  #    columns[i]["isFormula"] = True
  #  resulting_table_id, resulting_table_name, resulting_table_columns = gdm._engine.user_actions.doAddTable(table_name, columns, manual_sort=True, primary_view=should_be_visible, raw_section=True, record_card_section=True)

return Table
