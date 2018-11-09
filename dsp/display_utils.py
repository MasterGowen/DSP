
def countdown_title(number):
    last_numeral = float(str(number)[-1])
    if number in [11, 12, 13, 14] or last_numeral in [0, 5, 6, 7, 8, 9]:
        return "отсчётов"
    elif last_numeral in [2, 3, 4]:
        return "отсчёта"
    elif last_numeral == 1:
        return "отсчёт"
    else:
        return "отсчётов"


def time_title(number):
    last_numeral = float(str(number)[-1])
    if last_numeral in [2, 3, 4]:
        return "раза"
    return "раз"