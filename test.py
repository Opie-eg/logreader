import json

with open("config.json") as f:
    json_data = json.load(f)
    server_list = []
    for i in json_data:
        if "server" in i:
            server_list.append([i,json_data[i]])
    print(server_list)
    print(len(server_list))



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
                            self.setIcon(QtGui.QIcon("Hall_Red-320x320.png"))

                    if servicefound == False:
                        self.service_option.setIcon(QtGui.QIcon("readygreen.png"))
                        self.setIcon(QtGui.QIcon("Hall_Blue-320x320.png"))
            finally:
                pythoncom.CoUninitialize()
            if cycle == None:
                time.sleep(60*60*json_data["tempo_espera_servico_horas"])
            else:
                break