

#c = wmi.WMI()
def connect_computer_services(server,netdomain,utilizador,password):
    print("Starting Connection to server...")
    username = "%s\\%s" % (netdomain, utilizador)
    computer = wmi.WMI(server, user = username, password = password)
    #c = wmi.WMI("MachineB", user=r"GUIA\fred", password ="secret")
    print("...Success!")
    stopped_services = computer.Win32_Service (State="Stopped")
    if stopped_services:
        for s in stopped_services:
            if s.Name == "Prototipo_ServicoPortalRFID":
                print(s.Caption, "service is not running")
                computer.Win32_Service(Name = 'Prototipo_ServicoPortalRFID')[0].StartService()
                return False
        return True

    else:
        print("No Services stopped")



    
# Below will output all possible service names
#for service in c.Win32_Service():
    #print(service.Name)

"""
for service in c.Win32_Service(Name="seclogon"):
    result, = service.StopService()
    if result == 0:
        print( "Service", service.Name, "stopped")
    else:
        print( "Some problem", result)
    break
else:
    print("Service not found")

"""


#http://timgolden.me.uk/python/wmi/tutorial.html
