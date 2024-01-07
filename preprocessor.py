import re
import pandas as pd

def preprocess(data, country):

    if country == 'India':
        pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        # Replace \u202F with a space (or you can use '' to remove it)
        new_dates = []
        for i in dates:
            new_dates.append(i.replace('\u202f', ' ')
                             .replace(' - ', ''))
        df = pd.DataFrame({'user_message': messages, 'date': new_dates})
        # Convert the 'date' column to datetime using pandas' to_datetime
        df['datetime'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p', errors='coerce')


    elif country == 'USA':
        pattern = '\[\d{1,2}/\d{1,2}/\d{2},\s?\d{1,2}:\d{2}:\d{2}\s[APM]{2}\] '
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        # Replace \u202F with a space (or you can use '' to remove it)
        new_dates = []
        for i in dates:
            new_dates.append(i.replace('\u202f', ' ')
                             .replace(' - ', '')
                             .replace('[', '')
                             .replace('] ', '')
                             )
        df = pd.DataFrame({'user_message': messages, 'date': new_dates})
        # Convert the 'date' column to datetime using pandas' to_datetime
        df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M:%S %p')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df['only_date'] = df['datetime'].dt.date
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df