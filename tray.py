import sys
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
    print(str(streamdata))
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
        menu_title_icon= menu.addAction("Hall RFID - Gestão de Portal")
        menu_title_icon.setIcon(QtGui.QIcon("hallrfid.ico"))
        menu.addSeparator()

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
                hostlist.append(json_data[iplist[ip]][0]) 
                #print(iplist[ip],json_data[iplist[ip]][0],json_data[iplist[ip]][1])
        menu.addSeparator()

        self.service_option = menu.addAction("Serviço RFID")
        self.service_option.setIcon(QtGui.QIcon("notreadyred.png"))
        self.service_option.triggered.connect(self.connect_computer_services)
        self.service_option.setToolTip(f'Clique para ligar Reader')
        menu.addSeparator()

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("Hall_Red-33x16.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        #self.activated.connect(self.onTrayIconActivated)
        self.show()
    def connect_computer_services(self):
        print("Starting Connection to server...")
        username = "%s\\%s" % (self.netdomain, self.userinput)
        computer = wmi.WMI(self.server, user = username, password = self.passinput)
        #c = wmi.WMI("MachineB", user=r"GUIA\fred", password ="secret")
        print("...Success!")
        stopped_services = computer.Win32_Service (State="Stopped")
        if stopped_services:
            for s in stopped_services:
                if s.Name == "Prototipo_ServicoPortalRFID":
                    print(s.Caption, "service is not running")
                    computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
                    self.service_option.setIcon(QtGui.QIcon("readygreen.png"))
            self.service_option.setIcon(QtGui.QIcon("readygreen.png"))

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
        with open("config.json") as f:
            json_data = json.load(f)
        while True:
            for i in self.menudict:
                response = ping(json_data[i][0])
                if response == True:
                    self.menudict[i].setIcon(QtGui.QIcon("readygreen.png"))
                else:
                    self.menudict[i].setIcon(QtGui.QIcon("notreadyred.png"))
                self.menudict[i].triggered.connect(lambda: self.openpage("google"))
            time.sleep(60*json_data["tempo_espera_ping"])


#https://www.accadius.com/using-python-read-windows-event-logs-multiple-servers/
#https://www.blog.pythonlibrary.org/2010/07/27/pywin32-getting-windows-event-logs/
def eventlog_Listening(userinput,passinput,ignored_notifications,server,netdomain):
    #with open("config.json") as f:
        #json_data = json.load(f)
    
    #ignored_notifications = json_data["ignored_notifications"]
    #print(ignored_notifications)
    #server = json_data["server"] # name of the target computer to get event logs
    #netdomain= json_data["network_domain"]# name of the network domain to connect to
    logtype = 'Application' # 'Application' # 'Security'
    #filehandler = win32evtlog.OpenEventLog(server,logtype)
    #win32evtlog.NotifyChangeEventLog(filehandler, eventhandler)
    #flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ|win32evtlog.EVENTLOG_BACKWARDS_READ 
    #x = userinput #input("Nome De Utilizador: ")
    #y = passinput #getpass.getpass("Password: ")
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
            time.sleep(2)

    #eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO MYEVENTSOURCE /D "My first Log"

def read_event(subscription,ignored_notifications):
    events=win32evtlog.EvtNext(subscription, 10)
    if len(events)==0:
        return
    else:
        for event in events:
            #print(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            root = etree.fromstring(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            provider = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Provider[@Name='Prototipo_PortalRFID']")#
            if provider is not None:
                computer = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Computer")
                data = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Data")
                res = [ele for ele in ignored_notifications if(ele in data.text)]
                if data is not None and bool(res) == False:
                    print(computer.text,data.text)
                    notify_user(data.text)


def icon_function(server,netdomain,userinput,passinput):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("hallrfid.ico"), w , server,netdomain,userinput,passinput)
    Thread(target = tray_icon.cycle_ping).start()
    sys.exit(app.exec_())
  
    

def service_listening():
    pass

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

