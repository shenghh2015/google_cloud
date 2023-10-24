import datetime
import sys
import typing
import pytz

def is_none_or_empty(data) -> bool:
  '''This applies to any data type which has a __len__ method'''
  if data is None:
    return True

  try:
    return len(data) == 0
  except:
    return False

def __strdate(timezone: str, now):
  city = timezone.split("/")[-1]
  ts = now.strftime("%Y-%m-%d_%Ih-%Mm-%Ss_%p")
  return f"{city}_{ts}"
  
def get_log_time(utc_time: bool = True, country_city: str = None):
  '''
  utc_time: if False, return local time(server);
            if True, return local time(city).
  country_city : When utc_time is true,  if city is None, return UTC(0).
                See pytz/__init__.py:510, all_timezones

  e.g., SF time is UTC+8, then get_log_time(True) - 8 = get_log_time(False)
  '''
  if utc_time:
    if is_none_or_empty(country_city):
      now = datetime.datetime.utcnow()
      return __strdate("utc", now)
    else:
      now = datetime.datetime.now(pytz.timezone(country_city))
      return __strdate(country_city, now)

  else:
    now = datetime.datetime.now()
    return __strdate("local", now)

class Logger:
  '''
  debug=0, info=1, warning=2, error=3
  '''
  level = 1
  outstream = sys.stdout
  country_city = ""  #"Asia/Chongqing", 'America/Los_Angeles'

  @staticmethod
  def reset_outstream(out_file: str, append=False):
    mode = "a" if append else "w"
    Logger.outstream = open(out_file, mode)

  @staticmethod
  def set_level(level):
    Logger.level = level

  @staticmethod
  def is_debug():
    return Logger.level <= 0

  @staticmethod
  def debug(*args):
    if Logger.level <= 0:
      print(get_log_time(country_city=Logger.country_city),
            "DEBUG:",
            *args,
            file=Logger.outstream)
      Logger.outstream.flush()

  @staticmethod
  def info(*args):
    if Logger.level <= 1:
      print(get_log_time(country_city=Logger.country_city),
            "INFO:",
            *args,
            file=Logger.outstream)
      Logger.outstream.flush()

  @staticmethod
  def warn(*args):
    if Logger.level <= 2:
      print(get_log_time(country_city=Logger.country_city),
            "WARN:",
            *args,
            file=Logger.outstream)
      Logger.outstream.flush()

  @staticmethod
  def error(*args):
    if Logger.level <= 3:
      print(get_log_time(country_city=Logger.country_city),
            "ERR:",
            *args,
            file=Logger.outstream)
      Logger.outstream.flush()

def pydict_file_read(file_name, max_num: int = -1) -> typing.Iterator:
  assert file_name.endswith(".pydict")
  data_num = 0
  with open(file_name, encoding="utf-8") as fin:
    for idx, ln in enumerate(fin):
      if max_num >= 0 and idx + 1 > max_num:
        break
      if idx > 0 and idx % 10_000 == 0:
        Logger.info(f"{file_name}: {idx} lines have been loaded.")

      try:
        obj = eval(ln)
        yield obj
        data_num += 1

      except Exception as err:
        Logger.error(f"reading {file_name}:{idx + 1}: {err} '{ln}'")

  Logger.info(f"{file_name}: #data={data_num:,}")

def pydict_file_write(data: typing.Iterator, file_name: str, **kwargs) -> None:
  assert file_name.endswith(".pydict")
  if isinstance(data, dict):
    data = [data]
  with open(file_name, "w") as fou:
    num = 0
    for obj in data:
      num += 1
      obj_str = str(obj)
      if "\n" in obj_str:
        Logger.error(f"pydict_file_write: not '\\n' is allowed: '{obj_str}'")
      print(obj, file=fou)
      if kwargs.get("print_log", True) and num % 10_000 == 0:
        Logger.info(f"{file_name} has been written {num} lines")

  if kwargs.get("print_log", True):
    Logger.info(f"{file_name} has been written {num} lines totally")
