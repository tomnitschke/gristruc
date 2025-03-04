# Paste below into a formula column called 'format_filesize'.

# See: https://stackoverflow.com/questions/1094841/get-a-human-readable-version-of-a-file-size
def format_filesize(num: int|float, suffix: str="B", divisor: int|float=1024.0):
  for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
    unit = unit[:-1] if divisor != 1024 else unit
    if abs(num) < divisor:
      return f"{num:3.2f} {unit}{suffix}"
    num /= divisor
  return f"{num:.1f} Yi{suffix}"

return format_filesize
