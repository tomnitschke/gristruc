Stuff for working with records in Grist. See [here](https://github.com/tomnitschke/gristruc/blob/main/README.md) for instructions on how to use.
```
import json
from grist import Record

class WidgetOptions:
  @classmethod
  def get(cls, colrec: Record) -> dict:
    """
    Get the widget options for a column. These are where most settings from the creator panel, e.g. the column type,
    currency symbol to use, number of decimals to show, and so on, are stored.
    
    Arguments:
    colrec       The record from _grist_Tables_column representing the column in question.
                 You can obtain it by doing _grist_Tables_column.lookupRecords(tableId="table_name_goes_here", colId="column_name_goes_here").
    """
    try:
      return json.loads(getattr(colrec, "widgetOptions", "{}"))
    except:
      return {}
  
  @classmethod
  def set(cls, colrec: Record, widget_options: dict) -> None:
    """
    Set the widget options for a column. See above get() method for details.
    
    Arguments:
    colrec          See get(), above.
    widget_options  A dictionary containing the widget options. Keys and values must be such that Grist knows how to interpret
                    them, otherwise things will break in weird ways.
    """
    if not isinstance(widget_options, dict):
      raise ValueError(f"widget_options must be a dict, not {type(widget_options)}.")
    try:
      widget_options_json = json.dumps(widget_options)
      return $Record.update(colrec, {"widgetOptions": widget_options_json})
    except:
      pass
  
  @classmethod
  def update_item(cls, colrec: Record, item_name: str, item_val: object) -> None:
    """
    Update a specific widget option item to a new value. See above get() and set() for details.
    """
    widget_options = cls.get(colrec)
    widget_options[item_name] = item_val
    return cls.set(colrec, widget_options)



return WidgetOptions
```
