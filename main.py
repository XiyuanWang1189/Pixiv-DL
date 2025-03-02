import requests
import bs4
import json

UserId = ""
Url = "https://www.pixiv.net/ajax/user/" + UserId + "/profile/all?sensitiveFilterMode=userSetting&lang=zh&version=7be51036945f7f940ffa9923c2e13b8a3f9634cd"
Hs = {
    "Priority": "u=1, i",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Accept": "application/json",
    "Baggage": "",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "",
    "Sentry-Trace": "",
    "X-User-Id": "",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.pixiv.net/",
    "Cookie": ""
}
SubHs = {
    "Priority": "u=1, i",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Baggage": "",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.pixiv.net/",
}
pro = {"http": "", "https": ""}
Req = requests.get(Url, headers=Hs, proxies=pro)
Req.raise_for_status()
Req.encoding = Req.apparent_encoding
Bs = bs4.BeautifulSoup(Req.text)
print("Request OK")
print("*"*30)
aws = json.loads(Bs.find("body").find("p").text).get("body").get("illusts").keys()
print("Analysis-0 OK")
print("*"*30)
aws = list(aws)
index = 1
for aw in aws:
    SubUrl = "https://www.pixiv.net/ajax/user/" + UserId + "/profile/illusts?ids%5B%5D=" + aw + "&work_category=illust&is_first_page=0&sensitiveFilterMode=userSetting&lang=zh&version=7be51036945f7f940ffa9923c2e13b8a3f9634cd"
    SubR = requests.get(SubUrl, headers=Hs, proxies=pro)
    SubR.raise_for_status()
    SubR.encoding = SubR.apparent_encoding
    SubBs = bs4.BeautifulSoup(SubR.text)
    js = json.loads(SubBs.find("body").find("p").text).get("body").get("works")
    js = js.get(list(js.keys())[0])
    Title = js.get("title")
    Src = js.get("url")
    Src2 = Src.replace("c/250x250_80_a2/custom-thumb", "img-original")\
        .replace("_custom1200", "")\
        .replace("c/250x250_80_a2/img-master", "img-original")\
        .replace("_square1200", "")
    Src1 = Src2.replace("jpg", "png")
    print("Analysis-" + str(index) +" OK")
    print("*" * 30)
    try:
        Img = requests.get(Src1, headers=SubHs, stream=True, proxies=pro)
        Img.raise_for_status()
        Img.encoding = Img.apparent_encoding
    except requests.exceptions.HTTPError:
        Img = requests.get(Src2, headers=SubHs, stream=True, proxies=pro)
        Img.raise_for_status()
        Img.encoding = Img.apparent_encoding
    fn = Title + "-" + str(index) + ".jpg"
    with open(fn, 'wb') as f:
        f.write(Img.content)
    print("Save " + fn + " OK")
    print("*" * 30)
    index += 1
