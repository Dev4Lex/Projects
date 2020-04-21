#!/usr/bin/env python

import scapy.all as scapy #импорт модуля и всех функций; вызов как scapy
import argparse

def get_arguments(): #функция получения аргументов
    parser = argparse.ArgumentParser() #экземпляр класса для чтения входных параметров
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.") #добавление опции 't',
    # 'target', храним значение в 'target', справка 'Target IP / IP range.'
    options = parser.parse_args() #возвращает переменную 'target' в 'options'
    return options #функция get_arguments возвращает значение options

def scan(ip): #функция сканирования; передается ip-адрес
    arp_request = scapy.ARP(pdst = ip) #созадем экземпляр ARP запроса; подставляем ip в pdst
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") #создаем Ethernet фрэйм; широковещательный адрес в dst
    arp_request_broadcast = broadcast/arp_request #создаем переменную, содержащую broadcast и arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #отправка пакета
    # arp_request_broadcast; возвращает 1 набор значений: отвеченные; ждет ответа 1с


    clients_list = [] #создаем пустой список
    for element in answered_list: #перебор набора значений answered_list
        client_dict = {"ip": element[1].psrc, 'mac': element[1].hwsrc} #создаем словарь, где psrc->ip, hwsrc->mac
        clients_list.append(client_dict) #добавляем словарь client_dict  в список clients_list
    return clients_list #возвращается словарь со всеми элементами из answered_list

def print_result(results_list): #функция вывода результата
    print("IP\t\t\tMAC Address\n-----------------------------------") #отрисовка шапки таблицы
    for client in results_list: #перебор набора значений results_list
        print(client["ip"] + "\t\t" + client["mac"]) #вывод ip и mac адресов

options = get_arguments() #вызов функции получения аргумента
scan_result = scan(options.target) #вызов функции сканирования с полученным от пользователя ip
print_result(scan_result) #вызов функции вывода результата с входными clienst_list
