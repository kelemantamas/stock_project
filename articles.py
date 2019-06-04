import json
import config
import datetime
import collections
import pandas as pd
import time
import matplotlib.pyplot as plt

with open(config.json_file) as f:
    data = json.load(f)


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
        try:
            txt = data[i]['full-text']
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
                articles_with_comps.append(data[i])
                break
            if (company + " ") in msg.encode('utf-8'):
                articles_with_comps.append(data[i])
                break
        # for key, subsidiaries in comps.iteritems():
        #     srch = '(NASDAQ: {0})'.format(key)
        #     # if re.search(srch, txt, re.IGNORECASE):
        #     if srch in txt:
        #         print key, " in full-text:"
        #         print '\n', txt
        #         print '\n', ' - - - - - - - - - - ', '\n'
        #         continue
        #     if srch in msg:
        #         print key, " in message field:"
        #         print '\n', msg
        #         print '\n', ' - - - - - - - - - - ', '\n'
        #         continue
        #     for subsidiary in subsidiaries:
        #         if (subsidiary + " ") in txt.encode('utf-8'):
        #             print key, ' - ', subsidiary, " in full-text: \n", txt
        #             print '\n', ' - - - - - - - - - - ', '\n'
        #             break
        #         if (subsidiary + " ") in msg.encode('utf-8'):
        #             print key, ' - ', subsidiary, " in message field: \n", msg
        #             print '\n', ' - - - - - - - - - - ', '\n'
        #             break
    return articles_with_comps


def getArticleCountTalkingAboutCompany(company_symbol):
    companies = getCompanies()
    count = 0
    for i in range(0, len(data)):
        msg = data[i]['message']
        try:
            txt = data[i]['full-text']
        except Exception:
            txt = "No full-text field"
        srch_for_key = 'NASDAQ: {0} '.format(company_symbol)

        if srch_for_key in txt:
            count += 1
            continue
        if srch_for_key in msg:
            count += 1
            continue

        for company in companies[company_symbol]:
            if (company + " ") in txt.encode('utf-8'):
                count += 1
                break
            if (company + " ") in msg.encode('utf-8'):
                count += 1
                break
    return count


def diagramForCompany(day_count_dict, symbol):
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
    result = getActualArticlesPerDay(getArticleTalkingAboutCompany("AAPL"))

    diagramForCompany(result, "AAPL")


start_time = time.time()

main()

print "Took: %s s" % (time.time() - start_time)
