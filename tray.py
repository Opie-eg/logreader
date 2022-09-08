from multiprocessing.connection import wait
import os
import sys
from PySide2 import QtWidgets, QtGui
from threading import Thread
import time
import datetime #for reading present date
import win32evtlog # requires pywin32 pre-installed
import win32event
import win32con
from plyer import notification #for getting notification on your PC
import json
from multiprocessing import Process
from notify import notify_user 
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
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Hall RFID - Gestão de Portal')
        menu = QtWidgets.QMenu(parent)
        menu_title_icon= menu.addAction("Hall RFID - Gestão de Portal")
        menu_title_icon.setIcon(QtGui.QIcon("hallrfid.ico"))
        menu.addSeparator()

        #menudict= {}
        #with open("config.json") as json_data:
            #while checking:
                #if json_data["ip"+str(i)]:
                    #menudict["ping"+str(i)]= menu.addAction("Ping:"+ json_data["ip"+str(i)])
                    #menudict["ping"+str(i)].triggered.connect(self.ping_ip(json_data["ip"+str(i)],i,menudict))
                    #menudict["ping"+str(i)].setIcon(QtGui.QIcon("Hall_Red-33x16.png"))
                #else:
                    #checking= False
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

            if json_data["ip5"] is not None:
                self.ip5 = menu.addAction(json_data["ip5"][1])
                self.ip5.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip5.triggered.connect(self.ping_ip5)
               
            if json_data["ip6"] is not None:
                self.ip6 = menu.addAction(json_data["ip6"][1])
                self.ip6.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip6.triggered.connect(self.ping_ip6)
                

            if json_data["ip7"] is not None:
                self.ip7 = menu.addAction(json_data["ip7"][1])
                self.ip7.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip7.triggered.connect(self.ping_ip7)
               

            if json_data["ip8"] is not None:
                self.ip8 = menu.addAction(json_data["ip8"][1])
                self.ip8.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip8.triggered.connect(self.ping_ip8)
                

            if json_data["ip9"] is not None:
                self.ip9 = menu.addAction(json_data["ip9"][1])
                self.ip9.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip9.triggered.connect(self.ping_ip9)
               

            if json_data["ip10"] is not None:
                self.ip10 = menu.addAction(json_data["ip10"][1])
                self.ip10.setIcon(QtGui.QIcon("readyblue.png"))
                self.ip10.triggered.connect(self.ping_ip10)
                
        '''
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
                print(ip)
                self.menudict["ip{0}".format(ip)].triggered.connect(lambda opt=ip : print(opt))
                self.menudict["ip{0}".format(ip)].setIcon(QtGui.QIcon("readyblue.png"))
                hostlist.append(json_data[iplist[ip]][0])
               
            #print(iplist[ip],json_data[iplist[ip]][0],json_data[iplist[ip]][1])

        #open_cal = menu.addAction("Open Calculator")
        #open_cal.triggered.connect(self.open_calc)
        #open_cal.setIcon(QtGui.QIcon("Hall_Red-33x16.png"))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("Hall_Red-33x16.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        self.show()
       
    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            self.open_notepad()
        # if reason == self.Trigger:
        #     self.open_notepad()
    
    def openpage(self,hostname):
        webbrowser.open_new_tab(hostname)
    '''
    def ping_ip1(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip1"] is not None:
                  hostname= json_data["ip1"][0]
       
        
        webbrowser.open_new_tab(hostname)

    def ping_ip2(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip2"] is not None:
                  hostname= json_data["ip2"][0]
       
        webbrowser.open_new_tab(hostname)
    
    def ping_ip3(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip3"] is not None:
                  hostname= json_data["ip3"][0]
       
        webbrowser.open_new_tab(hostname)
    
    def ping_ip4(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip4"] is not None:
                  hostname= json_data["ip4"][0]
       
        webbrowser.open_new_tab(hostname)

    def ping_ip5(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip5"] is not None:
                  hostname= json_data["ip5"][0]
       
        webbrowser.open_new_tab(hostname)

    def ping_ip6(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip6"] is not None:
                  hostname= json_data["ip6"][0]
       
        webbrowser.open_new_tab(hostname)
    
    def ping_ip7(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip7"] is not None:
                  hostname= json_data["ip7"][0]
       
        webbrowser.open_new_tab(hostname)

    def ping_ip8(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip8"] is not None:
                  hostname= json_data["ip8"][0]
       
        webbrowser.open_new_tab(hostname)

    def ping_ip9(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip9"] is not None:
                  hostname= json_data["ip9"][0]
       
        webbrowser.open_new_tab(hostname)
        
    def ping_ip10(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip10"] is not None:
                  hostname= json_data["ip10"][0]
       
        webbrowser.open_new_tab(hostname)
    '''
    '''
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
                
                if json_data["ip3"] is not None:
                    response = ping(json_data["ip3"][0])
                    if response == True:
                        self.ip3.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip3.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip4"] is not None:
                    response = ping(json_data["ip4"][0])
                    if response == True:
                        self.ip4.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip4.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip5"] is not None:
                    response = ping(json_data["ip5"][0])
                    if response == True:
                        self.ip5.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip5.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip6"] is not None:
                    response = ping(json_data["ip6"][0])
                    if response == True:
                        self.ip6.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip6.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip7"] is not None:
                    response = ping(json_data["ip7"][0])
                    if response == True:
                        self.ip7.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip7.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip8"] is not None:
                    response = ping(json_data["ip8"][0])
                    if response == True:
                        self.ip8.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip8.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip9"] is not None:
                    response = ping(json_data["ip9"][0])
                    if response == True:
                        self.ip9.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip9.setIcon(QtGui.QIcon("notreadyred.png"))
                if json_data["ip10"] is not None:
                    response = ping(json_data["ip10"][0])
                    if response == True:
                        self.ip10.setIcon(QtGui.QIcon("readygreen.png"))
                    else:
                        self.ip10.setIcon(QtGui.QIcon("notreadyred.png"))
                
            time.sleep(60*15)
    '''        
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
            time.sleep(60*15)
    def open_notepad(self):
        """
        this function will open application
        :return:
        """
        os.system('notepad')

    def open_calc(self):
        """
        this function will open application
        :return:
        """
        os.system('calc')
    #def notify_user(self,source,info):
    #    self.showMessage("%s {}".format(datetime.date.today())%source, info)

#https://www.accadius.com/using-python-read-windows-event-logs-multiple-servers/
#https://www.blog.pythonlibrary.org/2010/07/27/pywin32-getting-windows-event-logs/
def alternative_Listening():
    ignored_notifications = ["Codigo a processar","Este codigo RFID não está autorizado a sair"]
    #server = '192.168.1.15' # name of the target computer to get event logs
    #logtype = 'Application' # 'Application' # 'Security'
    #filehandler = win32evtlog.OpenEventLog(server,logtype)
    #x = input("Nome De Utilizador: ")
    #y = getpass.getpass("Password: ")
    #sessionlogin = win32evtlog.EvtOpenSession(('192.168.1.15',x,'GUIA',y,win32evtlog.EvtRpcLoginAuthDefault), win32evtlog.EvtRpcLogin , 0 , 0 )     
    eventhandler = win32event.CreateEvent(None, 1, 0, "wait") #criar um evento como ponto de referencia
    flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ|\
            win32evtlog.EVENTLOG_BACKWARDS_READ 
    sub_flags = win32evtlog.EvtSubscribeToFutureEvents
    #win32evtlog.NotifyChangeEventLog(filehandler, eventhandler)
    subscription = win32evtlog.EvtSubscribe('Application', sub_flags, SignalEvent= eventhandler, Callback= None, Context= None,
    Query= "*", Session= None)
    while 1:
        testo(subscription,ignored_notifications)
        while 1:
            #print('waiting...')
            w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
            if w==win32con.WAIT_OBJECT_0:
               break
    #eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO MYEVENTSOURCE /D "My first Log"

def testo(subscription,ignored_notifications):
    events=win32evtlog.EvtNext(subscription, 10)
    if len(events)==0:
        return
    else:
        #for event in events:
            #print(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
        root = etree.fromstring(win32evtlog.EvtRender(events[0], win32evtlog.EvtRenderEventXml))
        provider = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Provider")#[@Name='Prototipo_PortalRFID']
        if provider is not None:
            computer = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Computer")
            data = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Data")
            if data is not None and not any(x in data.text for x in ignored_notifications):
            
                print(computer.text,data.text)
                notify_user(provider.text,data.text)
def icon_function():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("hallrfid.ico"), w)
    #while True:
        #tray_icon.cycle_ping()
        #time.sleep(60*15)
    Thread(target = tray_icon.cycle_ping).start()
    sys.exit(app.exec_())
  
    #tray_icon.showMessage('VFX Pipeline', 'Hello "Name of logged in ID')
    #alternative_Listening(tray_icon)
    

def main():
    Thread(target = icon_function).start()
    Thread(target = alternative_Listening).start()

if __name__ == '__main__':
    main()



'''
   while 1:
        while 1:
            events=win32evtlog.EvtNext(s, 10)
            if len(events)==0:
                break
            for event in events:
                print (win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            print('retrieved %s events' %len(events))
            notify_user("beep","boop")
        while 1:
            #print('waiting...')
            w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
            if w==win32con.WAIT_OBJECT_0:
                break
            '''

'''cursorlog = win32evtlog.GetNumberOfEventLogRecords(filehandler)
    cursorlog += 1
    print("Go to : %s" % (cursorlog))#localizacao do evento criado
    while looping == True:
        #the timeout delay can be set to 0xFFFFFFF for infinite timeout
        result = win32event.WaitForSingleObjectEx(eventhandler, 2000,True)
        # Timeout
        if result == win32con.WAIT_OBJECT_0:
            #print("CURSORLOG: %s" % (cursorlog) )
            readlog = win32evtlog.ReadEventLog(win32evtlog.OpenEventLog(server,logtype), flags, 1)
            #readlog = win32evtlog.ReadEventLog(filehandler, flags, 0)
            #readlog = win32evtlog.EvtNext(s, 10)
            #print(len(readlog)) #sempre 22 por alguma razao???
            readlog= [readlog[0]]
            for event in readlog:
                #print(event)
                #http://timgolden.me.uk/pywin32-docs/PyEventLogRecord.html
                print("%s : [%s] : %s" % (event.TimeGenerated.Format(), event.RecordNumber, event.SourceName))
                p= Process(target =  notify_user, args=(event.SourceName,event.StringInserts[0],))
                p.start()
                p.join()
                notify_user(event.SourceName,event.StringInserts[0])
            cursorlog+=len(readlog)
            
   '''