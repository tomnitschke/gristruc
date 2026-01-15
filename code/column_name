# Paste below into a formula column called 'column_name'.

def column_name(fstring_expression_equal:str, item=1)->str:
  """
  Get a referenced column's name (ID) while maintaining Grist dependencies (i.e. survives a column rename & ID change).

  Usage:
    LIB.lookupOne().column_name(f"{ $AnyColumn = }")

  Insights:
  f-string must evaluate the expression in the calling block, because the expression changes on block change.
  Spaces inside the f-string are optional.
  `$AnyColumn` and `rec.AnyColumn` are identical (Grist always translates former to latter).
  Item `1` corresponds to pattern `rec.AnyColumn = ...`. Use items `2`+ to access referenced record's columns.
  """
  return fstring_expression_equal.replace(".", " ").replace("=", " ").split()[item]

return column_name
