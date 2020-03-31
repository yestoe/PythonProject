from netmiko import ConnectHandler
import readline
import os
import getpass
import socket

clear = lambda: os.system('clear')

print("1. Cisco-IOS")
print("2. Cisco-NXOS")
print("3. JUN_OS")

while True:
    choose_dt = input("Choose device Type: ")
    if choose_dt == "1":
        device_dt = "cisco_ios"
        break
    if choose_dt == "2":
        device_dt = "cisco_nxos"
        break
    if choose_dt == "3":
        device_dt = "juniper"
        break
    else:
        print("Wrong argument, try again")

print(device_dt)
host = input("Enter hostname or ip addres: ")
login = input("Enter login: ")
passwd = getpass.getpass("Enter Password: ")

ip_host = socket.gethostbyname(host)

# print(ip_host)

device = {
    "device_type": device_dt,
    "ip": ip_host,
    "username": login,
    "password": passwd
}

net_connect = ConnectHandler(**device)
net_connect.enable()
clear()


def show_route_cisco():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route: ")
    ip_route = socket.gethostbyname(route)
    output_show_route = net_connect.send_command("show ip route " + ip_route)
    print("show ip route " + ip_route)
    print(output_show_route)


def show_route_junos():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route: ")
    ip_route = socket.gethostbyname(route)
    output_show_route = net_connect.send_command("show route " + ip_route)
    print(output_show_route)


def add_route_cisco():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route or prefix(no mask): ")
    mask = input("Enter mask(x.x.x.x): ")
    gateway = input("Enter gateway(FQDN or ip_addres): ")
    ip_gateway = socket.gethostbyname(gateway)
    print("ip route " + route + " " + mask + " " + ip_gateway + " " + "name " + gateway)
    net_connect.send_config_set("ip route " + route + " " + mask + " " + ip_gateway + " " + "name " + gateway)
    output_add_route = net_connect.send_command("show ip route " + route)
    print(output_add_route)


def add_route_junos():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route or prefix(x.x.x.x/x): ")
    gateway = input("Enter gateway(FQDN or ip_addres): ")
    ip_gateway = socket.gethostbyname(gateway)
    print("set routing-options static route " + route + " " + "next-hop" + " " + ip_gateway + " ")
    output_add_route = net_connect.send_config_set("set routing-options static route " + route + " " + "next-hop" + " " + ip_gateway + " ")
    print(output_add_route)

def remove_route_cisco():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route or prefix(no mask): ")
    mask = input("Enter mask(x.x.x.x): ")
    gateway = input("Enter gateway(FQDN or ip_addres): ")
    ip_gateway = socket.gethostbyname(gateway)
    if not gateway:
        ip_gateway = ""
    print("no ip route " + route + " " + mask + " " + ip_gateway)
    net_connect.send_config_set("no ip route " + route + " " + mask + " " + ip_gateway)
    output_delete_route = net_connect.send_command("show ip route " + route)
    print(output_delete_route)

def remove_route_junos():
    print("You are login in: " + host)
    print("Press 'Crtl+c' to exit")
    route = input("Enter route or prefix(x.x.x.x/x): ")
    gateway = input("Enter gateway(FQDN or ip_addres): ")
    ip_gateway = socket.gethostbyname(gateway)
    print("delete routing-options static route " + route + " " + "next-hop" + " " + ip_gateway + " ")
    output_delete_route = net_connect.send_config_set("delete routing-options static route " + route + " " + "next-hop" + " " + ip_gateway + " ")
    print(output_delete_route)


def show_running_config_cisco():
    print("You are login in: " + host)
    include = input("Include statement: ")
    output = net_connect.send_command("show running-config | include " + include)
    if not include:
        output = net_connect.send_command("show running-config")
    print(output)


def write_memory():
    while True:
        if choose_dt == "1":
            print("You are login in: " + host)
            choose_write = input("Are youe sure ?(y,n): ")
            if choose_write == "y":
                output = net_connect.send_command("write memory")
                print(output)
                break
            if choose_write == "n":
                print("Do nothing")
                break
            else:
                print("Wrong argument, try again")
        if choose_dt == "2":
            print("You are login in: " + host)
            choose_write = input("Are youe sure ?(y,n): ")
            if choose_write == "y":
                output = net_connect.send_command("commit")
                print(output)
                break
            if choose_write == "n":
                print("Do nothing")
                break
            else:
                print("Wrong argument, try again")
        if choose_dt == "3":
            print("You are login in: " + host)
            print("Bulding compare...")
            output_compare = net_connect.send_config_set("show | compare")
            output_commit_check = net_connect.send_config_set("commit check")
            print(output_compare)
            print(output_commit_check)
            choose_commit = input("commit ?(y/n): ")
            while True:
                if choose_commit == "y":
                    output_commit = net_connect.send_config_set("commit")
                    print(output_commit)
                    break
                if choose_commit == "n":
                    print("Do nothing")
                    break
                else:
                    print("Wrong argument, try again")
                if choose_commit == "n":
                    print("Do nothing")
                    break
                else:
                    print("Wrong argument, try again")
            if choose_commit == "n":
                break
            if choose_commit == "y":
                break


try:
    while True:
        print("You are login in: " + host)
        print("1. show route")
        print("2. add route")
        print("3. delete route")
        print("9. show running-config")
        print("10. write-memory")
        print("Press 'Crtl+c' to exit")
        choose = input("Choose options: ")
        choose_dt_int = int(choose_dt)
        if choose == "1":
            clear()
            while True:
                if choose_dt_int == 1:
                    try:
                        while True:
                            show_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 2:
                    try:
                        while True:
                            show_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 3:
                    try:
                        while True:
                            show_route_junos()
                    except KeyboardInterrupt:
                        print()
                        break
        if choose == "2":
            clear()
            while True:
                if choose_dt_int == 1:
                    try:
                        while True:
                            add_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 2:
                    try:
                        while True:
                            add_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 3:
                    try:
                        while True:
                            add_route_junos()
                    except KeyboardInterrupt:
                        print()
                        break
        if choose == "3":
            clear()
            while True:
                if choose_dt_int == 1:
                    try:
                        while True:
                            remove_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 2:
                    try:
                        while True:
                            remove_route_cisco()
                    except KeyboardInterrupt:
                        print()
                        break
                if choose_dt_int == 3:
                    try:
                        while True:
                            remove_route_junos()
                    except KeyboardInterrupt:
                        print()
                        break
        if choose == "9":
            clear()
            while True:
                try:
                    show_running_config_cisco()
                except KeyboardInterrupt:
                    print()
                    break
        if choose == "10":
            clear()
            write_memory()
        else:
            print("Wrong argument, try again")
except KeyboardInterrupt:
    print()
    exit()