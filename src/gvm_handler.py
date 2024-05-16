"""
Script responsible for handling connection with GVM using GMP protocol, additionaly responsible for:
- scanning targets
- generating reports
- sending pdf reports to user's email
"""

from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from base64 import b64decode
from pathlib import Path
from logger import Logger
from logger import Logger_levels as lvl
import subprocess
import defusedxml.ElementTree as ET
import os
import sys
import smtp_handler
import time

login = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
ip_to_scan = os.environ.get("IP")
sender_password = os.environ.get("SENDER_PASS")
email = os.environ.get("EMAIL")
port = 9390
hostname="localhost"
log_obj = Logger("/opt/log/app.log", True)


def main():
    connection = try_to_connect()
    log_obj.log(f"Connecting to GVM at: {hostname}:{port}",lvl.INFO)
    with Gmp(connection=connection) as gmp:
        if (authenticate(gmp) != True):
            sys.exit(1)
        scanner = get_scanner(gmp)
        scan_config = get_scan_config(gmp)
        port_list = get_port_list(gmp)
        ips = get_ips()
        log_obj.log(ips,lvl.DEBUG)
        target = create_target(gmp, ips, port_list)
        task = create_task(gmp, scan_config, target, scanner)
        report_id = start_task(gmp, task)
        while True:
            task_status=get_task_status(gmp, task)
            if task_status == "Done":
                path_to_report = prepare_report(gmp, report_id)
                log_obj.log("Report prepared",lvl.INFO)
                smtp_handler.send_email(sender_password, path_to_report,email)
                log_obj.log("Report sent.",lvl.SUCCESS)
                break
            time.sleep(10)

def try_to_connect():
    connection = TLSConnection(hostname=hostname,port=port)
    log_obj.log("Established",lvl.DEBUG)
    return connection

def authenticate(gmp):
    response = xml(gmp.authenticate(login, password))
    if response.get('status') != '200':
        log_obj.log("Authentication failed",lvl.ERROR)
        return False
    log_obj.log("Authenticated to GVM",lvl.INFO)
    return True


def start_task(gmp: Gmp, task):
    response = xml(gmp.start_task(task))
    if response.get('status') == '202':
        report_id = response.find('report_id').text
        log_obj.log(f"Task started. Report id for task: {report_id}",lvl.INFO)
        return report_id
    log_obj.log(f"Failed to start task. Response status: {response.get('status')}",lvl.ERROR)
    sys.exit(1)


def create_target(gmp: Gmp, ips, port_list):
    response = xml(gmp.create_target('target', hosts=ips, port_list_id=port_list))
    if response.get('status') == '201':
        log_obj.log("Target created",lvl.INFO)
        return response.get('id')
    log_obj.log(f"Failed to create target. Response status: {response.get('status')}",lvl.ERROR)


def get_scanner(gmp: Gmp):
    for scanner in xml(gmp.get_scanners()).findall('scanner'):
        if scanner.find('name').text == 'OpenVAS Default':
            scanner_id = scanner.get('id')
            log_obj.log(f"Found OpenVAS Default Scanner. Scanner_id: {scanner_id}",lvl.INFO)
            return scanner_id
    log_obj.log("Failed to find OpenVAS Default scanner.",lvl.ERROR)
    sys.exit(1)


def get_scan_config(gmp: Gmp):
    for config in xml(gmp.get_scan_configs()).findall('config'):
        if config.find('name').text == 'Full and fast':
            log_obj.log("Found scan config.",lvl.INFO)
            return config.get('id')
    log_obj.log("Failed to find scan config.",lvl.ERROR)
    sys.exit(1)


def create_task(gmp: Gmp, scan_config, target, scanner):
    response = xml(gmp.create_task('task', scan_config, target, scanner))
    if response.get('status') == '201':
        task_id = response.get('id')
        log_obj.log(f"Task created. Task id: {task_id}",lvl.INFO)
        return task_id
    log_obj.log(f"Failed to create task.",lvl.ERROR)
    sys.exit(1)


def get_port_list(gmp):
    tree = xml(gmp.get_port_lists())
    for lst in tree.findall('port_list'):
        if lst.find('name').text == 'All IANA assigned TCP':
            log_obj.log("Found IANA TCP Port list",lvl.INFO)
            return lst.get('id')
    log_obj.log("Failed to found port list.", lvl.ERROR)
    sys.exit(1)


def xml(a):
    return ET.fromstring(a)


def get_ips():
    nmap = subprocess.run(['nmap',  '-n', '-sn', ip_to_scan, '-oG', '-'], stdout=subprocess.PIPE)
    result = subprocess.check_output(['awk' ,'/Up$/{print $2}'], input=nmap.stdout)
    return [str(x)[2:-1] for x in result.splitlines()]


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
    for task in task_tree.findall("task"):
        if task is not None:
            task_status=task.find('status').text
    if (task_status == ""):
        log_obj.log("Failed to determine task status.",lvl.ERROR)
        return 1
    log_obj.log(f"Task status:{task_status}",lvl.DEBUG)
    return task_status


if __name__ == '__main__':
    time.sleep(60*8)
    main()
