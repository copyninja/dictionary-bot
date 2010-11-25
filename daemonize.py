#!/usr/bin/python

# -*- coding: utf-8 -*-
#daemonize.py
#      
#Copyright 2010 Vasudev Kamath <kamathvasudev@gmail.com>
#
#Sanchaya Group <http://sanchaya.net>
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU  General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#     
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#      
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.
#


import os
import signal
import resource

__RUNNING_DIR__ = "/var"
__LOG_DIRECTORY__ = "log"

LOCK_FILE = "pydaemond.pid"
LOG_FILE = "pydaemond.log"
MAX_FD = 1024

def __signal_handler__(sig,frame):
    global LOCK_FILE
    if sig == signal.SIGHUP:
        return

    if sig == signal.SIGTERM:
        os.remove(os.path.join(__RUNNING_DIR__,"run",LOCK_FILE))
        os._exit(0)

def set_lockfile(lockfile):
    global LOCK_FILE
    LOCK_FILE = lockfile

def set_logfile(logfile):
    global LOG_FILE
    LOG_FILE = logfile

def get_daemon_log():
    return os.path.join(__RUNNING_DIR__,__LOG_DIRECTORY__,LOG_FILE)
        
def daemonizer():
    # Already Daemon Process?
    if(os.getppid() == 1):
        return
    
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception,"Exception occured %s [%d]"%(e.strerror,e.errno)
        os._exit(0)

    if pid == 0:
        # First child
        os.setsid()
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception,"Exception occured %s [%d]"%(e.strerror,e.errno)
            os._exit(0)
            
        if pid == 0:
            # Second child

            # Change the running directory
            os.chdir(__RUNNING_DIR__)
            # Now file creation permission will be 0777 & ~027 = 0750
            os.umask(027)
        else:
            # Parent of Second Child (First child) exits
            os._exit(0)
    else:

        os.wait()
        os._exit(0) # Parent of First Child exits
        
    # Second child continues as Daemon
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if maxfd == resource.RLIM_INFINITY:
        maxfd = MAX_FD
        
    # Close all open files (assuming they are open) 
    for fd in range(0,maxfd):
        try:
           os.close(fd)
        except OSError:
            # Not an error file isn't open :)
            pass
        
     # STDIN to /dev/null
    fd = os.open(os.devnull,os.O_RDWR)
    os.dup(fd) # STDOUT

    os.dup(fd) # STDERR
    lfp = os.open(os.path.join(__RUNNING_DIR__,"run",LOCK_FILE),os.O_RDWR|os.O_CREAT)
    os.write(lfp,str(os.getpid())+"\n")
    os.close(lfp)
    return 0
