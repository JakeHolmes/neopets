import subprocess
import sys
import time
import urllib

def ChangeIP():
    """ Get a new IP address """

    print "    Changing IP"
    page = urllib.urlopen("http://mxtoolbox.com/WhatIsMyIP/")
    html = page.read()
    pos1 = html.find('ipAddress": ') + 13
    pos2 = html.find("'", pos1)
    old_ip = html[pos1:pos2]

    try:
        args = '"C:\Program Files (x86)\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -changeip'
        subprocess.Popen(args)
    except WindowsError:
        args = '"C:\Program Files\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -changeip'
        subprocess.Popen(args)

    time.sleep(45)

    try:
        page = urllib.urlopen("http://mxtoolbox.com/WhatIsMyIP/")
    except:
        DisconnectVPN()
        if ConnectToVPN():
            return True

    html = page.read()
    pos1 = html.find('ipAddress": ') + 13
    pos2 = html.find("'", pos1)
    new_ip = html[pos1:pos2]

    # TODO: Get Mom's IP to add in here
    if new_ip in (old_ip, '24.157.121.247', ''):
        print "    ERROR: Failed to change IP address - aborting program"
        sys.exit()

    print "    IP Successfully Changed"
    print "    " + new_ip
    return True


def ConnectToVPN():
    """ Connect to the VPN (only use this if there is not an existing connection) """

    print "    Connecting to VPN"
    page = urllib.urlopen("http://mxtoolbox.com/WhatIsMyIP/")
    html = page.read()
    pos1 = html.find('ipAddress": ') + 13
    pos2 = html.find("'", pos1)
    old_ip = html[pos1:pos2]

    try:
        args = '"C:\Program Files (x86)\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -connect'
        subprocess.Popen(args)
    except WindowsError:
        args = '"C:\Program Files\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -connect'
        subprocess.Popen(args)

    try:
        page = urllib.urlopen("http://mxtoolbox.com/WhatIsMyIP/")
    except:
        print "    ERROR: Failed to change IP address - aborting program"
        sys.exit()

    html = page.read()
    pos1 = html.find('ipAddress": ') + 13
    pos2 = html.find("'", pos1)
    new_ip = html[pos1:pos2]

    # TODO: Get Mom's IP to add in here
    if new_ip in (old_ip, '24.157.121.247', ''):
        print "    ERROR: Failed to connect to VPN - aborting program"
        sys.exit()

    print "    IP Successfully Changed"
    print "    " + new_ip


def DisconnectVPN():
    """ Disconnect from the VPN """

    try:
        args = '"C:\Program Files (x86)\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -disconnect'
        subprocess.Popen(args)
    except WindowsError:
        args = '"C:\Program Files\HMA! Pro VPN\\bin\HMA! Pro VPN.exe" -disconnect'
        subprocess.Popen(args)

    time.sleep(10)
    return True
