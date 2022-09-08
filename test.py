import json
'''
with open("config.json") as f:
    json_data = json.load(f)
    if json_data["ip1"] is not None:
        self.ip1 = menu.addAction(json_data["ip1"][1])
        self.ip1.setIcon(QtGui.QIcon("readyblue.png"))
        self.ip1.triggered.connect(self.ping_ip1)

    if json_data["ip2"] is not None:
        self.ip2 = menu.addAction(json_data["ip2"][1])
        self.ip2.setIcon(QtGui.QIcon("readyblue.png"))
        self.ip2.triggered.connect(self.ping_ip2)
        
    if json_data["ip3"] is not None:
        self.ip3 = menu.addAction(json_data["ip3"][1])
        self.ip3.setIcon(QtGui.QIcon("readyblue.png"))
        self.ip3.triggered.connect(self.ping_ip3)
        
    if json_data["ip4"] is not None:
        self.ip4 = menu.addAction(json_data["ip4"][1])
        self.ip4.setIcon(QtGui.QIcon("readyblue.png"))
        self.ip4.triggered.connect(self.ping_ip4)


def ping_ip1(self):
    with open("config.json") as f:
        json_data = json.load(f)
        if json_data["ip1"] is not None:
            hostname= json_data["ip1"][0]
    
    
    webbrowser.open_new_tab(hostname)

def cycle_ping(self):
    while True:
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip1"] is not None:
                response = ping(json_data["ip1"][0])
                if response == True:
                    self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
                else:
                    self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
                    
            if json_data["ip2"] is not None:
                response = ping(json_data["ip2"][0])
                if response == True:
                    self.ip2.setIcon(QtGui.QIcon("readygreen.png"))
                else:
                    self.ip2.setIcon(QtGui.QIcon("notreadyred.png"))
'''
menudict = {}
webpagedict = {}
iplist= []
with open("config.json") as f:
    json_data = json.load(f)
    for i in json_data:
        if "ip" in i:
            iplist.append(i)
    for ip in range(0,len(iplist)):
        menudict["ip{0}".format(ip)]= "beep{0}".format(ip) #menu.addAction(json_data[iplist[ip]][1])
        #menudict["ip{0}".format(ip)].setIcon(QtGui.QIcon("readyblue.png"))
        webpagedict["page{0}".format(ip)]= "boop"#webbrowser.open_new_tab(json_data[iplist[ip]][0])
        menudict["ip{0}".format(ip)] +=  webpagedict["page{0}".format(ip)] #.triggered.connect(webpagedict["page{0}".format(ip)])
        #print(iplist[ip],json_data[iplist[ip]][0],json_data[iplist[ip]][1])
    #print(menudict)

def altcycle_ping(self):
    with open("config.json") as f:
        json_data = json.load(f)
    while True:
        for i in self.menudict:
            response = ping(json_data[i][0])
            if response == True:
                self.menudict[ip].setIcon(QtGui.QIcon("readygreen.png"))
            else:
                self.menudict[ip].setIcon(QtGui.QIcon("notreadyred.png"))


