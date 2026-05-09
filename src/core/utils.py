import datetime
import time
from dateutil import relativedelta
from typing import Any, Tuple

from src.core.config import logger

def daily_readme(birthday: datetime.datetime) -> str:
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + format_plural(diff.years), 
        diff.months, 'month' + format_plural(diff.months), 
        diff.days, 'day' + format_plural(diff.days),
        ' \U0001f382' if (diff.months == 0 and diff.days == 0) else '')

def format_plural(unit: int) -> str:
    return 's' if unit != 1 else ''

def perf_counter(funct, *args) -> Tuple[Any, float]:
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def formatter(query_type: str, difference: float, funct_return: Any = False, whitespace: int = 0) -> Any:
    time_str = '{:>12}'.format('%.4f' % difference + ' s ') if difference > 1 else '{:>12}'.format('%.4f' % (difference * 1000) + ' ms')
    logger.info('{:<23}{}'.format('   ' + query_type + ':', time_str))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return
