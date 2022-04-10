import json
import requests
import math
from fake_useragent import UserAgent

class BDL:
    def __init__(self,bv,ep_id=1,style=1,qua=80):
        self.bv=bv
        self.epid=int(ep_id-1)
        self.style=style
        self.qua=qua
    
    def bvtoav(self):
        BvNo1 = self.bv[2:]
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
        self.av=sum ^ temp
    
    def change_UA(self):
        UA=UserAgent()
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3883.400 QQBrowser/10.8.4559.400"}#UA.random}

    def get_cid(self,page=None):
        page=int(input("What page do you want?:"))
        req=requests.get(url="https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp".format(self.av),headers=self.headers)
        con=json.loads(req.text)
        cid=con.get("data")[page-1]["cid"]
        part=con.get("data")[page-1]["part"]
        self.cid=cid
        self.part=part

    def get_save(self):
        if self.style==2:
            while True:
                try:
                    self.epid+=1
                    req=requests.get(url="https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&epid={}&type=&otype=json".format(self.av,self.cid,self.qua,self.epid),headers=self.headers)
                    con=json.loads(req.text)
                    url=con["data"]["durl"][0]["url"]
                    self.headers["referer"]="https://www.bilibili.com/av{}".format(self.av)
                    file=requests.get(url=url,headers=self.headers)
                    with open("{}.flv".format(self.part),"wb") as f:
                       for data in file.iter_content(1024):
                           f.write(data)
                except IndexError:
                    break
        elif self.style==1:
            req=requests.get(url="https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json".format(self.av,self.cid,self.qua),headers=self.headers)
            con=json.loads(req.text)
            url=con["data"]["durl"][0]["url"]
            self.headers["referer"]="https://www.bilibili.com/av{}".format(self.av)
            file=requests.get(url=url,headers=self.headers)
            with open("{}.flv".format(self.part),"wb") as f:
                for data in file.iter_content(1024):
                    f.write(data)
    
    def start(self):
        self.bvtoav()
        self.change_UA()
        self.get_cid()
        self.get_save()

a=BDL(bv="BV17x411g7zn",style=2)
a.start()