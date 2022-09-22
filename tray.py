import sys
import pythoncom
from PySide2 import QtWidgets, QtGui
from threading import Thread
import time
import win32evtlog # requires pywin32 pre-installed
import win32event
import win32con
import json
from notify import notify_user 
import wmi
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import webbrowser
import getpass
from lxml import etree
from lxml.etree import _Element as Element, _ElementTree as ElementTree
import os 
looping = True

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr= subprocess.PIPE)
    streamdata = process.communicate()[0]
    #print(str(streamdata))
    if not 'Reply from {host}'in str(streamdata):
        if  'Destination host unreachable.' in str(streamdata):
            return  False
        else:
            return True
    else:
        return False

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent, server, netdomain, userinput, passinput):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.server = server
        self.netdomain = netdomain
        self.userinput= userinput
        self.passinput= passinput
        self.setToolTip(f'Hall RFID - Gestão de Portal')
        menu = QtWidgets.QMenu(parent)
        self.menu_title_icon= menu.addAction("Hall RFID - Gestão de Portal")
        self.menu_title_icon.setIcon(QtGui.QIcon("ICONE_AZUL.ico"))
        menu.addSeparator()
        menu.setToolTipsVisible(True)
        # Creating menu options based on ip"x" values in config.json each one of the menu options opens a page with the respective ip address.
        self.menudict = {}
        iplist= []
        hostlist = []
        with open("config.json") as f:
            json_data = json.load(f)
            for i in json_data:
                if "ip" in i:
                    iplist.append(i)
            for ip in range(0,len(iplist)):
                self.menudict["ip{0}".format(ip)]= menu.addAction(json_data[iplist[ip]][1])
                self.menudict["ip{0}".format(ip)].triggered.connect(lambda ignored= iplist, a= ip: webbrowser.open_new_tab(json_data[iplist[a]][0]))
                self.menudict["ip{0}".format(ip)].setIcon(QtGui.QIcon("readyblue.png"))
                self.menudict["ip{0}".format(ip)].setToolTip('Abrir Página de Administração')
                hostlist.append(json_data[iplist[ip]][0]) 
                #print(iplist[ip],json_data[iplist[ip]][0],json_data[iplist[ip]][1])
        menu.addSeparator()
        self.service_option = menu.addAction("Serviço RFID")
        self.service_option.setIcon(QtGui.QIcon("readyblue.png"))
        self.service_option.triggered.connect(lambda : Thread(target = self.start_service).start())
        self.service_option.setToolTip('Clicar para ligar o Serviço.')
        #self.service_option.setToolTip('Serviço ativo')
          
        menu.addSeparator()

        exit_ = menu.addAction("Sair")
        exit_.triggered.connect(lambda: sys.exit())
        

        menu.addSeparator()
        self.setContextMenu(menu)
        #self.activated.connect(self.onTrayIconActivated)
        self.show()

    def connect_computer_services(self,cycle=None):
        with open("config.json") as f:
                json_data = json.load(f)
        while True:
            pythoncom.CoInitialize()
            try:
                print("Starting Connection to server...")
                username = "%s\\%s" % (self.netdomain, self.userinput)
                computer = wmi.WMI(self.server, user = username, password = self.passinput)
                #c = wmi.WMI("MachineB", user=r"GUIA\fred", passwor\d ="secret")
                print("...Success!")
                stopped_services = computer.Win32_Service (State="Stopped")
                servicefound = False
                if stopped_services:
                    for s in stopped_services:
                        if s.Name == "Prototipo_ServicoPortalRFID":
                            print(s.Caption, "service is not running")
                            servicefound = True
                            #computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
                            self.service_option.setIcon(QtGui.QIcon("notreadyred.png"))
                            self.setIcon(QtGui.QIcon("ICONE_VERMELHO.ico"))
                            
                    if servicefound == False:
                        self.service_option.setIcon(QtGui.QIcon("readygreen.png"))
                        self.setIcon(QtGui.QIcon("ICONE_AZUL.ico"))
            finally:
                pythoncom.CoUninitialize()
            if cycle == None:
                time.sleep(60*60*json_data["tempo_espera_servico_horas"])
            else:
                break
                
    
    def start_service(self):
        pythoncom.CoInitialize()
        try:
            print("Starting Connection to server...")
            username = "%s\\%s" % (self.netdomain, self.userinput)
            computer = wmi.WMI(self.server, user = username, password = self.passinput)
            print("...Success!")
            computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
            self.connect_computer_services(self,1)
        finally:
            pythoncom.CoUninitialize()
    '''
    def start_service(self):
        print("Starting Connection to server...")
        username = "%s\\%s" % (self.netdomain, self.userinput)
        computer = wmi.WMI(self.server, user = username, password = self.passinput)
        print("...Success!")
        computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
        self.connect_computer_services()
    '''
    
    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.open_notepad()
        #if reason == self.Trigger:
        #     self.open_notepad()

    # Goes through the previously created ip"x" menus and changes their icon depending on the response to their respective ip's assigned in config.json
    def cycle_ping(self):
        counter = 0
        with open("config.json") as f:
            json_data = json.load(f)
        while True:
            for i in self.menudict:
                response = ping(json_data[i][0])
                if response == True:
                    counter += 1
                    self.menudict[i].setIcon(QtGui.QIcon("readygreen.png"))
                else:
                    self.menudict[i].setIcon(QtGui.QIcon("notreadyred.png"))
                #self.menudict[i].triggered.connect(lambda: self.openpage("google"))
            if counter < len(self.menudict):
                self.setIcon(QtGui.QIcon("ICONE_LARANJA.ico"))
            elif counter >= len(self.menudict):
                self.setIcon(QtGui.QIcon("ICONE_AZUL.ico"))
            counter = 0 
            time.sleep(60*json_data["tempo_espera_ping_minutos"])


