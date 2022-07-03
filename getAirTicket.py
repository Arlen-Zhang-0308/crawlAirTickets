import requests, time, csv, tqdm
from bs4 import BeautifulSoup

header = {
    'authority':'flights.ctrip.com',
    'method':'POST',
    'path':'/itinerary/api/12808/products',
    'scheme':'https',
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    #'content-length':'288',
    'content-type':'application/json',
    'cookie':'cookie:_abtest_userid=06b0b441-66ab-4967-bd87-e88e24b69927; _RF1=183.94.121.207; _RSG=BGqXPqr3Ky6hmC.53OCdIB; _RDG=280054ba88ed422e2e24dbd137dc1f020c; _RGUID=6f140f5d-1987-440b-b4a7-3180c5f8cc2b; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1576128839632; MKT_CKID=1575524039652.xet2w.ka75; _ga=GA1.2.1451907420.1575524040; _gid=GA1.2.823502183.1575524040; MKT_Pagesource=PC; DomesticUserHostCity=WUH|%ce%e4%ba%ba; gad_city=2b565ea2e8ff53ecb7394782e7e5595d; appFloatCnt=2; FD_SearchHistorty={"type":"S","data":"S%24%u6B66%u6C49%28WUH%29%24WUH%242020-01-02%24%u4E0A%u6D77%28SHA%29%24SHA"}; _bfa=1.1575524030898.v7vcy.1.1575524030898.1575528974404.2.21; _bfs=1.8; _jzqco=%7C%7C%7C%7C1575524039807%7C1.800332023.1575524039648.1575529128177.1575529187541.1575529128177.1575529187541.undefined.0.0.16.16; __zpspc=9.2.1575528974.1575529187.5%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D21%26v2%3D20',
    'origin':'https://flights.ctrip.com',
    'referer':'https://flights.ctrip.com/itinerary/oneway/wuh-tao?date=2020-01-12',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'
}

def write_file(filename,wrcontent,typ = 'wb'):                                                                              #下载文件函数
    with open(filename,typ, errors = 'ignore') as hf:
        hf.write(wrcontent)
        hf.flush()
        hf.close()

def getTickets(fro="青岛", to="广州", date="2022-07-08", code=0): 
    cities = []

    with open("airportName.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            cities.append(line[:-1].split(','))
    del lines

    if code == 0:
        for city in cities: 
            if fro == city[1]:
                fromCode = city[0]
                fromCity = city[1]
            if to == city[1]:
                toCode = city[0]
                toCity = city[1]
    else: 
        for city in cities: 
            if fro == city[0]:
                fromCode = city[0]
                fromCity = city[1]
            if to == city[0]:
                toCode = city[0]
                toCity = city[1]
    del cities
    time.sleep(0.8)
    
    mainPage = requests.get("http://www.9935china-air.com/tools/query.aspx?t=0.5&sc=" + fromCode + 
                            "&ec=" + toCode + "&sd=" + date)
    mainPage_B = BeautifulSoup(mainPage.text, "html.parser")
    
    newstyledetails = mainPage_B.find_all("ul", class_="newstyledetails1")

    for details in newstyledetails: 
        detail = details.find("li", class_="details1_li1")
        fromTime = detail.find("strong").text
        toTime = detail.find("span").text

        detail = details.find("li", class_="details1_li2")
        airportName = detail.find_all('p')
        fromAirport = airportName[0].text
        toAirport = airportName[1].text

        detail = details.find("li", class_="details1_li3")
        flightInfo = detail.find_all("span")
        flightName = flightInfo[0].text
        flight = flightInfo[1].text
        plane = flightInfo[3].text

        detail = details.find("li", class_="details1_li4")
        price = int(detail.find("strong").text)

        csvLine = [date, fromCity, toCity, fromTime, toTime, fromAirport, toAirport, flightName, flight, plane, price]
        if csvLine != []: 
            writer.writerow(csvLine)
        del csvLine

if __name__ == "__main__": 
    cities = []

    file = open("airTickets.csv", 'w', newline='')

    global writer
    writer = csv.writer(file)

    csvHeader = ["日期", "出发城市", "到达城市", "起飞时间", "降落时间", "起飞机场", "降落机场", "航空公司", "航班", "机型", "价格"]
    writer.writerow(csvHeader)
    file.flush()

    with open("airportName.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            cities.append(line[:-1].split(','))
    del lines
    for n, city1 in enumerate(cities): 
        time.sleep(0.8)
        print(n)
        for city2 in tqdm.tqdm(cities): 
            getTickets(city1[0], city2[0], "2022-07-08", 1)
            if city1[1] == city2[1]:
                continue
            file.flush()
        break
    file.close()