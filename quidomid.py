#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# Name:        quidomid.py
# Purpose:     Daemon that queries my home network equipment to build a list 
#              of connected equipment.
# 
# Author:      Luispa
#
# Created:     2022-11-27
# Licence:     MIT
#-----------------------------------------------------------------------------

# Preparar el entorno Python
# 
# MacOS ---
# Recomiendo instalar Python usando Homebrew. 
#   Referencia sobre cómo hacerlo
#   https://www.luispa.com/desarrollo/2021/04/30/python-jupyter.html
# 
# Linux ---
#
# Windows ---
#


# Librerías
#
import sys
from time import sleep
#import os
#import time
#import argparse
import logging

# Librerías adicionales
# PySNMP - https://snmplabs.thola.io/pysnmp/download.html
#   https://snmplabs.thola.io/pysnmp/contents.html
# Puresnmp - 
pip install puresnmp
# Fuente: https://github.com/eozer/awesome-snmp

# > pipenv install daemon
# 
#import daemon
#from daemon import pidfile

try:
    import netsnmp

except ImportError:
    logging.error("El módulo 'netsnmp' no existe! Instálalo antes anda :-)")
    sys.exit()

print("Hello, World!")
def get_netgear_mac_table(hostname):
    """Returns [(port, mac_addr), ...]."""
    macs = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.1',
                            Version = 2,
                            Community = netgear_community,
                            DestHost = hostname)
    ports = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.2',
                             Version = 2,
                             Community = netgear_community,
                             DestHost = hostname)
    return zip(map(int, ports), map(format_mac, macs))


i = 1
while( True ):
    print(f'Iteración: {i}')

    sleep(0.3)
    i = i + 1


sys.exit()


# SuperFastPython.com
# example of daemon processes being terminated abruptly
from multiprocessing import current_process
from multiprocessing import Process
 
# function to be executed in a new process
def task():
    print("Hola mundo !!")
    # get the current process
    process = current_process()
    # report if daemon process
    print(f'Daemon process: {process.daemon}')
    # loop for a while
    for i in range(1000):
        print(i, flush=True)
        # block for a moment
        sleep(0.1)
 
# entry point
if __name__ == '__main__':
    # create a new daemon process
    process = Process(target=task, daemon=True)
    # start the new process
    process.start()
    # block for a moment to let the daemon process run
    sleep(3)
    # prepare the user
    print('Main process exiting...')



debug_p = False

def do_something(logf):
    ### This does the "work" of the daemon

    logger = logging.getLogger('eg_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf)
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    while True:
        logger.debug("this is a DEBUG message")
        logger.info("this is an INFO message")
        logger.error("this is an ERROR message")
        time.sleep(5)


def start_daemon(pidf, logf):
    ### This launches the daemon in its context

    global debug_p

    if debug_p:
        print("eg_daemon: entered run()")
        print("eg_daemon: pidf = {}    logf = {}".format(pidf, logf))
        print("eg_daemon: about to start daemonization")

    ### XXX pidfile is a context
    with daemon.DaemonContext(
        working_directory='/var/lib/eg_daemon',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        ) as context:
        do_something(logf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--pid-file', default='/var/run/eg_daemon.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/eg_daemon.log')

    args = parser.parse_args()
    
    start_daemon(pidf=args.pid_file, logf=args.log_file)
