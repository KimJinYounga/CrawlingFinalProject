import os
import sys
import urllib.request
import datetime
import time
import json
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

# [CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# [CODE 2]
# 측정소별 실시간 측정정보 조회
def getTourPointVisitor(stationName, dataTerm, nPagenum, nItems, ver):
    end_point = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    parameters = "?_returnType=json&serviceKey=" + "n4QEDdt0gCsxKLfB7Gb0jbNHSr%2BezTz24%2BQXNGMWYsDZMNOU2BkxxQJXrid3CtTByh2Y1TdaV82BBnk5T0Vv1w%3D%3D"

    parameters += "&stationName=" + urllib.parse.quote(stationName)
    parameters += "&dataTerm="+urllib.parse.quote(dataTerm)

    parameters += "&pageNo=" + str(nPagenum)
    parameters += "&numOfRows=" + str(nItems)
    parameters += "&ver=" + str(ver)

    url = end_point + parameters
    print(url)
    retData = getRequestUrl(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)


# [CODE 3]
def getTourPointData(item, stationName, jsonResult):
    dataTime = '' if 'dataTime' not in item.keys() else item['dataTime']
    so2Value = '' if 'so2Value' not in item.keys() else item['so2Value']
    coValue = '' if 'coValue' not in item.keys() else item['coValue']
    o3Value = '' if 'o3Value' not in item.keys() else item['o3Value']
    no2Value = '' if 'no2Value' not in item.keys() else item['no2Value']
    pm10Value = '' if 'pm10Value' not in item.keys() else item['pm10Value']
    pm10Value24 = '' if 'pm10Value24' not in item.keys() else item['pm10Value24']
    pm25Value = '' if 'pm25Value' not in item.keys() else item['pm25Value']
    pm25Value24 = '' if 'pm25Value24' not in item.keys() else item['pm25Value24']
    khaiValue = '' if 'khaiValue' not in item.keys() else item['khaiValue']
    khaiGrade = '' if 'khaiGrade' not in item.keys() else item['khaiGrade']
    so2Grade = '' if 'so2Grade' not in item.keys() else item['so2Grade']
    coGrade = '' if 'coGrade' not in item.keys() else item['coGrade']
    o3Grade = '' if 'o3Grade' not in item.keys() else item['o3Grade']
    pm10Grade = '' if 'pm10Grade' not in item.keys() else item['pm10Grade']
    no2Grade = '' if 'no2Grade' not in item.keys() else item['no2Grade']
    pm25Grade = '' if 'pm25Grade' not in item.keys() else item['pm25Grade']
    pm10Grade1h = '' if 'pm10Grade1h' not in item.keys() else item['pm10Grade1h']
    pm25Grade1h = '' if 'pm25Grade1h' not in item.keys() else item['pm25Grade1h']




    jsonResult.append({'stationName':stationName,'dataTime':dataTime, 'so2Value': so2Value, 'coValue': coValue, 'o3Value': o3Value,
                       'no2Value': no2Value, 'pm10Value': pm10Value, 'pm10Value': pm10Value,
                       'pm10Value24': pm10Value24,'pm25Value':pm25Value ,'pm25Value24': pm25Value24,'khaiValue':khaiValue ,
                       'khaiGrade':khaiGrade ,'so2Grade':so2Grade ,'coGrade':coGrade ,'o3Grade':o3Grade ,'no2Grade':no2Grade ,
                       'pm10Grade':pm10Grade,'pm25Grade':pm25Grade ,'pm10Grade1h':pm10Grade1h ,'pm25Grade1h':pm25Grade1h})

    return


# [CODE 0]
def main():
    jsonResult = []
    stationName = '종로구'
    dataTerm='DAILY'
    nPagenum = 1
    nItems = 100
    ver=1.3
    nStartYear = 2011
    nEndYear = 2017

    # def getTourPointVisitor(stationName, dataTerm, nPagenum, nItems, ver):
    while True:
        jsonData = getTourPointVisitor(stationName, dataTerm, nPagenum, nItems, ver)
        print(jsonData)
        running=True
        # if (jsonData['response']['header']['resultMsg'] == 'NORMAL SERVICE.'):
        if running:
            nTotal = jsonData['totalCount']
            print(nTotal)

            if nTotal == 0:
                break
            for item in jsonData['list']:
                getTourPointData(item, stationName, jsonResult)

            nPage = math.ceil(nTotal / 100)
            if (nPagenum == nPage):
                break

            nPagenum += 1

        else:
            break

    # mise_table=pd.DataFrame(jsonResult, columns=('stationName','dataTime',
    #                                              'so2Value','coValue', 'o3Value','no2Value',
    #                                              'pm10Value', 'pm10Value24','pm25Value','pm25Value24',
    #                                              'khaiValue','khaiGrade','so2Grade','coGrade','o3Grade',
    #                                              'no2Grade','pm10Grade','pm25Grade','pm10Grade1h','pm25Grade1h'
    #                                              ))
    # mise_table.to_csv("./전국대기오염정보.csv", encoding="cp949", mode='w', index=True)

    # with open('./%s_실시간대기오염정보_%d_%d.json' % (stationName, nStartYear, nEndYear - 1), 'w',
    #           encoding='utf8') as outfile:
    #     retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    #     outfile.write(retJson)

    # print('%s_실시간대기오염정보_%d_%d.json Saved' % (stationName, nStartYear, nEndYear - 1))

    print("saved")

if __name__ == '__main__':
    # main()
    titanic=pd.read_csv("./실시간대기오염정보.csv", encoding="cp949")
    titanic_df=pd.DataFrame(titanic, columns=('stationName','dataTime',
                                                 'so2Value','coValue', 'o3Value','no2Value',
                                                 'pm10Value', 'pm10Value24','pm25Value','pm25Value24',
                                                 'khaiValue','khaiGrade','so2Grade','coGrade','o3Grade',
                                                 'no2Grade','pm10Grade','pm25Grade','pm10Grade1h','pm25Grade1h'))
    titanic = titanic.drop(['Unnamed: 0'], axis=1)
    print(titanic[205:210])


    # print(titanic_df.head())
    # print(titanic)
    # titanic=titanic.drop(['Unnamed: 0'], axis=1)
    # df_na=titanic.isnull()
    # df_na_sum=titanic.isnull().sum()
    # df_dropna=titanic.dropna()
    # df_na_sum=titanic.isnull().sum()
    # print(df_na_sum)
    # print(df_dropna)
    # print(df_na)