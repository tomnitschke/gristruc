Stuff for working with relations in Grist. See [here](https://github.com/tomnitschke/gristruc/blob/main/README.md) for instructions on how to use.
```python
from grist import Record, RecordSet, UserTable

class Relation:
  @classmethod
  def get_referring_columns(cls, record: Record, table_to_query: UserTable) -> list[Record]:
    """In the 'table_to_query', find all reference/reference list-type columns that refer to 'record'."""
    target_table = record._table
    result = []
    foreign_table_name = table_to_query.table.table_id
    for colrec in $Column.get_all(table_to_query):
      if not colrec.type in (f"Ref:{target_table.table_id}", f"RefList:{target_table.table_id}"):
        continue
      result.append(colrec)
    return result

  @classmethod
  def get_referrers(cls, record: Record, table_to_query: UserTable=None, make_flat: bool=False) -> dict|list[Record]:
    """
    Across all tables, for optionally just the 'table_to_query', find all records that refer to 'record'.
    Returns a dictionary of layout {referring_table_name: {referring_column_name: [referring_record_0, referring_record_1, ...]}}.
    Alternatively, if 'make_flat' is True, return a flat list of referring records.
    """
    result = [] if make_flat else {}
    for foreign_table in $Table.get_all() if not table_to_query else [table_to_query]:
      foreign_table_name = foreign_table.table.table_id
      for referring_col in cls.get_referring_columns(record, foreign_table):
        referring_col_name = referring_col.colId
        referring_recs = list(foreign_table.lookupRecords(**{referring_col_name: record.id}) or foreign_table.lookupRecords(**{referring_col_name: CONTAINS(record.id)}))
        if make_flat:
          result += [r for r in referring_recs if not r in result]
          continue
        if not foreign_table_name in result:
          result[foreign_table_name] = {}
        result[foreign_table_name][referring_col_name] = referring_recs
    return result
  
  @classmethod
  def get_referring_records(cls, record: Record, table_to_query: UserTable=None) -> list[Record]:
    """Alias for the above get_referrers() but with 'make_flat' = True."""
    return cls.get_referrers(record, table_to_query, make_flat=True)
        



return Relation
```
