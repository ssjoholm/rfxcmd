#!/usr/bin/python
# coding=UTF-8

"""

    CONFIG.PY

    Copyright (C) 2012-2013 Sebastian Sjoholm, sebastian.sjoholm@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Website: http://www.rfxcmd.eu/

"""

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import sys
import string
import os

# ------------------------------------------------------------------------------
def read_config(configfile, configitem):
    """
    Read item from the configuration file

    :param configfile: The configuration file
    :type configfile: String
    :param configitem: The XML tag to read
    :type configitem: String
    :rtype: Returns the data for the specific XML tag
    :raises: Exception

    """
    logger.debug("Open configuration file")
    logger.debug("File: %s", configfile)

    if os.path.exists(configfile):
        try:
            f = open(configfile, 'r')
            data = f.read()
            f.close()
        except Exception as err:
            logger.error("Error: %s", str(err))
            raise

        # xml parse file data
        logger.debug("Parse config XML data")
        try:
            dom = minidom.parseString(data)
        except Exception as err:
            logger.error("Error: %s", str(err))
            logger.debug("Error in config.xml file")
            print "Error: problem in the config.xml file, cannot process it"
            raise

        # Get config item
        logger.debug("Get the configuration item: %s", configitem)

        try:
            xmlTag = dom.getElementsByTagName( configitem )[0].toxml()
            logger.debug("Found: %s", xmlTag)
            xmlData = xmlTag.replace('<' + configitem + '>','').replace('</' + configitem + '>','')
            logger.debug("--> %s", xmlData)
        except Exception as err:
            logger.error("Error: %s", str(err))
            logger.debug("The item tag not found in the config file")
            xmlData = ""

    else:
        logger.error("Error: Config file does not exists.")

    return xmlData

