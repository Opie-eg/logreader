
import sys
import re
import pythoncom
import tkinter.messagebox
from PySide2 import QtWidgets, QtGui
from threading import Thread
import time
import win32evtlog # requires pywin32 pre-installed
import win32event
import win32con
import json
from notify import notify_user 
from score import updateUserScore
from tkinter import ttk
from ttkthemes import ThemedTk
import wmi
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import webbrowser
from lxml import etree
from lxml.etree import _Element as Element, _ElementTree as ElementTree
import os
from validate import encrypt_password,decrypt_password,verify

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
    process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr= subprocess.PIPE, shell=True)
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
    def __init__(self, icon, parent, serverlist, netdomain, userinput, passinput,license_name):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        license_name= "Licenciado para uso em: " + license_name
        self.server = serverlist
        self.netdomain = netdomain
        self.userinput= userinput
        self.passinput= passinput
        self.setToolTip(f'Hall RFID - Gestão de Portal')
        menu = QtWidgets.QMenu(parent)
        self.menu_title_icon= menu.addAction("Hall RFID - Gestão de Portal")
        self.menu_title_icon.setIcon(QtGui.QIcon("Hall_Blue-320x320.png"))
        self.licence_title_icon1 = menu.addAction(license_name)
        menu.addSeparator()
        
        menu.setToolTipsVisible(True)
        # Creating menu options based on ip"x" values in config.json each one of the menu options opens a page with the respective ip address.
        self.menudict = {}
        self.servicemenudict = {}
        iplist= []
        hostlist = []
        secondserverlist = []
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
        for server in serverlist:
            self.servicemenudict[server[0]]= menu.addAction("Serviço RFID - "+ server[1][1])
            self.servicemenudict[server[0]].triggered.connect(lambda ignored= serverlist, a= server[1][0],: Thread(target = self.start_service, args = (a,)).start())
            self.servicemenudict[server[0]].setIcon(QtGui.QIcon("readyblue.png"))
            self.servicemenudict[server[0]].setToolTip('Clicar para ligar o Serviço.')
            #secondserverlist.append(json_data[iplist[server]][0]) 

        '''
        self.service_option = menu.addAction("Serviço RFID")
        self.service_option.setIcon(QtGui.QIcon("readyblue.png"))
        self.service_option.triggered.connect(lambda : Thread(target = self.start_service).start())
        self.service_option.setToolTip('Clicar para ligar o Serviço.')
        #self.service_option.setToolTip('Serviço ativo')
        
        '''
       
          
        menu.addSeparator()

        exit_ = menu.addAction("Sair")
        exit_.triggered.connect(lambda: sys.exit())
        

        menu.addSeparator()
        self.setContextMenu(menu)
        #self.activated.connect(self.onTrayIconActivated)
        self.show()

    def connect_computer_services(self):
        with open("config.json") as f:
                json_data = json.load(f)
        username = "%s\\%s" % (self.netdomain, self.userinput)
        if "tempo_espera_servico_horas" in json_data:
            tempo_horas = json_data["tempo_espera_servico_horas"]
        else:
            tempo_horas = 12
        while True:
            for i in self.servicemenudict:
                
                pythoncom.CoInitialize()
                try:
                    print("Starting Connection to server...")
                    server= json_data[i][0]
                    computer = wmi.WMI(server, user = username, password = self.passinput)
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
                                self.servicemenudict[i].setIcon(QtGui.QIcon("notreadyred.png"))
                                self.setIcon(QtGui.QIcon("Hall_Red-320x320.png"))

                        if servicefound == False:
                            self.servicemenudict[i].setIcon(QtGui.QIcon("readygreen.png"))
                            self.setIcon(QtGui.QIcon("Hall_Blue-320x320.png"))
                except:
                    self.servicemenudict[i].setIcon(QtGui.QIcon("notreadyred.png"))
                    self.setIcon(QtGui.QIcon("Hall_Red-320x320.png"))

                finally:
                    pythoncom.CoUninitialize()
               
            time.sleep(60*60*tempo_horas)
                
    
    def start_service(self,server):
        pythoncom.CoInitialize()
        try:
            print("Starting Connection to server...")
            username = "%s\\%s" % (self.netdomain, self.userinput)
            computer = wmi.WMI(server, user = username, password = self.passinput)
            print("...Success!")
            computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
            
        finally:
            pythoncom.CoUninitialize()

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
        if "tempo_espera_ping_minutos" in json_data:
            tempo_min = json_data["tempo_espera_ping_minutos"]
        else:
            tempo_min = 15
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
                self.setIcon(QtGui.QIcon("Hall_Orange-320x320.png"))
            elif counter >= len(self.menudict):
                self.setIcon(QtGui.QIcon("Hall_Blue-320x320.png"))
            counter = 0 
            time.sleep(60*tempo_min)


