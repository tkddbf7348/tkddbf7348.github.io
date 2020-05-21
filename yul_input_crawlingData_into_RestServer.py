import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import csv
import socket
import time


def main() :
    res = requests.get('https://thisibelieve.org/theme/')
    soup = BeautifulSoup(res.content, 'html.parser')
    text = ''
    for h in [0, 1, 2]:
        links = soup.select('ul.content-column')[h].text
        text += links
    lists = []
    d = {}
    lists = text.split(')')
    for hh in lists:
        if hh == '':
            break
        else:
            chunk = []
            chunk = hh.split('(')
            d[str(chunk[0].rstrip())] = str(chunk[1])

    themes = []
    themes = list(d.keys())
    th_index = 0
    th = themes[th_index]
    p = 1


    f = open('data/output_' + th + '.csv', 'r', encoding='utf-8', errors='ignore')  # 결과 저장할 파일 만듦
    wr = csv.reader(f)  # csv객체

    ff = open('data/error.csv', 'w', encoding='utf-8', newline='', errors='ignore')  # 글이 들어가지 않을 시에 error.csv 파일에 따로 저장해 둠.
    wrr = csv.writer(ff)

    while(th_index <= len(themes)) :


        for line in wr:
            print(line)

            try:
                sql = 'http://203.250.123.99:9500/sql/INSERT%20INTO%20TABLE%20test%20VALUES ("csai","test",("' + str(line[0]) + '","' + str(line[1]).strip() + '","' + str(line[2]) + '"))'
                ###### http://203.250.123.99:9500/sql/INSERT INTO table yul2 VALUES('csai','yul2',('doc_no','text','tag'))
                sql = sql.replace('‘', "'").replace(" ", "%20").replace("'", "%27").replace('"', "%22").replace("?","(question)").replace("(", "%28").replace(")", "%29")  # URL형식에 맞게 특수문자 수정
                # print(urllib.parse.quote(sql))
                print(sql)
                req = urllib.request.Request(sql)
                data = urllib.request.urlopen(req).read()
                print('theme : ' + th + ', ' + str(p) + " clear")
                print(data)
                print()


                if 'null' in str(data):
                    wrr.writerow([str(line[0]), str(line[1].strip()), str(line[2]), "null"])
                p = p + 1



            except urllib.error.HTTPError as e1:

                print(e1)

                wrr.writerow([str(line[0]), str(line[1].strip()), str(line[2]), str(e1)])
                p = p + 1
                print()
                print()




            except UnicodeEncodeError as e3:

                print(e3)

                wrr.writerow([str(line[0]), str(line[1].strip()), str(line[2]), str(e3)])
                p = p + 1
                print()
                print()


        th_index = th_index + 1 #다음 테마

    f.close()
    ff.close()






main()