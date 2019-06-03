import config
import mysql.connector
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy


class Result:
    def __init__(self, startDate, endDate, startValue, endValue, delta):
        self.startDate = startDate
        self.endDate = endDate
        self.startValue = startValue
        self.endValue = endValue
        self.delta = delta


class StructFull:
    def __init__(self, date, open, high, low, close):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def avg(self):
        return (self.open + self.high + self.low + self.close) / 4


def nmaxvalue(arr, n):
    res = []
    for j in range(0, n):
        max = arr[0].delta
        k = 0
        for i in range(0, len(arr)):
            if abs(arr[i].delta) > max:
                max = abs(arr[i].delta)
                k = i
        res.append(arr[k])
        arr.pop(k)
    return res


def nmaxdate(arr, n):
    res = []
    for j in range(0, n):
        max = datetime.timedelta(0)
        k = 0
        for i in range(0, len(arr)):
            if arr[i].endDate - arr[i].startDate > max:
                max = arr[i].endDate - arr[i].startDate
                k = i
        res.append(arr[k])
        arr.pop(k)
    return res


def changeDetect(symbol, minDate, maxDate, maxResultCount):
    conn = mysql.connector.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'],
                                   db=config.db['dbname'])
    cursor = conn.cursor()

    query = "SELECT `datentime`, `open`, `high`, `low`, `close` FROM `data` WHERE `symbol` = '" + symbol + "' and `datentime` >= '" + minDate + "' and `datentime` <= '" + maxDate + "' ORDER BY `datentime`"

    cursor.execute(query)
    raw_data = cursor.fetchall()

    # arrays need for plotting
    dateArray = []
    openArray = []
    highArray = []
    lowArray = []
    closeArray = []
    avgArray = []

    itemsFull = []

    for element in raw_data:
        date = element[0]
        open = element[1]
        high = element[2]
        low = element[3]
        close = element[4]
        avg = (open + high + low + close) / 4

        dateArray.append(date)
        openArray.append(open)
        highArray.append(high)
        lowArray.append(low)
        closeArray.append(close)
        avgArray.append(avg)

        itemsFull.append(StructFull(date, open, high, low, close))

    resultArray = []
    i = 0
    tempStartDate = itemsFull[i].date
    tempStartValue = itemsFull[i].avg()

    # for element in itemsFull:
    #     print element.date, ' - ', element.avg()

    while i < len(itemsFull) - 2:
        temp = itemsFull[i].avg()
        if temp < itemsFull[i + 1].avg():
            if itemsFull[i + 1].avg() > itemsFull[i + 2].avg():
                tempEndDate = itemsFull[i + 1].date
                tempEndValue = itemsFull[i + 1].avg()
                resultArray.append(
                    Result(tempStartDate, tempEndDate, tempStartValue, tempEndValue, tempEndValue - tempStartValue))
                tempStartDate = itemsFull[i + 1].date
                tempStartValue = itemsFull[i + 1].avg()
        else:
            if itemsFull[i + 1].avg() < itemsFull[i + 2].avg():
                tempEndDate = itemsFull[i + 1].date
                tempEndValue = itemsFull[i + 1].avg()
                resultArray.append(
                    Result(tempStartDate, tempEndDate, tempStartValue, tempEndValue, tempEndValue - tempStartValue))
                tempStartDate = itemsFull[i + 1].date
                tempStartValue = itemsFull[i + 1].avg()
        i += 1

    resultArray.append(Result(resultArray[len(resultArray) - 1].endDate, itemsFull[len(itemsFull) - 1].date,
                              resultArray[len(resultArray) - 1].endValue, itemsFull[len(itemsFull) - 1].avg(),
                              itemsFull[len(itemsFull) - 1].avg() - resultArray[len(resultArray) - 1].endValue))

    resarr = copy.copy(resultArray)
    for element in nmaxvalue(resarr, maxResultCount):
        print element.startDate, ' - ', element.endDate, ': ', element.delta

    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)

    resarr = copy.copy(resultArray)
    res = nmaxvalue(resarr, maxResultCount)
    minmaxdates = []
    minmaxvalues = []
    decinc = []
    minDates = []
    maxDates = []
    minValues = []
    maxValues = []

    for i in range(0, maxResultCount):
        daterow = []
        valuerow = []
        if res[i].delta < 0:
            decinc.append(-1)
        else:
            decinc.append(1)
        for temp in itemsFull:
            if res[i].startDate <= temp.date <= res[i].endDate:
                daterow.append(temp.date)
                valuerow.append(temp.avg())
        minmaxdates.append(daterow)
        minmaxvalues.append(valuerow)

    for obj in resultArray:
        if obj.delta <= 0:
            minDates.append(obj.startDate)
            minValues.append(obj.startValue)
        else:
            maxDates.append(obj.startDate)
            maxValues.append(obj.startValue)

    plt.plot(dateArray, avgArray, 'k', label='Average Price')
    for i in range(0, maxResultCount):
        if decinc[i] > 0:
            plt.plot(minmaxdates[i], minmaxvalues[i], 'tab:green')
        else:
            plt.plot(minmaxdates[i], minmaxvalues[i], 'tab:red')
    plt.scatter(maxDates, maxValues, marker=mpl.markers.CARETUPBASE, color='tab:green', s=100, label='Increase')
    plt.scatter(minDates, minValues, marker=mpl.markers.CARETDOWNBASE, color='tab:red', s=100, label='Decrease')
    plt.legend(loc='upper center')
    ax.set(xlabel='Date', ylabel='Values',
           title='%s values (%s - %s)' % (symbol, dateArray[0], dateArray[len(dateArray) - 1]))
    plt.grid()
    plt.show()

    return 0


try:
    print changeDetect('MSFT', "2019,01,30", "2019,01,31", 10)
except Exception, e:
    print e
