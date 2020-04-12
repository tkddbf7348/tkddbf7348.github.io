import requests
import csv
import json
import time
import socket
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict


# from goto import with_goto

# @with_goto
def main(var):
    res = requests.get('https://thisibelieve.org/theme/')
    soup = BeautifulSoup(res.content, 'html.parser')
    text = ''
    for h in [0, 1, 2]:
        links = soup.select('ul.content-column')[h].text
        text += links
    lists = []
    d = {}
    lists = text.split(')')
    #   print(lists)
    for hh in lists:
        if hh == '':
            break
        else:
            chunk = []
            chunk = hh.split('(')
            repr1 = ""
            repr = ""
            if '&' in chunk[0]:
                rep = chunk[0].replace("&", "-")
                repr = rep.replace(" ", "")
            else:
                rep = chunk[0].rstrip()
                repr = rep.replace(" ", "-")
            repr1 = repr.lower()
            d[repr1] = str(chunk[1])

    print(d)
    p = 1  # 현재 페이지
    doc_no = 1  # 문서번호
    tag = 'addiction'  # 태그
    themes = []
    themes = list(d.keys())
    themes1 = themes[int(var):]

    ff = open('C:\\Users\\tkddb.DESKTOP-JCAG9KP\\PycharmProjects\\data\\' + 'parse_error.csv', 'w', encoding='UTF-16',newline='')  # 에러내용 저장할 파일 만듦
    wrr = csv.writer(ff)

    for th in themes1:
        p = 1
        f = open('C:\\Users\\tkddb.DESKTOP-JCAG9KP\\PycharmProjects\\data\\' + str(themes.index(th)) + '_output_' + th + '.csv', 'w', encoding='UTF-16', newline='')  # 결과 저장할 파일 만듦
        wr = csv.writer(f)  # csv객체
        page_num = int(int(d[th]) / 10) + 1
        if page_num == 0:
            page_num = 1
        tag = th
        while (p <= page_num):  # 마지막 페이지까지 실행
            res = ""
            res = requests.get('https://thisibelieve.org/theme/' + tag + '/page/' + str(p))  # 첫번째 페이지부터 긁어옴
            soup = BeautifulSoup(res.content, 'html.parser')  # 첫번쨰페이지의 content 파싱

            # 페이지에서 글들 url 뽑아오기
            url = list()  # 현재 페이지에 있는 글들의 url을 저장하는 list

            links = soup.select('.essay-title > a')  # 글들이 url이 저장되어있는 태그 긁어오기
            for link in links:
                url.append(link['href'])  # 주소들만 따서 넣어줌 (주소양식 : /essay/~~/)

            for i in url:  # 그 페이지 안의 글들을 하나씩 봄
                url_string = []
                url_string = i.split('/')
                print(str(themes.index(th)), ', ', tag, '--> ', url_string[2])
                doc_no = url_string[2]
                # label .begin
                try:
                    res2 = requests.get('https://thisibelieve.org' + i)  # 글 하나를 가져옴
                    soup2 = BeautifulSoup(res2.content, 'html.parser')  # 파싱
                    essay_text = soup2.find('div', {'id': 'essay-text'})  # 본문내용이 저장되어있는 태그 찾기
                    text = ''  # 본문내용 저장할 문자열
                    for item in essay_text.find_all('p', {'class': None}):  # 본문내용을 저장한 태그에서 본문찾기(필요한 부분만)
                        if item in soup2.find('div',
                                              {'class': 'entry-donation donate-widget-full'}):  # 만약 도네이션 부분이면 포함하지않음
                            continue
                        item_fix = str(
                            item.get_text())  # .replace('’', "'").replace('—', '-').replace('–','-').replace('“', '"').replace('”', '"').replace('\n', '').replace(',', '.').replace('   ', '').replace('…', '...').replace(' ', ' ').replace('   ', '')#csv상에서 깨지고 형식바뀌고 이상한 글자 전-----부 수정
                        text = text + ' ' + item_fix  # 본문내용을 저장함(문장 마다 공백 한 칸 추가)

                    wr.writerow([doc_no, text, tag])  # 내용을 파일에 씀
                #                    doc_no = doc_no + 1 #문서번호 1 증가
                except socket.error as e1:
                    print()
                    print(e1)
                    sec = 10
                    for i in range(sec, 0, -1):
                        time.sleep(1)
                        print('will do again since counting ' + str(i) + '/10 sec')

                    wrr.writerow([doc_no, text, tag, e1])  # 에러내용을 파일에 씀
                    print()
                    # goto .begin

            p = p + 1  # 다음 페이지
            print('theme : ' + tag + ', ' + str(p - 1) + "/" + str(page_num) + " page clear")  # 한 페이지가 끝났음을 알림

        f.close()  # 파일 닫아줌
    ff.close()


var1 = sys.argv[1]
main(var1)
