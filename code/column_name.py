# Paste below into a formula column called 'tracked_name'.

def tracked_name(self_documenting_fstring_expression):
  """
  Get the name of a column, table, or both, such that it stays up to date when said column or table gets renamed by the user.
  Args:
    self_documenting_fstring_expression:  An f-string expression where you give the names of a column or table as they currently are.
                                          This makes use of f-strings' self-documenting syntax and should look like this (note the equal sign):
                                          f"{SomeTable=}"                          returns "SomeTable", but if said table gets renamed, will return the new name instead.
                                          f"{$SomeColumn=}"                        returns "SomeColumn", but if said column gets renamed, will return the new name instead.
                                          f"{SomeTable.lookupOne().SomeColumn=}"   returns ["SomeTable", "SomeColumn"], or their respective new names if the table or the column get renamed.
  """
  if '=' in self_documenting_fstring_expression:
    left, right = self_documenting_fstring_expression.split('=')
    left_parts = left.split('.')
    if len(left_parts) == 1:
      return left_parts[0]
    if len(left_parts) == 2:
      return left_parts[1]
    if len(left_parts) == 3 and left_parts[1].startswith('lookupOne'):
      return left_parts[0], left_parts[2]
  raise ValueError(f"Passed f-string expression doesn't match any of the supported formats (or isn't the result of an f-string expression to begin with): '{self_documenting_fstring_expression}'. See docs for which formats are supported.")

return tracked_name
