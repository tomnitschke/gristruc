# Paste below into a formula column called 'Relation'.

from grist import Record, RecordSet, UserTable

class Relation:
  @classmethod
  def get_referring_columns(cls, record: Record=None, *, table_to_query: UserTable) -> list[Record]:
    """
    In the 'table_to_query', find all reference/reference list-type columns that refer to 'record'.
    """
    if record is None:
      _, _, record, _, _ = $get_current_node()
    if not isinstance(record, Record|record._table.Record):
      raise ValueError(f"record must be a Record, not {type(record)}.")
    target_table = record._table
    result = []
    foreign_table_name = table_to_query.table.table_id
    for column in $Column.get_all(table=table_to_query):
      if not column.type in (f"Ref:{target_table.table_id}", f"RefList:{target_table.table_id}"):
        continue
      result.append(column)
    return result

  @classmethod
  def get_referrers(cls, record: Record=None, tables_to_query: list[UserTable]=None, make_list: bool=False) -> dict|list[Record]:
    """
    Across all tables, for optionally just the 'tables_to_query', find all records that refer to 'record'.
    Returns a dictionary of layout {referring_table_name: {referring_column_name: [referring_record_0, referring_record_1, ...]}}.
    Alternatively, if 'make_list' is True, return a flat list of referring records.
    """
    if record is None:
      _, _, record, _, _ = $get_current_node()
    if not isinstance(record, Record|record._table.Record):
      raise ValueError(f"record must be a Record, not {type(record)}.")
    result = [] if make_list else {}
    foreign_tables = [t for t in $Table.get_all() if t != record._table.user_table] if tables_to_query is None else tables_to_query
    for foreign_table in foreign_tables:
      foreign_table_name = foreign_table.table.table_id
      for referring_col in cls.get_referring_columns(record=record, table_to_query=foreign_table):
        referring_col_name = referring_col.colId
        referring_recs = list(foreign_table.lookupRecords(**{referring_col_name: record.id}) or foreign_table.lookupRecords(**{referring_col_name: CONTAINS(record.id)}))
        if make_list:
          result += [r for r in referring_recs if not r in result]
          continue
        if not referring_recs:
          continue
        if not foreign_table_name in result:
          result[foreign_table_name] = {}
        result[foreign_table_name][referring_col_name] = referring_recs
    return result
  
  @classmethod
  def get_referring_records(cls, record: Record=None, tables_to_query: list[UserTable]=None) -> list[Record]:
    """
    Alias for the above get_referrers() but with 'make_list' = True.
    """
    if record is None:
      _, _, record, _, _ = $get_current_node()
    if not isinstance(record, Record|record._table.Record):
      raise ValueError(f"record must be a Record, not {type(record)}.")
    return cls.get_referrers(record=record, tables_to_query=tables_to_query, make_list=True)
        



return Relation
