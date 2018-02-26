"""BlackBean Server

Copyright (c) 2018 Daisuke IMAI

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""
import time
import json
import threading
from os import path

import broadlink
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

import commands


class BlackBeanManager(object):
    """Management Blackbean Class
    """

    def __init__(self):
        self._is_connected = False
        self._rf_commands = commands.rf_commands
        self._start_connector()

    def is_connected(self):
        return self._is_connected

    def check_command(self, rf_command):
        return self._rf_commands.has_key(rf_command)

    def send_command(self, rf_command):
        command = self._get_command(rf_command)
        if command == False:
            return False
        else:
            try:
                self._device.send_data(command.decode('hex'))
            except:
                self._is_connected = False
                return False
            else:
                return True

    def _get_command(self, rf_command):
        if self._rf_commands.has_key(rf_command):
            return self._rf_commands[rf_command]
        else:
            return False

    def _start_connector(self):
        self._connector_thread = threading.Thread(target=self._connector)
        self._connector_thread.setDaemon(True)
        self._connector_thread.start()

    def _connector(self):
        while True:
            if self._is_connected:
                time.sleep(60)
            else:
                devices = broadlink.discover(timeout=15)
                if len(devices) > 0:
                    self._is_connected = True
                    self._device = devices[0]
                    self._device.auth()


# make instance
blackbean = BlackBeanManager()


class BlackBeanHandler(APIHandler):
    """API Handler for BlackBean
    """
    @schema.validate(
            output_schema={"type":"object"},
    )
    def get(self, device, command):
        return_data = {}
        return_data['received'] = {}
        return_data['received']['device'] = device
        return_data['received']['command'] = command
        rf_command = device + '/' + command
        return_data['rf_command'] = rf_command
        if blackbean.is_connected():
            if blackbean.check_command(rf_command):
                if blackbean.send_command(rf_command):
                    return_data['result'] = 'success'
                else:
                    return_data['result'] = 'error'
                    return_data['error_message'] = 'blackbean is disconnected'
            else:
                return_data['result'] = 'error'
                return_data['error_message'] = 'rf_command is not defined'
        else:
            return_data['result'] = 'error'
            return_data['error_message'] = 'blackbean is not connected'
        return return_data
