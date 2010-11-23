#!/usr/bin/python
# -*- coding: utf-8 -*-
#logger.py
#      
#Copyright 2010 Vasudev Kamath <kamathvasudev@gmail.com>
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


import logging
from logging.handlers import TimedRotatingFileHandler


__all__ = ['get_logger']

BACKUPS = 10

LOG_LEVELS = {
    "info" : logging.INFO,
    "debug" : logging.DEBUG,
    "error" : logging.ERROR,
    "warning" : logging.WARNING,
    "critical" : logging.CRITICAL
    }

def get_logger(logger_name,log_file,log_level="debug"):
    global conf_values
    log = logging.getLogger(logger_name + ":")
    log.setLevel(LOG_LEVELS.get(log_level
                                ,logging.DEBUG))
    handler = None
    format_string = None
    
    handler = TimedRotatingFileHandler(log_file,"midnight",BACKUPS)
    format_string = '''%(asctime)s %(name)s %(levelname)s %(message)s'''


    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

