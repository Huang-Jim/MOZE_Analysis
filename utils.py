from datetime import datetime
from typing import Set

import pandas as pd


def _process_date(date: str) -> str:
    """
    捨棄"日"，僅保留"年/月"
    :param date: "年/月/日" 字串
    :return: "年/月" 字串
    """
    date = date.split('/')
    date = date[: -1]
    return '/'.join(date)


def duration_args(date: pd.Series,
                  duration_arg: str
                  ) -> Set[str]:
    """
    依照duration args來決定要往後要處理的年/月期間
    :param date: MOZE.csv內"日期"的Series
    :param duration_arg: duration arg
    :return: 欲處理的"年/月"集合
    """
    # 全部區間
    if duration_arg == 'all':
        _date = date.map(_process_date)
        return set(_date)
    # 特定區間 - 只有某個月
    if '-' not in duration_arg:
        _date = [datetime.strptime(duration_arg, '%Y/%m').strftime("%Y/%#m")]
        return set(_date)
    # 特定區間 - 有給定初始
    start, end = duration_arg.split('-')
    if not end:  # 如果end為空字串，代表取到date的最新"年/月"
        end = _process_date(date.iloc[-1])
    # 將使用者輸入統一格式成月份沒有zero-padding
    start = datetime.strptime(start, '%Y/%m').strftime("%Y/%#m")
    end = datetime.strptime(end, '%Y/%m').strftime("%Y/%#m")
    _date = pd.date_range(start, end, freq='1M').strftime("%Y/%#m").tolist()
    _date.append(end)
    return set(_date)
