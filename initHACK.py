#!/usr/bin/python3
#-------Author-------------
#W1nz4c4r
#--------------------------
import sys
import subprocess
import re
from art import text2art, FONT_NAMES
import signal
import ipaddress
from termcolor import colored




Begin_cmd = colored("[*] > ", "yellow", attrs=["bold"])
Alert_cmd = colored("[!] > ", "red", attrs=["bold"])
OS_cmd = colored('[Check OS] > ', "cyan", attrs=["bold"])
Direc_cmd = colored('[Create Dirs] > ', "magenta", attrs=["bold"])
Scan_cmd =colored('[Scanner] > ', "blue", attrs=["bold"])
Full_Scan_cmd =colored('[Scanner Full] > ', "blue", attrs=["bold"])

#handler for using Ctrl + C 
def signal_handler(sig, frame):
    print(colored("\n[-] Exiting program...Happy Hacking :)", "red", attrs=['reverse','bold']))
    # Perform any necessary cleanup here
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

#Displays the name of the tool
def Print_Name():
    ascii_art = text2art("Init-Hack", font='tarty1')
    print(ascii_art)
    print(colored('By: W1nz4c4r --> https://github.com/W1nz4c4r/initHACK  \n\n','magenta',  attrs=['bold']))

#will display the OS on the scan machine based on its ttl
def showInfo(value, ttl):
    if value == 1:
        print( OS_cmd + 'Machine type: ' + colored('LINUX','cyan', attrs=['underline']))
        print("\t" + colored('[+]','green', attrs=['bold']) + " Machine TTL --> {}".format(ttl))
    elif value == 2:
        print( OS_cmd + 'Machine type: ' + colored('WINDOWS','cyan', attrs=['underline']))
        print("\t" + colored('[+]','green', attrs=['bold']) + " Machine TTL --> {}".format(ttl))

#verify if the ip provided is valid or not
def is_Valid_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip == "0.0.0.0":
            raise ValueError("Invalid IP address: 0.0.0.0 is not allowed.")
        return True
    except ValueError as ve:
        #print(f"Invalid IP address: {ve}")
        return False


    
