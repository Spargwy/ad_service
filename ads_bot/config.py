from enum import Enum

db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    # """
    S_START = "0"  # Начало нового диалога
    S_AD_TEXT = "1"
    S_AD_PRICE = "2"
    S_ANSWER_ABOUT_HOT_PRICE = "3"
    S_SET_HOT_PRICE = "4"
