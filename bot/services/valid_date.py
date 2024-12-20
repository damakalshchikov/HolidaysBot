from datetime import datetime


def is_valid_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False
