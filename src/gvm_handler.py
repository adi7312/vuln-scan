"""
Script responsible for handling connection with GVM using GMP protocol, additionaly responsible for:
- scanning targets
- generating reports
- sending pdf reports to user's email
"""

from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp, CredentialType
from scapy.all import get_if_addr, conf, Ether, ARP, srp
import subprocess
import xml.etree.ElementTree as ET
import os
import smtp_handler

login = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
ip_to_scan = os.environ.get("IP")

def main():
    connection = TLSConnection(hostname="localhost",port=9390)
    with Gmp(connection=connection) as gmp:
        print(gmp.get_version())
        authenticate(gmp)
        scanner = get_scanner(gmp)
        scan_config = get_scan_config(gmp)
        port_list = get_port_list(gmp)
        target = create_target(gmp, ip, port_list)
        task = create_task(gmp, scan_config, target, scanner)
        start_task(gmp, task)


def authenticate(gmp):
    response = xml(gmp.authenticate(login, password))
    if response.get('status') != '200':
        print(response.get('status_text'))
        exit(1)


def start_task(gmp: Gmp, task):
    response = xml(gmp.start_task(task))
    if response.get('status') == '202':
        return response.find('report_id').text
    print('Failed to start task')
    exit(1)


def create_target(gmp: Gmp, ip, port_list):
    response = xml(gmp.create_target('target', hosts=[ip], port_list_id=port_list))
    if response.get('status') == '201':
        return response.get('id')
    print(response.get('status_text'))
    exit(1)


def create_credentails(gmp):
    response = xml(gmp.create_credential(name = 'credential', credential_type=CredentialType.USERNAME_PASSWORD, login=login, password=password))
    if response.get('status') != '201':
        print(response.get('status_text'))
        exit(1)
    return response.get('id')


def get_scanner(gmp: Gmp):
    for scanner in xml(gmp.get_scanners()).findall('scanner'):
        if scanner.find('name').text == 'OpenVAS Default':
            return scanner.get('id')
    print('Scanner not found')
    exit(1)


def get_scan_config(gmp: Gmp):
    for config in xml(gmp.get_scan_configs()).findall('config'):
        if config.find('name').text == 'Full and fast':
            return config.get('id')
    print('Scan config not found')
    exit(1)


def create_task(gmp: Gmp, scan_config, target, scanner):
    response = xml(gmp.create_task('task', scan_config, target, scanner))
    if response.get('status') == '201':
        return response.get('id')
    print(response.get('status_text'))
    exit(1)


def get_port_list(gmp):
    tree = xml(gmp.get_port_lists())
    for lst in tree.findall('port_list'):
        if lst.find('name').text == 'All IANA assigned TCP and UDP':
            return lst.get('id')
    print('Port list not found')
    exit(1)


def xml(a):
    return ET.fromstring(a)


def get_ips():
    nmap = subprocess.run(['nmap',  '-n', '-sn', ip_to_scan, '-oG', '-'], stdout=subprocess.PIPE)
    result = subprocess.check_output(['awk' ,'/Up$/{print $2}'], input=nmap.stdout)
    return [str(x)[2:-1] for x in result.splitlines()]

# TODO: Function for retrieving reports


if __name__ == '__main__':
    main()
