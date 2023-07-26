import csv
import datetime
from datetime import timedelta
from colorama import Fore, init

def read_csv(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header row
        dates = [(row[0], row[1]) for row in reader]  # Only read the first two columns
    return dates

def calculate_yearly_periods(application_date):
    yearly_periods = []
    for i in range(5):
        end_date = application_date - timedelta(days=i*365)
        start_date = end_date - timedelta(days=365) + timedelta(days=1)  # +1 to ensure no overlap
        yearly_periods.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    return yearly_periods

def calculate_days_out(dates, application_date, scenario):
    yearly_periods = calculate_yearly_periods(application_date)
    days_out_per_year = {}
    for i, period in enumerate(yearly_periods):
        days_out = 0
        for trip in dates:
            trip_start = datetime.datetime.strptime(trip[0], '%Y-%m-%d').date()
            trip_end = datetime.datetime.strptime(trip[1], '%Y-%m-%d').date()
            period_start = datetime.datetime.strptime(period[0], '%Y-%m-%d').date()
            period_end = datetime.datetime.strptime(period[1], '%Y-%m-%d').date()
            if trip_end < period_start or trip_start > period_end:
                continue
            if scenario == 1:
                days_out += (min(trip_end, period_end) - max(trip_start, period_start)).days + 1
            elif scenario == 2:
                if trip_start >= period_start and trip_end <= period_end:
                    days_out += (trip_end - trip_start).days
                else:
                    days_out += (min(trip_end, period_end) - max(trip_start, period_start)).days
            else:
                if trip_start >= period_start and trip_end <= period_end:
                    days_out += (trip_end - trip_start).days
                else:
                    days_out += (min(trip_end, period_end) - max(trip_start, period_start)).days - 1
        days_out_per_year[i+1] = days_out
    return days_out_per_year

def find_application_date(dates):
    for i in range(1, 181):
        application_date = (datetime.datetime.now() + timedelta(days=i)).date()
        if all(max(calculate_days_out(dates, application_date, scenario).values()) <= 90 for scenario in range(1, 4)):
            return application_date.strftime('%Y-%m-%d')
    return 'No application date found within the given date range.'

def main():
    init()  # initialize colorama
    file = input('Please enter the path of your CSV file (or press enter to use dates.csv): ')
    file = 'dates.csv' if file == '' else file
    application_date_str = input('Please enter the application date (or press enter to calculate it automatically): ')
    application_date = datetime.datetime.now().date() + timedelta(days=1) if application_date_str == '' else datetime.datetime.strptime(application_date_str, '%Y-%m-%d').date()

    dates = read_csv(file)
    print('\nApplication Date:', application_date.strftime('%Y-%m-%d'))

    for scenario in range(1, 4):
        print('\nScenario {}:\n'.format(scenario))
        days_out_per_year = calculate_days_out(dates, application_date, scenario)
        for year, days_out in days_out_per_year.items():
            if days_out > 90:
                print('Year {}: {} - {}: {} days out'.format(year, calculate_yearly_periods(application_date)[year-1][1], calculate_yearly_periods(application_date)[year-1][0], Fore.RED + str(days_out) + Fore.RESET))
            else:
                print('Year {}: {} - {}: {} days out'.format(year, calculate_yearly_periods(application_date)[year-1][1], calculate_yearly_periods(application_date)[year-1][0], Fore.GREEN + str(days_out) + Fore.RESET))

if __name__ == '__main__':
    main()
