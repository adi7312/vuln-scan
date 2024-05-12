"""
Script responsible for handling connection with GVM using GMP protocol, additionaly responsible for:
- scanning targets
- generating reports
- sending pdf reports to user's email
"""

from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp, CredentialType
from scapy.all import get_if_addr, conf, Ether, ARP, srp
from base64 import b64decode
from pathlib import Path
import subprocess
import defusedxml.ElementTree as ET
import os
import smtp_handler
import time

login = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
ip_to_scan = os.environ.get("IP")
sender_password = os.environ.get("SENDER_PASS")


def main():
    connection = TLSConnection(hostname="localhost",port=9390)
    with Gmp(connection=connection) as gmp:
        print(gmp.get_version())
        authenticate(gmp)
        scanner = get_scanner(gmp)
        scan_config = get_scan_config(gmp)
        port_list = get_port_list(gmp)
        target = create_target(gmp, "192.168.1.190", port_list)
        task = create_task(gmp, scan_config, target, scanner)
        start_task(gmp, task)
        while True:
            task_status=get_task_status(task)
            if task_status == "Done":
                report_id = get_report_id(gmp, task)
                path_to_report = prepare_report(gmp, report_id)
                smtp_handler.send_email(sender_password, path_to_report)
                exit(0)
            time.sleep(10)


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
        if lst.find('name').text == 'All IANA assigned TCP':
            return lst.get('id')
    print('Port list not found')
    exit(1)


def xml(a):
    return ET.fromstring(a)


def get_ips():
    nmap = subprocess.run(['nmap',  '-n', '-sn', ip_to_scan, '-oG', '-'], stdout=subprocess.PIPE)
    result = subprocess.check_output(['awk' ,'/Up$/{print $2}'], input=nmap.stdout)
    return [str(x)[2:-1] for x in result.splitlines()]

# TODO: Function(s) for retrieving PDF reports
def get_report_id(gmp: Gmp, task_id:str) -> str:
    task_tree = xml((gmp.get_task(task_id)))
    report_id=""
    for task in task_tree.findall("task"):
        current_report = task.find("current_report")
        if (current_report is not None):
            report = current_report.find("report")
            if (report is not None):
                report_id = report.attrib["id"]
    print(f"Report ID: {report_id}")
    return report_id



# TODO: Function for sending report when it is ready
def prepare_report(gmp: Gmp, report_id: str) -> str:
    report = gmp.get_report(report_id, report_format_id='c402cc3e-b531-11e1-9163-406186ea4fc5') # PDF format
    report_tree = xml(report)
    element = report_tree.find("report")
    content=element.find("report_format").tail
    binary_base64_encoded_pdf = content.encode('ascii')
    binary_pdf = b64decode(binary_base64_encoded_pdf)
    timestamp = int(time.time())
    path = f"/opt/reports/report_{timestamp}.pdf"
    pdf_path = Path(path).expanduser()
    pdf_path.write_bytes(binary_pdf)
    return path


def get_task_status(gmp: Gmp, task_id:str) -> str:
    task_tree = xml(gmp.get_task(task_id))
    task_status = ""
    for task in task_tree:
        task_status=task.find('status').text
    print(f"Task status: {task_status}")
    return task_status




if __name__ == '__main__':
    main()
