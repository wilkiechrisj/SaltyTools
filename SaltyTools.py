import json
import matplotlib.pyplot as plot

with open('saltydata.json', 'r') as infile:
    data = json.load(infile)


def unique_customers():

    customers = []

    for element in data:
        if element['user_id'] not in customers:
            customers.append(element['user_id'])

    return len(customers), customers


def unique_dealerships():

    dealerships = []

    for element in data:
        if element['dealership_id'] not in dealerships:
            dealerships.append(element['dealership_id'])

    return len(dealerships), dealerships


def customer_current_status():

    length, customers = unique_customers()
    status = []

    for id_number in range(len(customers)):
        status.append([customers[id_number], ''])

    for change in range(len(data)):

        info = data[change]

        for person in status:
            if info['user_id'] == person[0]:
                if info['new_status'] != 'sms_sent':
                    person[1] = info['new_status']
                else:
                    person[1] = info['prior_status']

    return status


def order_statuses():

    customer_stat = customer_current_status()
    status = [['generating_rc1', 0],
              ['form_started', 0],
              ['generating_quote', 0],
              ['sms_sent', 0],
              ['quote_generated', 0],
              ['ready', 0],
              ['car_deal_canceled', 0],
              ['payment_complete', 0],
              ['poi_generated', 0],
              ['poi_sent', 0],
              ['not-set', 0],
              ['manually_generating_quote', 0],
              ['manual_process_required', 0],
              ['quote_printed', 0],
              ['poi_printed', 0],
              ['rc1_failed', 0],
              ['payment_failed', 0],
              ['no_quote_available', 0],
              ['missing_data', 0]]

    for stat in status:
        for user in customer_stat:
            if user[1] == stat[0]:
                stat[1] += 1

    return status


def status_count(status):

    num = 0

    for element in data:
        if element['new_status'] == status:
            num += 1

    return num


def dealership_status_count(status, dealership):

    num = 0

    for element in data:
        if element['new_status'] == status and element['dealership_id'] == dealership:
            num += 1

    return num


def activity_on_date():

    dates = []

    for num in range(len(data)):

        info = data[num]

        if info['created_at'][:9] in dates:
            pass
        else:
            dates.append(info['created_at'][:9])

    events = []

    for element in dates:
        events.append([element, 0])

    for num in range(len(data)):

        info = data[num]

        for element in events:
            if element[0] == info['created_at'][:9]:
                element[1] += 1

    return events


def sales_data():

    pie_data = order_statuses()
    pie_col = ['r', 'b', 'g']
    pie_lab = ['Canceled', 'Processing', 'Payment']
    pie_num = [0, 0, 0]

    for i in pie_data:
        if i[0] == 'payment_complete' or i[0] == 'poi_sent' or i[0] == 'poi_printed':
            pie_num[2] += i[1]
        elif i[0] == 'car_deal_canceled':
            pie_num[0] += i[1]
        else:
            pie_num[1] += i[1]

    plot.pie(pie_num, labels=pie_lab, colors=pie_col)
    plot.legend()
    plot.show()
    print(pie_data)
    print(pie_num)


def date_data():

    dates = activity_on_date()
    x = []
    y = []

    for element in dates:
        x.append(element[0][:2] + element[0][3:6])
        y.append(element[1])

    plot.plot(x, y, marker='o')
    plot.xlabel('DATE')
    plot.ylabel('# of Status Changes')
    plot.xticks(rotation=90)
    plot.show()
    print(dates)


def dealership_sales():

    dealerships = []
    num, dealers = unique_dealerships()

    for element in dealers:
        dealerships.append([element, dealership_status_count('payment_complete', element)])

    for element in dealerships:
        if element[1] >= 26:
            print(element)

    return dealerships