# ------------------------------------------------------------------------------
def read_configfile():
    """
    Read items from the configuration file
    """
    if os.path.exists( cmdarg.configfile ):

        # ----------------------
        # Serial device
        if (read_config(cmdarg.configfile, "serial_active") == "yes"):
            config.serial_active = True
        else:
            config.serial_active = False
        config.serial_device = read_config( cmdarg.configfile, "serial_device")
        config.serial_rate = read_config( cmdarg.configfile, "serial_rate")
        config.serial_timeout = read_config( cmdarg.configfile, "serial_timeout")

        logger.debug("Serial device: " + str(config.serial_device))
        logger.debug("Serial rate: " + str(config.serial_rate))
        logger.debug("Serial timeout: " + str(config.serial_timeout))

        # ----------------------
        # Process
        if (read_config(cmdarg.configfile, "process_rfxmsg") == "yes"):
            config.process_rfxmsg = True
        else:
            config.process_rfxmsg = False
        logger.debug("Process RFXmsg: " + str(config.process_rfxmsg))
        
        # ----------------------
        # MySQL
        if (read_config(cmdarg.configfile, "mysql_active") == "yes"):
            config.mysql_active = True
        else:
            config.mysql_active = False
        config.mysql_server = read_config( cmdarg.configfile, "mysql_server")
        config.mysql_database = read_config( cmdarg.configfile, "mysql_database")
        config.mysql_username = read_config( cmdarg.configfile, "mysql_username")
        config.mysql_password = read_config( cmdarg.configfile, "mysql_password")
    
        # ----------------------
        # TRIGGER
        if (read_config( cmdarg.configfile, "trigger_active") == "yes"):
            config.trigger_active = True
        else:
            config.trigger_active = False

        if (read_config( cmdarg.configfile, "trigger_onematch") == "yes"):
            config.trigger_onematch = True
        else:
            config.trigger_onematch = False

        config.trigger_file = read_config( cmdarg.configfile, "trigger_file")
        config.trigger_timeout = read_config( cmdarg.configfile, "trigger_timeout")

        # ----------------------
        # SQLITE
        if (read_config(cmdarg.configfile, "sqlite_active") == "yes"):
            config.sqlite_active = True
        else:
            config.sqlite_active = False        
        config.sqlite_database = read_config(cmdarg.configfile, "sqlite_database")
        config.sqlite_table = read_config(cmdarg.configfile, "sqlite_table")

        # ----------------------
        # PGSQL
        if (read_config(cmdarg.configfile, "pgsql_active") == "yes"):
            config.pgsql_active = True
        else:
            config.pgsql_active = False
        config.pgsql_server = read_config(cmdarg.configfile, "pgsql_server")
        config.pgsql_database = read_config(cmdarg.configfile, "pgsql_database")
        config.pgsql_port = read_config(cmdarg.configfile, "pgsql_port")
        config.pgsql_username = read_config(cmdarg.configfile, "pgsql_username")
        config.pgsql_password = read_config(cmdarg.configfile, "pgsql_password")
        config.pgsql_table = read_config(cmdarg.configfile, "pgsql_table")

        # ----------------------
        # GRAPHITE
        if (read_config(cmdarg.configfile, "graphite_active") == "yes"):
            config.graphite_active = True
        else:
            config.graphite_active = False
        config.graphite_server = read_config(cmdarg.configfile, "graphite_server")
        config.graphite_port = read_config(cmdarg.configfile, "graphite_port")

        # ----------------------
        # XPL
        if (read_config(cmdarg.configfile, "xpl_active") == "yes"):
            config.xpl_active = True
            config.xpl_host = read_config(cmdarg.configfile, "xpl_host")
            config.xpl_sourcename = read_config(cmdarg.configfile, "xpl_sourcename")
            if (read_config(cmdarg.configfile, "xpl_includehostname") == "yes"):
                config.xpl_includehostname = True
            else:
                config.xpl_includehostname = False
        else:
            config.xpl_active = False

        # ----------------------
        # SOCKET SERVER
        if (read_config(cmdarg.configfile, "socketserver") == "yes"):
            config.socketserver = True
        else:
            config.socketserver = False
        config.sockethost = read_config( cmdarg.configfile, "sockethost")
        config.socketport = read_config( cmdarg.configfile, "socketport")
        logger.debug("SocketServer: " + str(config.socketserver))
        logger.debug("SocketHost: " + str(config.sockethost))
        logger.debug("SocketPort: " + str(config.socketport))
        
        # -----------------------
        # WHITELIST
        if (read_config(cmdarg.configfile, "whitelist_active") == "yes"):
            config.whitelist_active = True
        else:
            config.whitelist_active = False         
        config.whitelist_file = read_config( cmdarg.configfile, "whitelist_file")
        logger.debug("Whitelist_active: " + str(config.whitelist_active))
        logger.debug("Whitelist_file: " + str(config.whitelist_file))

        # -----------------------
        # DAEMON
        if (read_config(cmdarg.configfile, "daemon_active") == "yes"):
            config.daemon_active = True
        else:
            config.daemon_active = False
        config.daemon_pidfile = read_config( cmdarg.configfile, "daemon_pidfile")
        logger.debug("Daemon_active: " + str(config.daemon_active))
        logger.debug("Daemon_pidfile: " + str(config.daemon_pidfile))
        
        # -----------------------
        # WEEWX
        if (read_config(cmdarg.configfile, "weewx_active") == "yes"):
            config.weewx_active = True
        else:
            config.weewx_active = False
        config.weewx_config = read_config( cmdarg.configfile, "weewx_config")
        logger.debug("WeeWx_active: " + str(config.weewx_active))
        logger.debug("WeeWx_config: " + str(config.weewx_config))
        
        # ------------------------
        # RRD
        if (read_config(cmdarg.configfile, "rrd_active") == "yes"):
            config.rrd_active = True
        else:
            config.rrd_active = False
        
        # If RRD path is empty, then use the script path
        config.rrd_path = read_config( cmdarg.configfile, "rrd_path")
        if not config.rrd_path:
            config.rrd_path = os.path.dirname(os.path.realpath(__file__))
        
        # ------------------------
        # BAROMETRIC
        config.barometric = read_config(cmdarg.configfile, "barometric")
        
        # ------------------------
        # LOG MESSAGES
        if (read_config(cmdarg.configfile, "log_msg") == "yes"):
            config.log_msg = True
        else:
            config.log_msg = False
        config.log_msgfile = read_config(cmdarg.configfile, "log_msgfile")
        
        # ------------------------
        # PROTOCOLS
        if (read_config(cmdarg.configfile, "protocol_startup") == "yes"):
            config.protocol_startup = True
        else:
            config.protocol_startup = False
        config.protocol_file = read_config(cmdarg.configfile, "protocol_file")
        
    else:
        # config file not found, set default values
        print "Error: Configuration file not found (" + cmdarg.configfile + ")"
        logger.error("Error: Configuration file not found (" + cmdarg.configfile + ") Line: " + _line())

# ------------------------------------------------------------------------------
# END
# ------------------------------------------------------------------------------
