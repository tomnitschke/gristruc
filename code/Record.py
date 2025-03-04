# Paste below into a formula column called 'Record'.

from grist import UserTable, Record
from engine import OrderError
from docmodel import global_docmodel as gdm

class Record:
  @classmethod
  def create(cls, table: UserTable|str=None, fields: dict=None) -> Record:
    """Create a record in 'table' and optionally fill it with the values given in 'fields', then
    return the new record.
    
    Arguments:
    table      The table. Should be of type UserTable, which is what Grist gives you when you just
               type the name of a valid table in a formula. Leave empty to reference the current table.
    fields     A dict of layout {column_name: value_to_put} specifying how to fill out the newly
               created record. Defaults to None, for an empty record.
    """
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    table = table if isinstance(table, UserTable) else $Table.get(table_name=table)
    fields = fields or {}
    try:
      return next((r for r in gdm.add(table, **fields)), None)
    except OrderError as e:
      raise ValueError(f"Record.create() encountered an OrderError. This typically happens when using it to fill in the value for (perhaps among others) a column that is set up as an 'Empty Column' in Grist. Set all such columns to be 'Data Columns' instead and the error should go away. The offending column here may be {e.node} at row {e.row_id}.")
  
  @classmethod
  def update(cls, record: Record=None, *, fields: dict) -> None:
    """
    Update 'record' according to 'fields'. Leave 'record' empty to reference the current record.
    'fields' must be a dict of layout {column_name: value_to_put}.
    """
    if record is None:
      _, _, record, _, _ = $get_current_node()
    if not isinstance(record, Record|record._table.Record):
      raise ValueError(f"record must be a Record, not {type(record)}.")
    try:
      gdm.update([record], **fields)
    except OrderError as e:
      raise ValueError(f"Record.update() encountered an OrderError. This typically happens when using it to update (perhaps among others) a column that is set up as an 'Empty Column' in Grist. Set all such columns to be 'Data Columns' instead and the error should go away. The offending column here may be {e.node} at row {e.row_id}.")
  
  @classmethod
  def get_fields(cls, record: Record|UserTable=None, include_internal: bool=False) -> list[str]:
    """
    Get all fields (a.k.a. column names) from 'record', which is typically a Record but can also be a UserTable.
    If it is a UserTable, no dependency will be created, i.e. if a new column is added to said table, the formula using
    this method won't reflect that automatically.
    Leave 'record' empty to reference the current record.
    This excludes Grist-internal invisible columns like "manualSort" unless 'include_internal' is set to True.
    """
    if record is None:
      _, _, record, _, _ = $get_current_node()
    try:
      table = record._table
    except AttributeError:
      try:
        table = record.table
        record = table.Record
      except AttributeError:
        raise ValueError(f"record must be a Record or UserTable, not {type(record)}.")
    # NB: This effectively does the same as $Column.get_all(), but is preferred here because it should be less expensive.
    return [field for field in dir(record) if include_internal or (not field.startswith(("#","_","gristHelper_")) and not field in ("id", "manualSort"))]
  
  @classmethod
  def as_dict(cls, record: Record, include_internal: bool=False, do_peek: bool=False, include_only_fields: list[str]=None) -> dict[str, object]:
    if record is None:
      _, _, record, _, _ = $get_current_node()
    result = {}
    for field_name in cls.get_fields(record):
      if not include_only_fields or field_name in include_only_fields:
        result[field_name] = PEEK(getattr(record, field_name)) if do_peek else getattr(record, field_name)
    return result
  
  @classmethod
  def remove(cls, record: Record) -> None:
    return gdm.remove([record])



return Record
