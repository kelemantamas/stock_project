import config
import mysql.connector
import datetime
import copy


def nmaxvalue(arr, n):
    result = []
    for i in range(0, n):
        max = arr[0].diff
        k = 0
        for j in range(1, len(arr)):
            if max < arr[j].diff:
                max = arr[j].diff
                k = j
        result.append(arr[k])
        arr.pop(k)
    return result


class Daily:
    def __init__(self, datemin, datemax, valuemin, valuemax, diff):
        self.datemin = datemin
        self.datemax = datemax
        self.valuemin = valuemin
        self.valuemax = valuemax
        self.diff = diff


class Struct:
    def __init__(self, date, avg):
        self.date = date
        self.avg = avg


def findmax(symbol, minDate, maxDate, deltaT, nmax):
    days = datetime.timedelta(days=deltaT)
    if days > datetime.datetime.strptime(maxDate, "%Y,%m,%d") - datetime.datetime.strptime(minDate, "%Y,%m,%d"):
        return "deltaT is longer, than the interval"

    conn = mysql.connector.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'],
                                   db=config.db['dbname'])
    cursor = conn.cursor()

    query = "SELECT `datentime`, `open`, `high`, `low`, `close` FROM `data` WHERE `symbol` = '" + symbol + "' and `datentime` >= '" + minDate + "' and `datentime` <= '" + maxDate + "' ORDER BY `datentime`"

    cursor.execute(query)
    raw_data = cursor.fetchall()

    items = []
    for element in raw_data:
        avg = (element[1] + element[2] + element[3] + element[4]) / 4
        if element[0].hour == 9 and element[0].minute == 35:
            items.append(Struct(element[0], avg))
        if element[0].hour == 16:
            items.append(Struct(element[0], avg))

    # for element in items:
    #     print element.date, element.avg

    i = 0
    res = []
    while i < len(items) - deltaT * 2 + 1:
        first = items[i].date
        fv = items[i].avg
        i += deltaT * 2
        last = items[i - 1].date
        lv = items[i - 1].avg
        res.append(Daily(first, last, fv, lv, lv - fv))

    if res[len(res) - 1].datemax < items[len(items) - 1].date:
        res.append(Daily(res[len(res) - 1].datemax, items[len(items) - 1].date, res[len(res) - 1].valuemin,
                         items[len(items) - 1].avg, items[len(items) - 1].avg - res[len(res) - 1].valuemin))

    # for element in res:
    #     print datetime.datetime.strftime(element.datemin, '%Y-%m-%d'), ' - ', datetime.datetime.strftime(
    #         element.datemax, '%Y-%m-%d'), ': ', element.diff

    print "\n"
    arr = copy.copy(res)
    for element in nmaxvalue(arr, nmax):
        print datetime.datetime.strftime(element.datemin, '%Y-%m-%d'), ' - ', datetime.datetime.strftime(
            element.datemax, '%Y-%m-%d'), ': ', element.diff
    return 0


try:
    print findmax("MSFT", "2019,01,30", "2019,03,31", 2, 5)
except Exception, e:
    print e
