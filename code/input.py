import ast, re
from types import FunctionType
from grist import UserTable, Record, RecordSet
from objtypes import AltText

class Input:
  @classmethod
  def create_ref_from_input(cls, input: AltText|str|Record, table: UserTable|str=None, field_name: str="", fields: dict=None, input_processing_cb: FunctionType=None, prevent_doublets: bool=False, fields_for_doublet_check: dict=None) -> Record:
    """
    Transform raw string input into a value acceptable for putting into reference-type columns by creating a linked record according to the input if no such record exists.
    
    Background information: In a reference-type column, selecting a valid option from the dropdown menu produces input of type Record. Typing something invalid into the cell
    will produce an AltText containing the input as a string instead. This is used here to create missing linked records as necessary.
    
    Arguments:
    input                      The user input.
    table                      The table that we should create any missing linked records in. Leave empty to reference the current table.
    field_name                 When a linked record is created, this specifies the name of the column in 'table' that should get filled with 'input'. Can be left out to create an empty linked record.
    fields                     A dict of layout {name: value} specifying which other columns to fill out, and with what values, on newly created records. Can be left out to create an empty linked record.
                               Specifying a string with just an asterisk inside like "*" for a value will cause that value to be replace by 'input'.
                               Providing a callable instead of a value will cause that callable to get called with the value as argument, and the result used as final value.
                               Note: If there are any such callables here but an 'input_processing_cb', below, is also set, then both will get called but the latter will run first.
    input_processing_cb        A callback function to operate on user input before it gets written to any newly created record. The function takes one parameter, the user input
                               as a string. It should return the processed/cleaned up value.
    prevent_doublets           When creating records, first check existing records' fields - as specified by 'field_name' and 'fields', above - for identical data. If any are
                               found, link to those instead of creating new ones.
    fields_for_doublet_check   Dictionary like 'fields', above, containing all the columns and values to consider when doing a doublet check. Has no effect if 'prevent_doublets'
                               is False. Defaults to using the same fields as specified through 'field_name' or 'fields', above.
    """
    if not input or not isinstance(input, AltText|str):
      return input
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    input = str(input)
    input = input_processing_cb(input) if input_processing_cb else input
    fields = fields or {}
    if field_name:
      fields[field_name] = "*"
    fields = cls._prepare_fields_dict(input, fields)
    fields_for_doublet_check = cls._prepare_fields_dict(input, fields_for_doublet_check or fields)
    if prevent_doublets and (existing_record := table.lookupOne(**fields_for_doublet_check)):
      return existing_record
    return $Record.create(table, fields) or None
  
  #@classmethod
  #def create_ref_from_this(cls, table: UserTable, field_name: str="", fields: dict=None, input_processing_cb: FunctionType=None, prevent_doublets: bool=False, fields_for_doublet_check: dict=None) -> Record:
  #  _, _, last_input = $get_current_node()
  #  return cls.create_ref_from_input(input=last_input, table=table, field_name=field_name, fields=fields, input_processing_cb=input_processing_cb, prevent_doublets=prevent_doublets, fields_for_doublet_check=fields_for_doublet_check)

  @classmethod
  def create_reflist_from_input(cls, input: AltText|str|RecordSet, table: UserTable|str=None, field_name: str="", fields: dict=None, input_processing_cb: FunctionType=None, list_sep_regex: str=";", prevent_doublets: bool=False, fields_for_doublet_check: dict=None) -> list[Record]:
    """
    Transform raw string input into a value acceptable for putting into reference list-type columns by creating linked records according to the input if no such records exist.
    
    Background information: In a reference list-type column, selecting a valid option from the dropdown menu produces input of type RecordSet. Typing something invalid into the cell
    will produce an AltText instead, containing the input as a string representation of a list of record IDs plus the recently added user input values.
    This function attempts to parse the latter as an actual list, then filter out the items that are new and create the missing linked records for them. Finally, a list of valid
    Records will be returned (which a reference list-type column will accept just like a proper RecordSet).
    
    Arguments:
    input                      The user input.
    table                      The table that we should create any missing linked records in. Leave empty to reference the current table.
    field_name                 When a linked record is created, this specifies the name of the column in 'table' that should get filled with 'input'.
    fields                     A dict of layout {name: value} specifying which other columns to fill out, and with what values, on newly created records.
                               Specifying a string with just an asterisk inside like "*" for a value will cause that value to be replace by 'input'.
                               Providing a callable instead of a value will cause that callable to get called with the value as argument, and the result used as final value.
                               Note: If there are any such callables here but an 'input_processing_cb', below, is also set, then both will get called but the latter will run first.
    input_processing_cb        A callback function to operate on user input before it gets written to any newly created record. The function takes one parameter, the user input
                               as a string. It should return the processed/cleaned up value.
    list_sep_regex             Character or search pattern to split user input up by. This allows users to enter things like "one; two" into the cell and have that create two
                               records "one" and "two" rather than just one "one; two" on the 'table'.
    prevent_doublets           When creating records, first check existing records' fields - as specified by 'field_name' and 'fields', above - for identical data. If any are
                               found, link to those instead of creating new ones.
    fields_for_doublet_check   Dictionary like 'fields', above, containing all the columns and values to consider when doing a doublet check. Has no effect if 'prevent_doublets'
                               is False. Defaults to using the same fields as specified through 'field_name' or 'fields', above.
    """
    if not input or not isinstance(input, AltText|str):
      return input
    if not table:
      table, _, _, _, _ = $get_current_node()
    if not isinstance(table, UserTable|str):
      raise ValueError(f"table must be a UserTable or str, not {type(table)}.")
    fields = fields or {}
    if field_name:
      fields[field_name] = "*"
    inputlist = cls.sanitize_reflist_input(input, input_processing_cb=input_processing_cb, list_sep_regex=list_sep_regex)
    reflist = []
    records_to_create = []
    for item in inputlist:
      if isinstance(item, int):
        reflist.append(item)
        continue
      fields_for_this_item = cls._prepare_fields_dict(item, fields)
      fields_for_doublet_check_for_this_item = cls._prepare_fields_dict(item, fields_for_doublet_check or fields)
      if prevent_doublets and (existing_record := table.lookupOne(**fields_for_doublet_check_for_this_item)):
        reflist.append(existing_record)
        continue
      records_to_create.append((table, fields_for_this_item))
    for info in records_to_create:
      reflist.append($Record.create(info[0], info[1]))
    return reflist or None
  
  #@classmethod
  #def create_reflist_from_this(cls, table: UserTable, field_name: str="", fields: dict=None, input_processing_cb: FunctionType=None, list_sep_regex: str=";", prevent_doublets: bool=False, fields_for_doublet_check: dict=None) -> list[Record]:
  #  _, _, last_input = $get_current_node()
  #  return cls.create_reflist_from_input(input=last_input, table=table, field_name=field_name, fields=fields, input_processing_cb=input_processing_cb, list_sep_regex=list_sep_regex, prevent_doublets=prevent_doublets, fields_for_doublet_check=fields_for_doublet_check)
  
  @classmethod
  def sanitize_reflist_input(cls, input: AltText|str|RecordSet, input_processing_cb: FunctionType=None, list_sep_regex: str=";") -> list[str|int]:
    """
    Transform garbage data in a reference list-type column, as caused by invalid user input, into a clean list of valid record IDs
    (representing those items in the reference list that were properly selected using the dropdown menu) and strings of invalid data
    (representing that which the user added by just typing into the cell).
    
    Arguments:
    input                   The user input.
    input_processing_cb     A callback function to operate on the user input before it gets added to the results list.
                            The function takes one parameter, the user input as a string. It should return the processed/cleaned up value.
    list_sep_regex          Character or search pattern to split user input up by. This allows users to enter things like "one; two" into the cell
                            and have that appear as two items "one" and "two", rather than just "one; two", on the results list.
    """
    if not input or not isinstance(input, AltText|str):
      return list(input) if input else []
    input = str(input)
    try:
      input_list = cls.parse_listrepr(input)
    except:
      input_list = [input]
    result = []
    for entry in input_list:
      if isinstance(entry, int):
        result.append(entry)
        continue
      items = re.split(re.escape(list_sep_regex), entry)
      result += [input_processing_cb(item) for item in items] if input_processing_cb else items
    return result

  @classmethod
  def _prepare_fields_dict(cls, input: object, fields: dict) -> dict:
    """
    Helper function to replace the special "*" value and apply any callables to values in a column-to-value specification.
    See create_ref_from_input() or create_reflist_from_input() for details.
    """
    result = {}
    #return {key: input if val == "*" else val for key, val in fields.items()}
    for key, val in fields.items():
      if isinstance(val, FunctionType):
        try:
          result[key] = val(input)
          continue
        except:
          pass
      if val == "*":
        result[key] = input
      else:
        result[key] = val
    return result

  @classmethod
  def parse_listrepr(cls, input: str) -> list:
    """
    Parse a string that looks like a Python list into an actual Python list.
    """
    input = str(input)
    try:
      return ast.literal_eval(input)
    except:
      raise ValueError(f"Input '{input}' can't be parsed as a list.")
  
  @classmethod
  def make_input_a_valid_choice(cls, input: str|list|tuple, column: Record=None, prune_unused_items: bool=False) -> str:
    """
    For choice fields, add the input to the list of valid choices (if it's not already there) of column 'column'.
    Leave 'column' empty to reference the current calling column.
    Optionally 'prune_unused_items' from the list of choices. Note that this will check all records in the table 'column'
    belongs to, so it can be an expensive operation if the table is large.
    """
    is_input_a_str = isinstance(input, str)
    $ColumnOptions.add_choice(column=column, item=input, prune_unused_items=prune_unused_items)
    return input if is_input_a_str else input[0]
  
  #@classmethod
  #def make_this_a_valid_choice(cls, prune_unused_items: bool=False) -> str:
  #  current_table, current_column_name, last_input = $get_current_node()
  #  return cls.make_input_a_valid_choice(input=last_input, colrec=$Column.get(current_table, current_column_name), prune_unused_items=prune_unused_items)



return Input
