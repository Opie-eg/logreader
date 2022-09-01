from plyer import notification #for getting notification on your PC
def notify_user(source,info):
    if source == "Prototipo_PortalRFID":
        source= "Hall RFID - Portal"
    notification.notify(
                #title of the notification,
                title = "%s"%source,
                #the body of the notification
                message = info,  
                #creating icon for the notification
                #we need to download a icon of ico file format
                app_name = "boop",
                app_icon = "Hall_Blue33x16.ico",
                # the notification stays for 50sec
                timeout  = 5
      )