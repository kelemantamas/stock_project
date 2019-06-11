import json
import config
import datetime
import collections
import pandas as pd
import time
# import string
import matplotlib.pyplot as plt

with open(config.json_file) as f:
    raw_datag = json.load(f)

# remove multiple lines, checking by link cause it is unique
temp_dict = {raw_datag[0]['link']: raw_datag[0]}
for ig in range(1, len(raw_datag)):
    linkg = raw_datag[ig]['link']
    if linkg not in temp_dict:
        temp_dict[linkg] = raw_datag[ig]

# data is the new list with the no multipled articles
data = []
for keyg, valueg in temp_dict.items():
    data.append(valueg)


class Articles:
    def __init__(self, domain, date):
        self.domain = domain
        self.date = date
        self.counter = 1

    def increaseCounter(self):
        self.counter += 1

    def getCounter(self):
        return self.counter


def getAtricleCountPerFeed():
    mydict = {}
    for i in range(0, len(data)):
        key = data[i]['Feed']
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    for k in mydict:
        print k, ' - ', mydict[k]


def getAtricleCountPerDomain():
    mydict = {}
    for i in range(0, len(data)):
        key = str(data[i]['Feed'])
        key = key.split('.com')[0] + '.com/'
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    for k in mydict:
        print k, ' - ', mydict[k]


def getArticlesPerDay():
    mydict = {}
    for i in range(0, len(data)):
        try:
            date = datetime.datetime.strptime(data[i]['published'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d")
        except:
            date = "undefined date"

        if date not in mydict:
            mydict[date] = 1
        else:
            mydict[date] += 1

    orderedDict = collections.OrderedDict(sorted(mydict.items()))
    for key, value in orderedDict.items():
        print key, '\t\t', value


def getCompanies():
    df = pd.read_excel(config.excel_file, sheet_name="companies_and_subsideries")
    symb = df['name']
    subsides = df['subsidiary']
    n = min(len(symb), len(subsides))
    i = 0
    mydict = {}
    while i < n:
        key = str(symb[i])
        # value = str(subsides[i])
        value = subsides[i].encode('utf-8')

        if key not in mydict:
            mydict[key] = []
            mydict[key].append(value)
        else:
            if value not in mydict[key]:
                mydict[key].append(value)
        i += 1
    return mydict


def getActualArticlesPerDay(articles):
    mydict = {}
    for i in range(0, len(articles)):
        try:
            date = datetime.datetime.strptime(data[i]['published'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d")
        except:
            date = "undefined date"

        if date not in mydict:
            mydict[date] = 1
        else:
            mydict[date] += 1

    orderedDict = collections.OrderedDict(sorted(mydict.items()))
    for key, value in orderedDict.items():
        print key, '\t\t', value
    return orderedDict


def getArticleTalkingAboutCompany(company_symbol):
    articles_with_comps = []
    companies = getCompanies()
    for i in range(0, len(data)):
        msg = data[i]['message']
        # msg = str(msg.encode('utf-8'))
        # msg = msg.translate(string.maketrans("\n\t\r", "   "))
        try:
            txt = data[i]['full-text']
            # txt = str(txt.encode('utf-8'))
            # txt = txt.translate(string.maketrans("\n\t\r", "   "))
        except Exception:
            txt = "No full-text field"
        srch = 'NASDAQ: {0} '.format(company_symbol)
        if srch in txt:
            articles_with_comps.append(data[i])
            continue
        if srch in msg:
            articles_with_comps.append(data[i])
            continue

        for company in companies[company_symbol]:
            if (company + " ") in txt.encode('utf-8'):
                # if (company + " ") in txt:
                articles_with_comps.append(data[i])
                break
            if (company + " ") in msg.encode('utf-8'):
                # if (company + " ") in msg:
                articles_with_comps.append(data[i])
                break

    return articles_with_comps


def getArticleCountTalkingAboutCompany(company_symbol):
    return len(getArticleTalkingAboutCompany(company_symbol))


def diagramForCompany(symbol):
    day_count_dict = getActualArticlesPerDay(getArticleTalkingAboutCompany(symbol))
    dates = []
    counted = []

    for key, value in day_count_dict.iteritems():
        if key != "undefined date":
            dates.append(key)
            counted.append(value)

    pd.to_datetime(dates)
    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    plt.plot(dates, counted, 'r', marker="o", linestyle="", label="Number of articles per day")
    plt.legend(loc='upper center')
    ax.set(xlabel='Date', ylabel='Nr. of articles', title='Articles per day %s' % symbol)
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()


def main():
    start_time = time.time()
    proba = getArticleTalkingAboutCompany("MSFT")
    lista = []
    for element in proba:
        lista.append(element['link'])
    lista.sort()
    for element in lista:
        print element
    print getArticleCountTalkingAboutCompany("MSFT")

    diagramForCompany("MSFT")

    # for e in proba:
    #     print e['full-text']
    # print len(proba)
    # diagramForCompany("MSFT")
    print "Took: %s s" % (time.time() - start_time)


# main()
