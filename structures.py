"""
結構化資料型態，由大到小分別為"MonthSheet(月表)"、"MainItem(主類別)"以及"SubItem(子類別)"
每張月表能有複數個主類別，每個主類別底下也由複數個子類別構成
"""
from collections import OrderedDict
from typing import Dict, List, Set

import pandas as pd


class SubItem:
    """
    子類別
    """

    def __init__(self,
                 name: str,
                 money: float,
                 date: str,
                 parent_class: str):
        self.name = name
        self.money = money
        self.date = date
        self.year, self.month, self.day = date.split('/')
        self.parent_class = parent_class

    def __str__(self):
        return ' '.join((self.date, self.name, str(self.money)))


class MainItem:
    """
    主類別
    每個主類別有多項子類別物件，子類別們以dict方式儲存，key為該子類別名稱，value為該子類別組成的list
    """

    def __init__(self, name: str):
        self.name = name
        self.child_class_items = {}

    def add_subitem(self, child_item: SubItem) -> None:
        """
        增加子類別物件至`self.child_class_items`，key為該子類別名稱，value為該子類別物件組成的list
        :param child_item: 子類別的物件
        """
        if child_item.name not in self.child_class_items.keys():
            self.child_class_items[child_item.name] = [child_item]
        else:
            self.child_class_items[child_item.name].append(child_item)

    def sum_subitems(self) -> Dict[str, float]:
        """
        將子類別依照名稱個別相加總其金額
        :return: OrderedDict，子類別項目名以及他的金額加總，從小到大排列
        """
        result = {}
        for child_class, child_items in self.child_class_items.items():
            result[child_class] = sum(map(lambda x: x.money, child_items))
        return OrderedDict(sorted(result.items(), key=lambda x: x[-1]))

    def count_subitems(self) -> Dict[str, float]:
        """
        將子類別依照名稱個別加總其次數
        :return: OrderedDict，子類別項目名以及他的次數加總，從大到小排列
        """
        result = {}
        for child_class, child_items in self.child_class_items.items():
            result[child_class] = len(child_items)
        return OrderedDict(sorted(result.items(), key=lambda x: x[-1], reverse=False))

    def get_subitems_names(self) -> Set[str]:
        """
        該主類別下的所有子類別名
        """
        return set(self.child_class_items.keys())

    def get_subitems(self) -> List[SubItem]:
        """
        該主類別下的所有子類別物件
        """
        out = []
        for item in self.get_subitems_names():
            out.extend(self.child_class_items[item])
        return out

    def __getitem__(self, item: str) -> List[SubItem]:
        if isinstance(item, str):
            try:
                return self.child_class_items[item]
            except KeyError:
                raise KeyError('預期輸入的item為{}之一，但收到"{}"'.format(list(self.child_class_items.keys()), item))
        else:
            raise TypeError('item 一定要是str，但收到的型態為%s' % type(item))

    def __len__(self):
        return len(self.child_class_items)

    def __str__(self):
        keys = list(self.child_class_items.keys())
        info = '、'.join(keys[:-1]) + '和%s' % keys[-1]
        return '%s中含有%d項子類別: %s' % (self.name, len(keys), info)


class MonthSheet:
    """
    月表
    每張月表存有主類別的物件，以main_class_items維護，key為主類別名稱，value為主類別物件
    """

    def __init__(self, date: str):
        self.date = date
        self.year, self.month = date.split('/')[:2]
        self.main_class_items = {}

    def add_row(self, row: pd.Series) -> None:
        """
        檢驗此row是否已經存在於月表的主類別中，
        若主類別不存在，則實例化該row的子類別及主類別，並更新月表的main_class_items
        若主類別已存在，則實例化該row的子類別，並添加於該主類別的子類別
        :param row: MOZE.csv的每一個列
        """
        sub_item = SubItem(name=row['子類別'],
                           money=float(''.join(row['金額'].split(','))),
                           date=row['日期'],
                           parent_class=row['主類別'])
        if row['主類別'] not in self.main_class_items.keys():
            main_item = MainItem(name=row['主類別'])
            main_item.add_subitem(sub_item)
            self.main_class_items[row['主類別']] = main_item
        else:
            self.main_class_items[row['主類別']].add_subitem(sub_item)

    def sum_mainitems(self) -> Dict[str, float]:
        """
        將主類別依照名稱個別相加總其金額
        :return: OrderedDict，主類別項目名以及他的金額加總，從小到大排列
        """
        result = {}
        for main_class, main_item in self.main_class_items.items():
            result[main_class] = sum(main_item.sum_subitems().values())
        return OrderedDict(sorted(result.items(), key=lambda x: x[-1]))

    def get_mainitems_names(self) -> Set[str]:
        """
        該月表下的所有主類別名
        """
        return set(self.main_class_items.keys())

    def get_mainitems(self) -> List[MainItem]:
        """
        該月表下的所有主類別物件
        """
        return list(self.main_class_items.values())

    def get_subitems_names(self) -> Set[str]:
        """
        該月表下的所有主類別物件的所有子類別
        """
        out = set()
        for main_item in self.get_mainitems():
            out |= main_item.get_subitems_names()
        return out

    def get_subitems(self) -> List[SubItem]:
        """
        該月表下的所有主類別物件的所有子類別
        """
        out = []
        for main_item in self.get_mainitems():
            out.extend(main_item.get_subitems())
        return out

    def __getitem__(self, item: str) -> MainItem:
        if isinstance(item, str):
            try:
                return self.main_class_items[item]
            except KeyError:
                raise KeyError('預期輸入的item為{}之一，但收到"{}"'.format(list(self.main_class_items.keys()), item))
        else:
            raise TypeError('item 一定要是str，但收到的型態為%s' % type(item))

    def __len__(self):
        return len(self.main_class_items)

    def __str__(self):
        keys = list(self.main_class_items.keys())
        info = '、'.join(keys[:-1]) + '和%s' % keys[-1]
        return '%s年%s月的月表中含有%d項主類別: %s' % (self.year, self.month, len(keys), info)
