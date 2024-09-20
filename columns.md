Stuff for working with columns in Grist. See [here](https://github.com/tomnitschke/gristruc/blob/main/README.md) for instructions on how to use.
```python
from grist import UserTable, Record, RecordSet
from docmodel import global_docmodel as gdm

class Column:
  @classmethod
  def get(cls, table: UserTable, name: str) -> Record:
    """
    Get a column from 'table' by 'name'.
    This is functionally equivalent to just doing _grist_Tables_column.lookupOne(tableId=table.table.table_id, colId=name),
    but more readable and with a nicer error message if something goes wrong.
    """
    if not isinstance(table, UserTable):
      raise ValueError(f"table must be a UserTable, not {type(table)}.")
    try:
      return gdm.get_column_rec(table.table.table_id, name)
    except KeyError:
      raise KeyError(f"No such column '{name}' on table '{table.table.table_id}'.")
  
  @classmethod
  def get_all(cls, table: UserTable|str, get_as_names: bool=False, include_internals: bool=False) -> RecordSet:
    """Get all columns in the given 'table'."""
    table_name = table if isinstance(table, str) else (table.table if isinstance(table, UserTable) else table).table_id
    colrecs = _grist_Tables_column.lookupRecords(tableId=table_name)
    return [(cr.colId if get_as_names else cr) for cr in colrecs if not cr.colId.startswith(("#","_","gristHelper_")) and not cr.colId in ("id", "manualSort")]
    



return Column
```
