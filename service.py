import wmi


#c = wmi.WMI()
def connect_computer_services(computername,netdomain,utilizador,password):
    username = netdomain + "\\" + utilizador
    c = wmi.WMI(computername, user = username, password = password)
#c = wmi.WMI("MachineB", user=r"GUIA\fred", password ="secret")



def check_running_services(computer):
    stopped_services = computer.Win32_Service (State="Stopped")
    if stopped_services:
        for s in stopped_services:
            if s.Name == "Prototipo_ServicoPortalRFID":
                print(s.Caption, "service is not running")

    else:
        print("No Services stopped")

def start_service(computer):
    computer.Win32_Service(Name='Prototipo_ServicoPortalRFID')[0].StartService()
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