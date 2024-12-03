import requests
from bs4 import BeautifulSoup
def scrapyxcf(web):
    if not web:
        return None
    result = ""
    response= requests.get(web)
    soup = BeautifulSoup(response.text,"html.parser")
    resources = soup.findAll("td",attrs={"class":"name"})
    #print("材料")
    for food in resources:
        result += food.text
    steps = soup.findAll("p",attrs={"class":"text"})
    #print("步骤")
    for step in steps:
        result += step.text
    return result
def xcfsearch(name):
    if not name:
        return None
    pres="https://www.xiachufang.com/search/?keyword="
    web=pres+name
    response = requests.get(web)
    soup = BeautifulSoup(response.text,"html.parser")
    dest = "https://www.xiachufang.com/"+soup.find("p",{"class":"name"}).a['href']
    return dest
def hbsearch(name:str):
    pres = "https://www.boohee.com/food/search?keyword="
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
, "cookie":"Hm_lvt_7263598dfd4db0dc29539a51f116b23a=1726373413; HMACCOUNT=0CA9E86C7E024B34; acw_tc=0bca294217263773034162859eb5589e306bfa5d40cbec2c4965eed4d8bbba; _mboohee_session=cDhLNjhDOFFhV0tEZDArU2lXTW1MQ1NFZjdsUFY5Q1VEeURvNlk5Szdzb2gvMXdVSjcrNEtoR0xQeEF2aTIzUG5lNkhQYzBhUEphUVgrdDM1OTh1VlNTM0l4UHZDWVIxTTBLSmVRdTAybjcrbVFuRlpCRlloaVJEVXgxbHphNDBWTGdicm9UajRPbnlVVlRmcWhYNUVRPT0tLVpYWlk3d2hOQnpxSG5ZOWRURkRHMFE9PQ%3D%3D--5e0552918ee001ec3a70e80671662a5c692e4eb2; Hm_lpvt_7263598dfd4db0dc29539a51f116b23a=1726378663"}
    web=pres+name
    response = requests.get(web,headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    print(soup.find("ul").find("li").find("p").text.strip())
if __name__ == "__main__":
    print(scrapyxcf(xcfsearch('土豆炒肉')))