#https://www.accadius.com/using-python-read-windows-event-logs-multiple-servers/
#https://www.blog.pythonlibrary.org/2010/07/27/pywin32-getting-windows-event-logs/

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))
    
def eventlog_Listening(userinput,passinput,ignored_notifications,score_notifications,server,netdomain):
    logtype = 'Application' # 'Application' # 'Security'
    if is_valid_ip(server) == True:
        sessionlogin = win32evtlog.EvtOpenSession((server,userinput,netdomain,passinput,win32evtlog.EvtRpcLoginAuthDefault), win32evtlog.EvtRpcLogin , 0 , 0 )     
    else:
        sessionlogin = None
    eventhandler = win32event.CreateEvent(None, 1, 0, "wait") #criar um evento como ponto de referencia
    sub_flags = win32evtlog.EvtSubscribeToFutureEvents
    subscription = win32evtlog.EvtSubscribe(logtype, sub_flags, SignalEvent= eventhandler, Callback= None, Context= None,
    Query= "*", Session= sessionlogin)
    read_event(subscription,ignored_notifications,score_notifications)
    while 1:
        try:
            w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
            if w==win32con.WAIT_OBJECT_0:
                read_event(subscription,ignored_notifications,score_notifications)
                #w=win32event.WaitForSingleObjectEx(eventhandler, 2000, True)
                time.sleep(2)
        except:
            pass
    #eventcreate /ID 1 /L APPLICATION /T INFORMATION /SO MYEVENTSOURCE /D "My first Log"

def read_event(subscription,ignored_notifications,score_notifications):
    events=win32evtlog.EvtNext(subscription, 10)
    #print(events)
    if len(events)==0:
        return
    else:
        for event in events:
            #print(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            root = etree.fromstring(win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml))
            provider = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Provider[@Name='Prototipo_PortalRFID']")
            info = []
            scoreboard =[]

            if provider is not None:
                computer = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Computer")
                data = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Data")
                if data is not None:
                    res = [ele for ele in ignored_notifications if(ele in data.text)]
                    if bool(res) == False:
                        if "reader não ligou" in data.text:
                            resposta = "O reader não ligou."
                        else:
                            resposta = data.text
                        scoreboard.append(data.text)
                        new_info= computer.text +";"+ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+";"+ resposta
                        info.append(new_info)
                        #print(new_info)
                        #new func here
                        notify_user(resposta)
            if len(info) > 0:
                record_log(info)
                for i in scoreboard:
                    if i in score_notifications[0]:
                        value = score_notifications[0].index(i)
                        notitype = score_notifications[1][value]
                        updateUserScore(1,computer.text,notitype)


def record_log(info):
    file_name = 'event_logs.log'
    stat_file = 'statistics.txt'
    if os.path.exists(file_name):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    f = open(file_name, append_write, encoding= "utf-8")  # open file in write mode
    for i in info:
        f.write(i + "\n")
    f.close()

    if os.path.exists(stat_file):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    f = open(file_name, "r", encoding= "utf-8")
    f2 = open(stat_file, append_write, encoding= "utf-8")
    for i in f:
        if i == "X":
            pass
        elif i== "Y":
            pass
    f.close
    f2.close

def icon_function(server,netdomain,userinput,passinput,license_name):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    
    tray_icon = SystemTrayIcon(QtGui.QIcon("Hall_Blue-320x320.png"), w , server,netdomain,userinput,passinput,license_name)
    Thread(target = tray_icon.cycle_ping).start()
    Thread(target = tray_icon.connect_computer_services).start()
    sys.exit(app.exec_())

from tkinter import *
from functools import partial

def validateLogin(username, password,tkWindow):
    user= username.get()
    passw= password.get()
    if len(user) != 0 and len(passw) != 0:
        tkWindow.destroy()

    return 

