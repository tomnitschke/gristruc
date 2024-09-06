Stuff for working with tables in Grist. See [WIP: HERE] for instructions on how to use these.

```
from grist import UserTable
from docmodel import global_docmodel as gdm

class Table:
  @classmethod
  def get(cls, name: str) -> UserTable:
    """Get a UserTable by name.
    Note: You can turn a UserTable into a Table by doing 'your_usertable_here.table'.
    """
    try:
      return gdm.get_table(name)
    except KeyError:
      raise KeyError(f"No such table '{name}'.")
  
  @classmethod
  def get_all(cls, exclude_internal: bool=True, exclude_uppercase: bool=True) -> list[UserTable]:
    """Get all UserTables in the document. By default, Grist-internal tables as well as tables named in all caps are excluded.
    Note: You can turn a UserTable into a Table by doing 'your_usertable_here.table'.
    """
    return [x.user_table for x in gdm._engine.tables.values() if not (exclude_internal and x.table_id.startswith("_")) and not (exclude_uppercase and x.table_id.isupper())]



return Table
```
