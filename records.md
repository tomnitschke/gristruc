Stuff for working with records in Grist. See [here](https://github.com/tomnitschke/gristruc/blob/main/README.md) for instructions on how to use.
```python
from grist import UserTable, Record
from docmodel import global_docmodel as gdm

class Record:
  @classmethod
  def create(cls, table: UserTable, fields: dict=None) -> Record:
    """Create a record in 'table' and optionally fill it with the values given in 'fields', then
    return the new record.
    
    Arguments:
    table      The table. Should be of type UserTable, which is what Grist gives you when you just
               type the name of a valid table in a formula.
    fields     A dict of layout {column_name: value_to_put} specifying how to fill out the newly
               created record. Defaults to None, for an empty record.
    """
    fields = fields or {}
    return next((r for r in gdm.add(table, **fields)), None)
  
  @classmethod
  def update(cls, record: Record, fields: dict) -> None:
    """Update 'record' according to 'fields'. The latter must be a dict of layout {column_name: value_to_put}."""
    gdm.update([record], **fields)
  
  @classmethod
  def get_fields(cls, record: Record, include_internals: bool=False) -> list[str]:
    """
    Get all fields/aka column names from a 'record'.
    This excludes Grist-internal invisible columns like "manualSort" unless 'include_internals' is set to True.
    """
    return [field for field in dir(record) if include_internals or (not field.startswith(("#","_","gristHelper_")) and not field in ("id", "manualSort"))]


return Record
```