def main():
    with open("config.json") as f:
        json_data = json.load(f)

    if all(key in json_data for key in("licence_key","licence_name"))==False or (verify(json_data["licence_key"],json_data["licence_name"]) == False):
        tkinter.messagebox.showerror('HallRFID_GestorPortal Erro JSON', 'Chave de Licença em falha. \nVerifique se os campos "licence_key" e "licence_name" estão corretamente definidos no ficheiro config.json')
        return
    if "ignored_notifications" in json_data:
        ignored_notifications = json_data["ignored_notifications"]
    else:
        ignored_notifications = ["Codigo a processar","Lista do portal limpa",
"Tag adicionada","A tag que passou no portal","Usar web service?:",
"Tentativa de liga\u00E7\u00E3o 2","Tentativa de liga\u00E7\u00E3o 3","Tentativa de liga\u00E7\u00E3o 4"]

    score_verification= []
    score_translation= []
    if "score_notifications" in json_data:
        for i in range(0,len(json_data["score_notifications"])):
            score_verification.append(json_data["score_notifications"][i][0])
            score_translation.append(json_data["score_notifications"][i][1])
    else:
        score_notilist= [
            ["Falha no acesso \u00E0 base de dados do web service","FalhaBD"],
            ["Falha no acesso ao web service","FalhaWS"],["O leitor Impinj Ligou","LeitorL"],
            ["O leitor Impinj Desligou","LeitorD"],["Sentido 1_2","Sentido 1_2"],["Sentido 2_1","Sentido 2_1"],
            ["Este codigo RFID n\u00C3o est\u00E1 autorizado a sair","RFIDSair"],
            ["N\u00C3o foi poss\u00EDvel adicionar a passagem ao webservice","NoPassagemWS"],
            ["O servi\u00E7o parou","ServiceStop"]]
        for i in range(0,len(score_notilist)):
            score_verification.append(score_notilist[i][0])
            score_translation.append(score_notilist[i][1])

    score_notifications = [score_verification,score_translation]
    server_list = []
    for i in json_data:
        if "server" in i:
            server_list.append([i,json_data[i]])
    netdomain= json_data["network_domain"]# name of the network domain to connect to
    
    if all(key in json_data for key in("use_account","username","password")) and (json_data["use_account"] == "True" or json_data["use_account"] == "true"):
        userinput= json_data["username"]
        passinput= decrypt_password(json_data["password"])
    else:

        #window
        tkWindow = ThemedTk(theme="clearlooks")  
        width = 207 # Width 
        height = 75 # Height
        
        screen_width = tkWindow.winfo_screenwidth()  # Width of the screen
        screen_height = tkWindow.winfo_screenheight() # Height of the screen

        
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width) - (width)
        y = (screen_height) - (height*2)
        tkWindow.iconbitmap("ICONE_AZUL.ico")
        tkWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
        tkWindow.title('Login')

        login_frame = ttk.Frame(tkWindow, width=207, height=75)
        login_frame.pack(fill="both", expand=1)
        
        #username label and text entry box
        usernameLabel = ttk.Label(login_frame, text="Nome").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = ttk.Entry(login_frame, textvariable=username).grid(row=0, column=1)  

        #password label and password entry box
        passwordLabel = ttk.Label(login_frame,text="Palavra-Passe").grid(row=1, column=0)  
        password = StringVar()
        passwordEntry = ttk.Entry(login_frame, textvariable=password, show='*').grid(row=1, column=1)  

        bfunc = partial(validateLogin, username, password,tkWindow)

        #login button
        loginButton = ttk.Button(login_frame, text="Login", command=bfunc).grid(row=4, column=1)  
        
        tkWindow.mainloop()
        #print(bfunc)    
        userinput = username.get()
        passinput = password.get()
        
        #userinput = input("Nome De Utilizador: ")
        #passinput = getpass.getpass("Password: ")
    
    if len(userinput) != 0 and len(passinput) != 0:
        a = Thread(target = icon_function, args=(server_list,netdomain,userinput,passinput,json_data["licence_name"],))
        Listener_Threads = [Thread(target = eventlog_Listening , args=(userinput,passinput,ignored_notifications,score_notifications,i[1][0],netdomain,))
        for i in server_list]
        Listener_Threads.append(a)
        for thread in Listener_Threads:
            thread.start()
        
    else:
        return

if __name__ == '__main__':
    main()

