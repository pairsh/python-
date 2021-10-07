import json
import requests
import math

BV=input('请输入BV号(例如：BV1764y1975D )：')

def BvToAv(Bv):
    BvNo1 = Bv[2:]
    keys = {
        '1':'13', '2':'12', '3':'46', '4':'31', '5':'43', '6':'18', '7':'40', '8':'28', '9':'5',
        'A':'54', 'B':'20', 'C':'15', 'D':'8', 'E':'39', 'F':'57', 'G':'45', 'H':'36', 'J':'38', 'K':'51', 'L':'42', 'M':'49', 'N':'52', 'P':'53', 'Q':'7', 'R':'4', 'S':'9', 'T':'50', 'U':'10', 'V':'44', 'W':'34', 'X':'6', 'Y':'25', 'Z':'1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41', 'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14','z':'19'
    }
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))

    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6));
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2));
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4));
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8));
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5));
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9));
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3));
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7));
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1));
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0));

    sum = 0
    for i in BvNo2:
        sum += i

    sum -= 100618342136696320
    
    temp = 177451812
    return sum ^ temp


headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400",
"referer":""}
AV=BvToAv(BV)
i=int(input("请选择下载哪一P："))
def get_requests(av):
    a=requests.get(url="https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp".format(av),headers=headers)
    b=json.loads(a.text)
    c=b.get("data")[i-1]["cid"]
    d=b.get("data")[i-1]["part"]
    return c,d
r,k=get_requests(AV)
q=int(input("请选择清晰度(请输入数字，16为360p,32为480p,64为720p,80为1080P)："))
def get_and_save_flv_url(e,k):
    a=requests.get(url="https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json".format(AV,e,q),headers=headers)
    c=json.loads(a.text)
    b=c["data"]["durl"][0]["url"]
    headers["referer"]="https://www.bilibili.com/av{}".format(AV)
    r=requests.get(url=b,headers=headers)
    with open("{}.flv".format(k),"wb") as f:
        for data in r.iter_content(1024):
            f.write(data)

get_and_save_flv_url(r,k)