from datetime import date, timedelta

my_date = date.today()
week_day = my_date.weekday()
week_num = my_date.isocalendar()[1]
year = my_date.isocalendar()[0]

start_date = my_date - timedelta(days=week_day)
end_date = my_date + timedelta(days=(4 - week_day))