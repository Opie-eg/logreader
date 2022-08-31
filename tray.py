import os
import sys
from PySide2 import QtWidgets, QtGui
from threading import Thread
import time
import datetime #for reading present date
import win32evtlog # requires pywin32 pre-installed
import win32event
from plyer import notification #for getting notification on your PC
import json

looping = True


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
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip1"] is not None:
                self.ip1 = menu.addAction(json_data["ip1"][1])
                self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
                self.ip1.triggered.connect(self.ping_ip1)

            if json_data["ip2"] is not None:
                ip2 = menu.addAction(json_data["ip2"][1])
                ip2.setIcon(QtGui.QIcon("notreadyred.png"))
                ip2.triggered.connect(self.ping_ip2)
                
            if json_data["ip3"] is not None:
                ip3 = menu.addAction(json_data["ip3"][1])
                ip3.setIcon(QtGui.QIcon("notreadyred.png"))
                ip3.triggered.connect(self.ping_ip3)
                
            if json_data["ip4"] is not None:
                ip4 = menu.addAction(json_data["ip4"][1])
                ip4.setIcon(QtGui.QIcon("notreadyred.png"))
                ip4.triggered.connect(self.ping_ip4)

            if json_data["ip5"] is not None:
                ip5 = menu.addAction(json_data["ip5"][1])
                ip5.setIcon(QtGui.QIcon("notreadyred.png"))
                ip5.triggered.connect(self.ping_ip5)
               
            if json_data["ip6"] is not None:
                ip6 = menu.addAction(json_data["ip6"][1])
                ip6.setIcon(QtGui.QIcon("notreadyred.png"))
                ip6.triggered.connect(self.ping_ip6)
                

            if json_data["ip7"] is not None:
                ip7 = menu.addAction(json_data["ip7"][1])
                ip7.setIcon(QtGui.QIcon("notreadyred.png"))
                ip7.triggered.connect(self.ping_ip7)
               

            if json_data["ip8"] is not None:
                ip8 = menu.addAction(json_data["ip8"][1])
                ip8.setIcon(QtGui.QIcon("notreadyred.png"))
                ip8.triggered.connect(self.ping_ip8)
                

            if json_data["ip9"] is not None:
                ip9 = menu.addAction(json_data["ip9"][1])
                ip9.setIcon(QtGui.QIcon("notreadyred.png"))
                ip9.triggered.connect(self.ping_ip9)
               

            if json_data["ip10"] is not None:
                ip10 = menu.addAction(json_data["ip10"][1])
                ip10.setIcon(QtGui.QIcon("notreadyred.png"))
                ip10.triggered.connect(self.ping_ip10)
                

        #open_cal = menu.addAction("Open Calculator")
        #open_cal.triggered.connect(self.open_calc)
        #open_cal.setIcon(QtGui.QIcon("Hall_Red-33x16.png"))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("notreadyred.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

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
    
    def ping_ip1(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip1"] is not None:
                  hostname= json_data["ip1"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            
        else:
            print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("readyblue.png"))

    def ping_ip2(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip2"] is not None:
                  hostname= json_data["ip2"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip2"][1],json_data["ip2"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip2"][1],json_data["ip2"][1]+' is down!')
    
    def ping_ip3(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip3"] is not None:
                  hostname= json_data["ip3"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip3"][1],json_data["ip3"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip3"][1],json_data["ip2"][1]+' is down!')
    
    def ping_ip4(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip4"] is not None:
                  hostname= json_data["ip4"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip4"][1],json_data["ip4"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip4"][1],json_data["ip4"][1]+' is down!')

    def ping_ip5(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip5"] is not None:
                  hostname= json_data["ip5"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip5"][1],json_data["ip5"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip5"][1],json_data["ip5"][1]+' is down!')

    def ping_ip6(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip6"] is not None:
                  hostname= json_data["ip6"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip6"][1],json_data["ip6"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip6"][1],json_data["ip6"][1]+' is down!')
    
    def ping_ip7(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip7"] is not None:
                  hostname= json_data["ip7"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip7"][1],json_data["ip7"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip7"][1],json_data["ip7"][1]+' is down!')

    def ping_ip8(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip8"] is not None:
                  hostname= json_data["ip8"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip8"][1],json_data["ip8"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip8"][1],json_data["ip8"][1]+' is down!')

    def ping_ip9(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip9"] is not None:
                  hostname= json_data["ip9"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip9"][1],json_data["ip9"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip9"][1],json_data["ip9"][1]+' is down!')
        
    def ping_ip10(self):
        """
        this function will ping json ip1
        :return:
        """
        with open("config.json") as f:
            json_data = json.load(f)
            if json_data["ip10"] is not None:
                  hostname= json_data["ip10"][0]
       
        response = os.system("ping " + hostname)
        if response == 0:
            #print(hostname, 'is up!')
            self.ip1.setIcon(QtGui.QIcon("readygreen.png"))
            notify_user(json_data["ip10"][1],json_data["ip10"][1]+' is up!')
        else:
            #print(hostname, 'is down!')
            self.ip1.setIcon(QtGui.QIcon("notreadyred.png"))
            notify_user(json_data["ip10"][1],json_data["ip10"][1]+' is down!')


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


def alternative_Listening():
    server = 'localhost' # name of the target computer to get event logs
    logtype = 'Application' # 'Application' # 'Security'
    filehandler = win32evtlog.OpenEventLog(server,logtype)
    eventhandler = win32event.CreateEvent(None, 1, 0, "wait") #criar um evento como ponto de referencia
    flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ|\
            win32evtlog.EVENTLOG_BACKWARDS_READ 
            
    win32evtlog.NotifyChangeEventLog(filehandler, eventhandler)
    cursorlog = win32evtlog.GetNumberOfEventLogRecords(filehandler)
    cursorlog+=1
    print("Go to : %s" % (cursorlog))#localizacao do evento criado
    while looping == True:
        #the timeout delay can be set to 0xFFFFFFF for infinite timeout
        result = win32event.WaitForSingleObject(eventhandler, 1)
        # Timeout
        if not result :
            #print("CURSORLOG: %s" % (cursorlog) )
            readlog = win32evtlog.ReadEventLog(win32evtlog.OpenEventLog(server,logtype), flags, 1)
            #print(len(readlog)) sempre 22 por alguma razao???
            readlog= [readlog[0]]
            for event in readlog:
                #print(event)
                #http://timgolden.me.uk/pywin32-docs/PyEventLogRecord.html
                print("%s : [%s] : %s" % (event.TimeGenerated.Format(), event.RecordNumber, event.SourceName))
                notify_user(event.SourceName,event.StringInserts[0])
            cursorlog+=len(readlog)    

def notify_user(source,info):
      notification.notify(
                #title of the notification,
                title = "%s {}".format(datetime.date.today())%source,
                #the body of the notification
                message = info,  
                #creating icon for the notification
                #we need to download a icon of ico file format
                app_name = "boop",
                app_icon = "Hall_Blue33x16.ico",
                # the notification stays for 50sec
                timeout  = 5
      )
def icon_function():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("hallrfid.ico"), w)
    tray_icon.show()
    #tray_icon.showMessage('VFX Pipeline', 'Hello "Name of logged in ID')
    #alternative_Listening(tray_icon)
    sys.exit(app.exec_())

def main():
    Thread(target = icon_function).start()
    Thread(target = alternative_Listening).start()

if __name__ == '__main__':
    main()