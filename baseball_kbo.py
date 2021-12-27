import requests
from bs4 import BeautifulSoup

#국내 야구
url = "https://sports.news.naver.com/kbaseball/schedule/index"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
# naver에서 div를 날짜별 홀수와 짝수로 나누어 놓음
soupData = [soup.findAll("div", {"class": "sch_tb"}), soup.findAll("div", {"class": "sch_tb2"})]
dataList = []
for dataTb in soupData:
    for data in dataTb:
        # 일자
        dateValue = data.find("span", {"class": "td_date"}).text
        # 정렬을 위한 일자 포맷 통일
        if(len(dateValue.split(" ")[0].split(".")[1]) == 1):
            dateValue = dateValue.split(" ")[0].split(".")[0] + ".0" + dateValue.split(" ")[0].split(".")[1] + " " + dateValue.split(" ")[1]
        matchCnt = data.find("td")["rowspan"]
        for i in range(int(matchCnt)):
            matchData = {}
            # 일자
            matchData["date"] = dateValue
            # 시간
            matchData["time"] = data.findAll("tr")[i].find("span", {"class": "td_hour"}).text
            # 해당 일자에 경기가 없을 시 naver sports에서 matchData["time"] = "-" 반환
            if matchData["time"] != "-" :
                # 홈팀
                matchData["home"] = data.findAll("tr")[i].find("span", {"class": "team_rgt"}).text
                # 어웨이팀
                matchData["away"] = data.findAll("tr")[i].find("span", {"class": "team_lft"}).text
                # VS일 시 예정 경기
                if data.findAll("tr")[i].find("strong", {"class": "td_score"}).text != "VS" :
                    # 홈팀 스코어
                    matchData["homeScore"] = data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[1]
                    # 어웨이팀 스코어
                    matchData["awayScore"] = data.findAll("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                else :
                    matchData["homeScore"] = "-"
                    matchData["awayScore"] = "-"
                # 경기장
                matchData["stadium"] = data.findAll("tr")[i].findAll("span", {"class": "td_stadium"})[1].text
            else :
                matchData["home"] = "-"
                matchData["away"] = "-"
                matchData["homeScore"] = "-"
                matchData["awayScore"] = "-"
                matchData["stadium"] = "-"
            dataList.append(matchData)
# 홀수 순, 짝수 순으로 append된 데이터 정렬
result = sorted(dataList, key= lambda x: x["date"].split(" ")[0])
print(result)