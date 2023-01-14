class YearConverter:
    regex = r'20\d{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


class MonthConverter(YearConverter):
    regex = r'\d{1,2}'  # 1, 2글자 사용 가능


class DayConverter(YearConverter):
    regex = r'[0123]\d'  # 0~3까지 사용 가능하다.
