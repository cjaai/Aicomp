
#install anaconda
#create envirenment named bigquery
#conda install -c conda-forge/label/cf202003 google-cloud-bigquery
#conda install -c conda-forge/label/cf202003 google-cloud-storage
#conda install -c anaconda openpyxl 

from google.cloud import bigquery
import openpyxl
import datetime

BQ_TIMEOUT = 240
#max is 100 per project
BQ_THREAD_DRY_RUN_LIMIT = 20
BQ_QUERY_SLEEP_SECONDS = 1
AUTH_JSON_FILE_PATH = './my-project-20181130-6269805c6227.json'

def bq_InitConnection():
    return bigquery.Client.from_service_account_json(AUTH_JSON_FILE_PATH)

def bq_query(SQL):
    client = bq_InitConnection()
    bqJob = client.query(SQL)
    bqList = list(bqJob.result(timeout=BQ_TIMEOUT))  # Waits for job to complete.
    return bqList

def query_SaveSheet_TsUid(SQL, SheetTitle, FilePath):
    wb = openpyxl.Workbook()
    ws = wb.active
    bqListRet = bq_query(SQL)
    ws.append(["ts", "uid"])
    i = 0
    for listItem in bqListRet:
        item = list(listItem)

        # need covert format
        #item[0] = datetime.datetime.strptime(str(item[0]), '%Y-%m-%d %H:%M:%S')
        #item[1] = int(item[1])

        item[0] = item[0]
        item[1] = item[1]
        ws.append(item)
        i += 1
    ws.title = SheetTitle
    wb.save(FilePath)

    print(FilePath + "  has been downloaded")

def query_Collect(SQL):
    retList = []
    bqListRet = bq_query(SQL)
    i = 0
    for listItem in bqListRet:
        item = list(listItem)
        retList.append(item)
        i += 1
    return retList

if __name__ == '__main__':
    #SQL = "SELECT name,gender FROM `bigquery-public-data.usa_names.usa_1910_2013` GROUP BY name, gender LIMIT 10"

    SQL = "SELECT COUNT(*) AS cnt, country_code FROM (SELECT ANY_VALUE(country_code) AS country_code FROM `patents-public-data.patents.publications` AS pubs GROUP BY application_number) GROUP BY country_code ORDER BY cnt DESC"

    res = query_Collect(SQL)
    #print(res)
    #print(res[0][0])
    query_SaveSheet_TsUid(SQL, SheetTitle="Online", FilePath=".\Online.xlsx")