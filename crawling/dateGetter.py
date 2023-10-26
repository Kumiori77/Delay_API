import re  # re 모듈 추가
from datetime import datetime

def get_date(text, date_list):
    date_patterns = [
        re.compile(r'\d{4}\.\d{1,2}\.\d{1,2}\.'),
        re.compile(r'\d{1,2}\.\d{1,2}\.'),
        re.compile(r'\d{1,2}월\d{1,2}일'),
        re.compile(r'\d{4}-\d{2}-\d{2}'),
    ]

    date_format = ["%Y.%m.%d.", "%Y.%m.%d.", "%Y년%m월%d일", "%Y-%m-%d"]
    year_format = ["", ".", "년", ""]

    text = text.replace(" ", "")
    for i in range(4):
        match = date_patterns[i].search(text)
        if match:
            date_str = match.group()
            if i != 0 and i != 3:
                date_str = get_year() + year_format[i] + date_str
            date = datetime.strptime(date_str, date_format[i])
            date_list.append(date)
            date_list = get_date(text[match.end():], date_list)
            break
    return date_list


def get_year():
    today = datetime.now()
    year = today.year
    year = str(year)
    return year


def check_year(date_list):
    if len(date_list) == 2:
        if date_list[0] > date_list[1]:
            last_year = int(get_year()) - 1
            date_list[0] = date_list[0].replace(year=last_year)


# if __name__ == "__main__":
#     a = []
#     a = get_date("2022-11-22 13:00~ 2024-11-21 09:00", a)
#     print(a)