from selenium import webdriver
import time
import json

driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
driver.get('https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx')
selectTeam = driver.find_element_by_css_selector("#cphContents_cphContents_cphContents_ddlTeam_ddlTeam")

# ajax를 이용하기 때문에 페이지의 주소가 변하지 않는다.
selectTeam.send_keys("NC")
# 주소가 변하지 않기 때문에 파이썬이 작동하는시간을 정지 시켜준다.
time.sleep(2)

selectedTeamHead = driver.find_element_by_css_selector(
    "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > thead")

selectedTeamBody = driver.find_element_by_css_selector(
    "#cphContents_cphContents_cphContents_udpContent > div.record_result > table > tbody")

# 기록에 관한 컬럼을 가져온다.
column = selectedTeamHead.find_elements_by_tag_name("th")
columnLen = len(column)
# 각 선수에대한 로우를 가져온다.
pitcher = selectedTeamBody.find_elements_by_tag_name("tr")
pitcherLen = len(pitcher)

# 각 선수별 데이터를 컬럼에 넣는다.
def insertData(onePitcher):
    data = {}
    for i in range(len(onePitcher.find_elements_by_tag_name("td"))):
        data[column[i].text] = onePitcher.find_elements_by_tag_name("td")[i].text
    return data

totalList = {}
# 투수의 길이만큼 반복한다.
for i in range(pitcherLen):
    # insertData함수를 이용하여 json형태로 반환 받는다.
    # 반환 받은 json을 totalList json에 넣는다.
    totalList[str(i)] = insertData(pitcher[i])

finList = json.dumps(totalList, indent=4, ensure_ascii= False)
print(finList)

with open("NC_Pitchers.json","w") as json_file:
    json.dump(totalList, json_file, indent=4, ensure_ascii= False)