#https://www.accadius.com/using-python-read-windows-event-logs-multiple-servers/
#https://www.blog.pythonlibrary.org/2010/07/27/pywin32-getting-windows-event-logs/
def eventlog_Listening(userinput,passinput,ignored_notifications,server,netdomain):
    logtype = 'Application' # 'Application' # 'Security'
    sessionlogin = win32evtlog.EvtOpenSession((server,userinput,netdomain,passinput,win32evtlog.EvtRpcLoginAuthDefault), win32evtlog.EvtRpcLogin , 0 , 0 )     
    eventhandler = win32event.CreateEvent(None, 1, 0, "wait") #criar um evento como ponto de referencia
    sub_flags = win32evtlog.EvtSubscribeToFutureEvents
    subscription = win32evtlog.EvtSubscribe(logtype, sub_flags, SignalEvent= eventhandler, Callback= None, Context= None,
    Query= "*", Session= sessionlogin)
    read_event(subscription,ignored_notifications)
    while 1:
        w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
        if w==win32con.WAIT_OBJECT_0:
            read_event(subscription,ignored_notifications)
            #w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
            time.sleep(2)

    #eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO MYEVENTSOURCE /D "My first Log"

def read_event(subscription,ignored_notifications):
    events=win32evtlog.EvtNext(subscription, 10)
    print(events)
    if len(events)==0:
        return
    else:
        for event in events:
            #print(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            root = etree.fromstring(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            provider = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Provider")#[@Name='Prototipo_PortalRFID']")
            info = []
            if provider is not None:
                computer = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Computer")
                data = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Data")
                if data is not None:
                    res = [ele for ele in ignored_notifications if(ele in data.text)]
                    if bool(res) == False:
                        new_info= computer.text + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + data.text
                        info.append(new_info)
                        print(new_info)
                        #new func here
                        notify_user(data.text)
            if len(info) > 0:
                record_log(info)

def record_log(info):
    file_name = 'event_logs.log'
    stat_file = 'statistics.txt'
    if os.path.exists(file_name):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    f = open(file_name, append_write)  # open file in write mode
    for i in info:
        f.write(i)
    f.close()

    if os.path.exists(stat_file):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    f = open(file_name, "r")
    f2 = open(stat_file, append_write)
    for i in f:
        if i == "X":
            pass
        elif i== "Y":
            pass
    f.close
    f2.close

def icon_function(server,netdomain,userinput,passinput):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    
    tray_icon = SystemTrayIcon(QtGui.QIcon("ICONE_AZUL.ico"), w , server,netdomain,userinput,passinput)
    Thread(target = tray_icon.cycle_ping).start()
    Thread(target = tray_icon.connect_computer_services).start()
    sys.exit(app.exec_())
  
def main():
    with open("config.json") as f:
        json_data = json.load(f)
    ignored_notifications = json_data["ignored_notifications"]
    server = json_data["server"] # name of the target computer to get event logs
    netdomain= json_data["network_domain"]# name of the network domain to connect to
    userinput = input("Nome De Utilizador: ")
    passinput = getpass.getpass("Password: ")
    Thread(target = icon_function, args=(server,netdomain,userinput,passinput,)).start()
    Thread(target = eventlog_Listening , args=(userinput,passinput,ignored_notifications,server,netdomain,)).start()
    

if __name__ == '__main__':
    main()

