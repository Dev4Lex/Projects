#! /usr/bin/env python

import subprocess #импорт модуля subprocess - запуск процессов из Python
import optparse #импорт модуля optparse - парсер параметров командной строки
import re #импорт модуля re - операции с регулярными выражениями


def get_arguments(): #функция получения аргументов
    parser = optparse.OptionParser() #экземпляр класса для чтения входных параметров
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") #добавление
    # опции 'i, 'interface', храним значение в 'interface', справка 'Interface to change its MAC address'
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address") #добавление опции 'm', 'mac',
    # храним значение в 'new_mac', справка 'New MAC address'
    (options, arguments) = parser.parse_args() #возвращает переменные 'interface' и 'new_mac' в 'options';
    # '--interface' и '--mac' в 'arguments'
    if not options.interface: #указал ли пользователь interface, options.interface - доступ к значению 'interface'
        parser.error("[-] Please specify an interface, use --help for more info.") #обработка пользовательской ошибки
        # + информационне сообщение
    elif not options.new_mac: #указзал ли пользователь new_mac, options.new_mac - доступ к значению 'interface'
        parser.error("[-] Please specify an new mac, use --help for more info.") ##обработка пользовательской ошибки
        # + информационне сообщение
    return options #фнукция get_arguments возвращает значение options


def change_mac(interface, new_mac): #функция замены MAC-адреса с 'interface' и 'new_mac' на входе
    print("[+] Changing MAC address for " + interface + " to " + new_mac) #вывод уведомления о смене MAC-адреса
    subprocess.call(["ifconfig", interface, "down"])  #отключение интерфейса 'interface'
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac]) #замена MAC адреса на 'new mac'
    subprocess.call(["ifconfig", interface, "up"]) #включение интерфейса 'interface'


def get_current_mac(interface): #фукнция получения текущего MAC-адреса
    ifconfig_result = subprocess.check_output(["ifconfig", interface]) #получение вывода команды 'ifconfig'
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result) #получение MAC-адреса с
    # помощью регулярного выражения

    if mac_address_search_result:
        return mac_address_search_result.group(0) #возвращает первую найденную группу
    else:
        print("[-] Could not read MAC address.")  #если групп нет -> вывод уведомления


options = get_arguments() #get_arguments возвращает 'interface' и 'new_mac' и записывает в options
current_mac = get_current_mac(options.interface) #присвоение текущего MAC-адреса переменной current_mac
print("Current MAC = " + str(current_mac)) #вывод сообщения о текущем MAC-адресе (включая None)

change_mac(options.interface, options.new_mac) #вызов функции change_mac c переменными на входе

current_mac = get_current_mac(options.interface) #присвоение текущего MAC-адреса переменной current_mac
if current_mac == options.new_mac: #проверка изменения MAC-адреса на новый
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
