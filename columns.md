Stuff for working with columns in Grist. See [here](https://github.com/tomnitschke/gristruc/blob/main/README.md) for instructions on how to use.
```
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
  def get_all(cls, table: UserTable|str) -> RecordSet:
    """Get all columns in the given 'table'."""
    table_name = table if isinstance(table, str) else (table.table if isinstance(table, UserTable) else table).table_id
    return _grist_Tables_column.lookupRecords(tableId=table_name)



return Column
```
