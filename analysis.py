import articles
import time
import math


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


def tf(word, doc):
    return freq(word, doc) / float(word_count(doc))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) / float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
    return tf(word, doc) * idf(word, list_of_docs)


def allArticlesExcept(company_code):
    ignore_articles = articles.getArticleTalkingAboutCompany(company_code)
    print len(ignore_articles)

    article_all = articles.data
    i = 0
    print len(article_all)
    for act_all in article_all:
        link = act_all['link']
        for act_ignore in ignore_articles:
            if link == act_ignore['link']:
                article_all.pop(i)
                break
        i += 1

    print len(article_all)
    # data = []
    #
    # for element in article_all:
    #     try:
    #         data.append(element['full-text'].encode('utf-8'))
    #     except Exception:
    #         pass
    #
    # cv = CountVectorizer()
    #
    # # convert text data into term-frequency matrix
    # data = cv.fit_transform(data)
    #
    # tfidf_transformer = TfidfTransformer()
    #
    # # convert term-frequency matrix into tf-idf
    # tfidf_matrix = tfidf_transformer.fit_transform(data)
    #
    # # create dictionary to find a tfidf word each word
    # word2tfidf = dict(zip(cv.get_feature_names(), tfidf_transformer.idf_))
    #
    # orderedDict = collections.OrderedDict(sorted(word2tfidf.items(), key=operator.itemgetter(1)))
    #
    # for word, score in orderedDict.items():
    #     try:
    #         float(word)
    #         orderedDict.pop(word)
    #     except ValueError:
    #         print word, score
    #
    # print len(orderedDict)


def articlesAbout(company_code):
    raw_data = articles.getArticleTalkingAboutCompany(company_code)

    # mydict = {}
    # for i in range(0, len(raw_data)):
    #     key = raw_data[i]['link']
    #     if key not in mydict:
    #         mydict[key] = 1
    #     else:
    #         mydict[key] += 1
    #
    # for k in mydict:
    #     print k, ' - ', mydict[k]
    # print len(mydict)
    comp_arr = []
    for element in raw_data:
        try:
            comp_arr.append(element['full-text'].encode('utf-8'))
        except:
            comp_arr.append(element['message'].encode('utf-8'))

    # res = calculateTFIDF(comp_arr)

    # for key, value in res.items():
    #     print key, ' - ', value
    # print len(res)
    #
    # return res


# allFilesTfidf()
# companyTfidf()
start_time = time.time()

microsoft = "Ez egy microsoftos szoveg, a microsoft nagy ceg, sokat kere, megnyrete a palyazatokat, sok a penze microsoft"
microsoft = microsoft.lower()
microsoft = microsoft.translate(None, '!?,./')
nemmicrolist = "ez szoveg a nagy sokat sok ez is a nagy szoveg nem a nagy sok"

list_of_d = []
list_of_d.append(microsoft)
list_of_d.append(nemmicrolist)
mydict = {}

for elem in microsoft.split():
    mydict[elem] = tf_idf(elem, microsoft, list_of_d)

for key, value in mydict.items():
    print key, '\t\t\t- ', value
