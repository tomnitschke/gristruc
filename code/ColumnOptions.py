# Paste below into a formula column called 'ColumnOptions'.

import json
from grist import Record

class ColumnOptions:
  @classmethod
  def get(cls, column: Record=None) -> dict:
    """
    Get the column options for 'column'. These are where most settings from the creator panel, e.g. the column type,
    currency symbol to use, number of decimals to show, and so on, are stored.
    """
    if column is None:
      column = $Column.get()
    try:
      return json.loads(getattr(column, "widgetOptions", "{}"))
    except:
      return {}

  @classmethod
  def set(cls, column: Record=None, *, options: dict) -> None:
    """
    For 'column', sets column options to 'options'. This will replace all currently configured
    column options with those specified in 'options'. The latter must be a dict, and keys and values
    must be such that Grist knows how to interpret them, otherwise things will break in weird ways.
    """
    if column is None:
      column = $Column.get()
    if not isinstance(options, dict):
      raise ValueError(f"options must be a dict, not {type(options)}.")
    options_json = "{}"
    try:
      options_json = json.dumps(options)
    except:
      raise ValueError(f"Can't decode column options for column '{column.colId}' from JSON. This shouldn't normally happen. It might be a good idea to delete and remake the column from scratch.")
    try:
      return $Record.update(record=column, fields={"widgetOptions": options_json})
    except:
      raise

  @classmethod
  def get_option(cls, column: Record=None, *, option: str) -> object:
    """
    For 'column', get a specific column 'option'. Returns None if no such option exists.
    """
    co = cls.get(column)
    return co.get(option, None)
  
  @classmethod
  def set_option(cls, column: Record=None, *, option: str, value: object) -> None:
    """
    For 'column', update a specific column 'option' to a new 'value'.
    """
    if column is None:
      column = $Column.get()
    co = cls.get(column=column)
    co[option] = value
    return cls.set(column=column, options=co)
  
  @classmethod
  def add_choice(cls, column: Record=None, *, item: str|list|tuple, prune_unused_items: bool=False) -> bool:
    """
    For the choice/choice list 'column', add a new 'item' (or a list of items) to the list of allowable choices.
    Returns True if any items were added (i.e. didn't already exist), otherwise False.
    Optionally 'prune_unused_items' from the list of choices. Note that this will check all records in the table 'column'
    belongs to, so it can be an expensive operation if the table is large.
    """
    if not item:
      return False
    item = [item] if isinstance(item, str) else item
    if column is None:
      column = $Column.get()
    choices = cls.get_option(column, option="choices") or []
    is_choicelist_column = $Column.get_type(column) == "ChoiceList"
    if prune_unused_items:
      choices = []
      for val in PEEK(getattr($Table.get(column.tableId).all, column.colId)):
        values = val if is_choicelist_column else [val]
        for v in values:
          if v and not v in choices:
            choices.append(val)
    were_any_items_added = False
    for v in item:
      if v and not v in choices:
        choices.append(v)
        were_any_items_added = True
    if were_any_items_added or prune_unused_items:
      cls.set_option(column=column, option="choices", value=choices)
      return True
    return False



return ColumnOptions
