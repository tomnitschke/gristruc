# Paste below into a formula column called 'ColumnMeta'.

from grist import UserTable
from column import BaseColumn

class ColumnMeta:
  @classmethod
  def get(cls, table: UserTable|str=None, column_name: str=None) -> BaseColumn:
    """Get a column meta object from the given 'table' by 'column_name'."""
    if not table or not column_name:
      current_table, current_column_name, _, _, _ = $get_current_node()
      table = table if table else current_table
      column_name = column_name if column_name else current_column_name
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    table = table if isinstance(table, UserTable) else $Table.get(table_name=table)
    try:
      return table.table.get_column(column_name)
    except KeyError:
      raise KeyError(f"No such column '{column_name}' on table '{table.table.table_id}'.")
  
  @classmethod
  def get_all(cls, table: UserTable|str=None) -> list[BaseColumn]:
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    table = table if isinstance(table, UserTable) else $Table.get(table_name=table)
    return [col for col in table.table.all_columns.values() if not col.col_id.startswith(("#", "_", "gristHelper")) and not col.col_id in ("id", "manualSort")]


return ColumnMeta
