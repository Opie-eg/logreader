

#import Evtx.Evtx as evtx
from collections import OrderedDict
from lxml import etree
from lxml.etree import _Element as Element, _ElementTree as ElementTree
from infi.systray import SysTrayIcon
from winevt import EventLog
import os
from plyer import notification #for getting notification on your PC


def say_hello(systray):
    print("Hello, World!")

    hostname = "192.168.1.30" #example
    response = os.system("ping " + hostname)
    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')

def get_events(input_file, parse_xml=False):
    """Opens a Windows Event Log and returns XML information from
    the event record.

    Arguments:
        input_file (str): Path to evtx file to open
        parse_xml (bool): If True, return an lxml object, otherwise a string

    Yields:
        (generator): XML information in object or string format

    Examples:
        >>> for event_xml in enumerate(get_events("System.evtx")):
        >>>     print(event_xml)

    """
    with evtx.Evtx(input_file) as event_log:
        for record in event_log.records():
            if parse_xml:
                yield record.lxml()
            else:
                yield record.xml()

def open_evtx(input_file):
    """Opens a Windows Event Log and displays common log parameters.

    Arguments:
        input_file (str): Path to evtx file to open

    Examples:
        >>> open_evtx("System.evtx")
        File version (major): 3
        File version (minor): 1
        File is ditry: True
        File is full: False
        Next record number: 10549

    """
    ignored_notifications = ["Codigo a processar","Este codigo RFID não está autorizado a sair"]
    with evtx.Evtx(input_file) as open_log:
        header = open_log.get_file_header()
        properties = OrderedDict(
            [
                ("major_version", "File version (major)"),
                ("minor_version", "File version (minor)"),
                ("is_dirty", "File is dirty"),
                ("is_full", "File is full"),
                ("next_record_number", "Next record number"),
            ]
        )

        for key, value in properties.items():
            print(f"{value}: {getattr(header, key)()}")

    for event_xml in enumerate(get_events(input_file)):
        root = etree.fromstring(event_xml[1])
        
        provider = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Provider[@Name='Prototipo_PortalRFID']")
        if provider is not None:
            computer = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Computer")
            data = root.find(".//{http://schemas.microsoft.com/win/2004/08/events/event}Data")
            
            if not any(x in data.text for x in ignored_notifications):
                print(computer.text,data.text)

def eventReader(systray):
    query = EventLog.Query("Application","Event/System/Provider[@Name='Windows Error Reporting']")

    for event in query:
        for item in event.EventData.Data:
            if "dmp" in item.cdata:
                print(item.cdata)
    
def eventReader2(systray):
    query = EventLog.Query("Application")


    for event in query:
        if event.System.Provider['Name'] == "Prototipo_PortalRFID":
            print(event.System.Provider['Name'])



#open_evtx(r"C:\Users\Diogo\Desktop\projects\logreader\Eventos.evtx")


menu_options = (("Say Hello", None, say_hello),("test reader",None, eventReader),("test reader2",None, eventReader2))
systray = SysTrayIcon("hallrfid.ico", "Example tray icon", menu_options)
systray.start()