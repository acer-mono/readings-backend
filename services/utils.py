import datetime


def create_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')