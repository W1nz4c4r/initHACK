#!/usr/bin/python3
#-------Author-------------
#W1nz4c4r
#--------------------------
import sys
import subprocess
import re

def showInfo(value, ttl):
    if value == 1:
        print("\t [+] Linux machine --> ttl {}".format(ttl))
    elif value == 2:
        print("\t [+] Windows machine --> ttl {}".format(ttl))



def whichSystem(IP):
     try:
         #running the ping -c1 IP and checking the ttl to define the system
         process = subprocess.Popen(["ping -c1 {}".format(IP)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
         result, error = process.communicate()
         result = result.decode("utf-8")
         result = result.split()
         result = result[12].split('=')
         result = int(result[1])
         #checking the ttl
         if result >= 0 and result <= 64:
             #Linux machine
             showInfo(1, result)
         elif result >= 65 and result <= 128:
             #Windows machine
             showInfo(2, result)
             
         else:
             print("Error Please check the IP")
             sys.exit(1)
     except:
         print("[-] Check your input!")
         sys.exit(1)

def create_Workspace(fullcommand):
    if fullcommand == False:
        print("[+] Creating folders...")
        #making dir's (Content, nmap and exploits)
        #making nmap
        nmap_Proc = subprocess.run(["mkdir nmap 2>/dev/null"], shell=True)
        #making contect forlder
        cont_Proc = subprocess.run(["mkdir content 2>/dev/null"], shell=True)
        #making exploits forlder
        exp_Proc = subprocess.run(["mkdir exploits 2>/dev/null"], shell=True)
        print("[+] Creating folders => DONE")
    elif fullcommand == True:
        print("[!] Skipping workspace...")

    

def ip_portScan(IP,fullcommand,ports):
    if fullcommand == False:
        print("\t[+] Quick Nmap command copied to the clipboard")
        command = "sudo nmap -p- --open -sS -vvv -n -Pn  {} -oN nmap/OP_ports".format(IP)
        subprocess.run("xclip -sel clip", universal_newlines=True, input=command, shell=True)
        print("\n\n[+] Command to extract ports: \n\t- cat nmap/OP_ports | grep 'open' | awk '{ print $1 }' | awk '{print ($0+0)}' | sed -z 's/\\n/,/g;s/,$/\\n/'")
    elif fullcommand == True:
        #Parses the specified file and extracts open ports as a comma-separated list.
        #Returns:
        #A string containing comma-separated open ports, or an empty string if no ports are found.
        print("\t[+] FULL Nmap command copied to the clipboard")        
        command = "sudo nmap -sS -sV -sC -p{} -Pn -n -vvv {} -oA nmap/allPorts ".format(ports,IP)
        subprocess.run("xclip -sel clip", universal_newlines=True, input=command, shell=True)

def main(IP, fullCommand=False, ports="insert port"):
    print("\n[+] Checking the IP : {}".format(IP))
    if fullCommand == False:
        whichSystem(IP)
    elif fullCommand == True:
        print('[!] Skipping system recon...')
    create_Workspace(fullCommand)
    ip_portScan(IP, fullCommand, ports)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        IP = sys.argv[1]
        main(IP)
    elif len(sys.argv) == 3 or len(sys.argv) == 4:
        IP = sys.argv[1]
        if sys.argv[2] == '-p':
            ports = sys.argv[3]
            #print(ports)
            # check if number
            num_ports = ports.split(',')
            for x in num_ports:
                if x.isdigit():
                    None
                else:
                    sys.exit(1)
            main(IP, True, ports)

            
    else:
        print("[!] Usage: python3 initHACK.py <IP>")
        print("\t- example: python3 initHACK.py 192.163.0.25 -p")
        print("\n[!] -p -->specify ports")
        sys.exit(1)