#This will Determine the OS of the machine IP provided
def Check_OS(machine_ip):
    #get machine IP
    #enter ip of the machine you wish to check
    machine_ip = input("\n" + OS_cmd +"Enter IP you wish to scan: ")
    if is_Valid_ip(machine_ip):
        #running the ping -c1 IP and checking the ttl to define the system
        process = subprocess.Popen(["ping -c1 {}".format(machine_ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, error = process.communicate()
        result = result.decode("utf-8")
        result = result.split()
        result = result[12].split('=')
        result = int(result[1])
        #checking the ttl
        if result >= 0 and result <= 64:
            #linux machine
            showInfo(1, result)
            return machine_ip
        elif result >= 65 and result <= 128:
            #Windows machine
            showInfo(2, result)
            return machine_ip
    else:
        print(colored("Please enter a valid IP address!", "red", attrs=["bold"]))
        Check_OS()

#this will create the working directories I use on a pentest
# Directories created: nmap, content and Exploits 
def Create_Direcotires():
    #check if more directories are wanted
    print(Direc_cmd + 'Do you want to create more directories? (Default: nmap, content & exploits)')
    extra_dic = input(Direc_cmd + 'Press enter to continue or write the names of the extra directories \t(Use comma (,) for multile directories)\n')
    print(Direc_cmd + colored('Creating working directories...'))
    #creating extra directories if user wants
    if  extra_dic.strip():
            extra_list_dic= extra_dic.split(',')
            for i in range(len(extra_list_dic)):
                #if the input is empty do not create folder
                if not extra_list_dic[i].strip():
                    #print('This is empty!')
                    #print(extra_list_dic[i])
                    pass
                else:
                    #creating directories 
                    extra_command = "mkdir {} 2>/dev/null".format(extra_list_dic[i])
                    extra_Proc = subprocess.run([extra_command], shell=True)
                    #print(extra_list_dic[i])
    #making nmap
    nmap_Proc = subprocess.run(["mkdir nmap 2>/dev/null"], shell=True)
    #making contect forlder
    cont_Proc = subprocess.run(["mkdir content 2>/dev/null"], shell=True)
    #making exploits forlder
    exp_Proc = subprocess.run(["mkdir exploits 2>/dev/null"], shell=True)
    print(Direc_cmd + "Creating folders -> " + colored("DONE",'green'))

# This will start the scan only looking open ports
#if ip_Bool is False --> then no IP has been provided
#if ip_Bool is True --> IP has been provided 
def Scan_Open_Ports(machine_ip):
    #print('Valid ' + machine_ip)  
    
    scan_command = "sudo nmap -p- --open -sS -vvv -n -Pn  {} -oN nmap/OP_ports".format(machine_ip)
    print(Scan_cmd + scan_command)
    try:
        #start the scan for possible open ports
        #subprocess.run(scan_command,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) --> USER THIS TO NOT SHOW OUTPUT FROM THE SCAN
        subprocess.run(scan_command,shell=True)
        print(Scan_cmd + 'Scan for open ports...' + colored('DONE','green',attrs=['underline']))
        #print()
    except Exception as e:
        print(e)


#this will create the full Nmap command to perform a deep scan on specified ports
def Full_scan(machine_ip):
    #full scan command

    # Run the Bash pipeline in Python using subprocess.Popen
    #after running all this commands the script will get the open ports from the file located in  ./nmap/OP_ports
    cat = subprocess.Popen(['cat', 'nmap/OP_ports'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', 'open'], stdin=cat.stdout, stdout=subprocess.PIPE)
    awk1 = subprocess.Popen(['awk', '{ print $1 }'], stdin=grep.stdout, stdout=subprocess.PIPE)
    awk2 = subprocess.Popen(['awk', '{print ($0+0)}'], stdin=awk1.stdout, stdout=subprocess.PIPE)
    sed = subprocess.Popen(['sed', '-z', 's/\\n/,/g;s/,$/\\n/'], stdin=awk2.stdout, stdout=subprocess.PIPE)

    cat.stdout.close()
    grep.stdout.close()
    awk1.stdout.close()
    awk2.stdout.close()

    output, error = sed.communicate()
    if sed.returncode == 0:
        #ignore port 0 given and add everything to the nmap command
        open_ports = output.decode().strip().split(',')
        open_ports = open_ports[1:]
        ports_string = ','.join(str(x) for x in open_ports)
        print(Full_Scan_cmd, "Open ports found :", colored(ports_string, 'green', attrs=['bold']))
        Full_Scan_command = "sudo nmap -sS -sV -sC -p{} -Pn -n -vvv {} -oA nmap/allPorts ".format(ports_string,machine_ip)
        print(Full_Scan_cmd, Full_Scan_command)
        subprocess.run(Full_Scan_command,shell=True)
        print (Full_Scan_cmd + 'Full scan of target...' + colored('DONE','green',attrs=['underline']))


    else:
        print(Scan_cmd, "Error processing open ports:", error.decode().strip())
        print(Alert_cmd, 'Make sure you already scan for open ports (nmap/OP_ports)')


#display instructions
def show_help():
    print(colored("\nHelp Menu:\n", "yellow", attrs=["bold"]))  
    print(colored("1:", "yellow", attrs=["bold"]) + " Check machine OS")
    print(colored("2:", "yellow", attrs=["bold"]) + " Create working Directories")
    print(colored("3:", "yellow", attrs=["bold"]) + " Scan open ports on target")
    print(colored("4:", "yellow", attrs=["bold"]) + " Perform full scan on specified ports")
    print(colored("5:", "yellow", attrs=["bold"]) + " Exit program")
    print(colored("\nType 'help' to display this menu again.\n","green", attrs=["underline", 'bold']))

def main():
    show_help()
    machine_ip = '0.0.0.0'
    User_choice = input(Begin_cmd + "please select an option: ")
    while True:
        if User_choice == '1' : 
            # check machine OS
            machine_ip = Check_OS(machine_ip)
            User_choice = input(Begin_cmd)
        elif User_choice == '2':
            #Create working directories 
            Create_Direcotires()
            User_choice = input(Begin_cmd)
        elif User_choice == '3':
            # Scan machine for open targets
            while machine_ip == '0.0.0.0'or not is_Valid_ip(machine_ip):
                machine_ip = input(Scan_cmd + 'Please enter the IP: ').strip()
                if not is_Valid_ip(machine_ip) :
                    print(Alert_cmd , 'Please enter a valid IP!')
                    print(Alert_cmd , 'NOTE: 0.0.0.0 does not count as valid IP')
            Scan_Open_Ports(machine_ip)
            User_choice = input(Begin_cmd)
        elif User_choice == '4':
            #this will perform Full_scan

            while machine_ip == '0.0.0.0'or not is_Valid_ip(machine_ip):
                machine_ip = input(Full_Scan_cmd + 'Please enter the IP: ').strip()
                if not is_Valid_ip(machine_ip) :
                    print(Alert_cmd , 'Please enter a valid IP!')
                    print(Alert_cmd , 'NOTE: 0.0.0.0 does not count as valid IP')
            Full_scan(machine_ip)
            User_choice = input(Begin_cmd)

        elif User_choice == '5':
            #exit the program
            print(colored("\n[-] Exiting program...Happy Hacking :)", "red", attrs=['reverse','bold']))
            # Perform any necessary cleanup here
            sys.exit(0)
        elif User_choice.strip().lower() == 'help':
            show_help()
            User_choice = input(Begin_cmd)

        else:
            print(Alert_cmd + 'Please enter a valid input!\n'+ Alert_cmd + 'Note: type help to show all options')
            User_choice = input(Begin_cmd)


if __name__ == '__main__':
    Print_Name()
    main()