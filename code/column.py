import useractions
from grist import UserTable, Record, RecordSet
from docmodel import global_docmodel as gdm

class Column:
  @classmethod
  def get(cls, table: UserTable|str=None, column_name: str=None) -> Record:
    """
    Get a column from 'table' by 'name'.
    This is functionally equivalent to doing _grist_Tables_column.lookupOne(tableId=table.table.table_id, colId=name),
    but is more readable and comes with a nicer error message if something goes wrong.
    
    Args:
      table: The table (or its name) to get the column from.
      column_name: The name of the column.
    
    Returns:
      The record from _grist_Tables_column that matches the requested table and column name.
    
    For convenience, this function may be called without arguments in order to reference the current calling column itself.
    """
    if not table or not column_name:
      current_table, current_column_name, _, _, _ = $get_current_node()
      table = table if table else current_table
      column_name = column_name if column_name else current_column_name
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    table = table if isinstance(table, UserTable) else $Table.get(table_name=table)
    table_name = table.table.table_id
    try:
      return gdm.get_column_rec(table_name, column_name)
    except KeyError:
      raise KeyError(f"No such column '{column_name}' on table '{table_name}'.")
  
  @classmethod
  def get_all(cls, table: UserTable|str=None, get_as_names: bool=False, include_internal: bool=False) -> RecordSet:
    """
    Get all columns in the given 'table'.
    Optionally get just the column names ('get_as_names' = True).
    Optionally also 'include_internal' like 'manualSort' and the like.
    For convenience, this function may be called without the 'table' argument in order to get all columns of the current table.
    """
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    table_name = table if isinstance(table, str) else (table.table if isinstance(table, UserTable) else table).table_id
    columns = _grist_Tables_column.lookupRecords(tableId=table_name)
    return [(cr.colId if get_as_names else cr) for cr in columns if include_internal or (not cr.colId.startswith(("#","_","gristHelper_")) and not cr.colId in ("id", "manualSort"))]
  
  @classmethod
  def get_type(cls, column: Record=None) -> str:
    if not column:
      column = cls.get()
    if not isinstance(column, Record|column._table.Record):
      raise ValueError(f"column must be a column, not {type(column)}.")
    return column.type
  
  @classmethod
  def create(cls, table: UserTable|str=None, column_name: str=None, col_info: dict=None, should_be_visible: bool=False) -> tuple[int, str]:
    col_info = col_info if col_info else {"type": "Any", "isFormula": False}
    column_name = "" if not column_name and not column_name is None else column_name
    if not table or not column_name:
      current_table, current_column_name, _, _, _ = $get_current_node()
      table = table if table else current_table
      column_name = column_name if not column_name is None else current_column_name
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    if not isinstance(column_name, str):
      raise ValueError(f"column_name must be a str, not {type(column_name)}.")
    if not isinstance(col_info, dict):
      raise ValueError(f"col_info must be a dict, not {type(col_info)}.")
    col_info["type"] = col_info.get("type", "Any")
    col_info["isFormula"] = col_info.get("isFormula", False)
    col_info["formula"] = col_info.get("formula", "")
    #return table.table.table_id, column_name, col_info
    # Returns int col_ref and str col_name for the newly created column.
    action = "AddVisibleColumn" if should_be_visible else "AddColumn"
    return getattr(gdm._engine.user_actions, action)(table.table.table_id, column_name, col_info)
    #return gdm._engine.user_actions.AddColumn(table.table.table_id, column_name, col_info)



return Column
