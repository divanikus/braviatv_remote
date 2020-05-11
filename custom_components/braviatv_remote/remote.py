"""Emulation of BraviaTV IR devices."""
import logging
import socket
import voluptuous as vol

from requests import Session
from homeassistant.components import remote
from homeassistant.components.remote import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_DEVICES,
    CONF_HOST,
    CONF_NAME,
    DEVICE_DEFAULT_NAME,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONNECT_TIMEOUT = 5000
CONF_PSK = 'psk'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICES): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Optional(CONF_HOST): cv.string,
                    vol.Optional(CONF_NAME): cv.string,
                    vol.Optional(CONF_PSK): cv.string,
                }
            ],
        ),
    }
)
COMMANDS = {
    'num1': 'AAAAAQAAAAEAAAAAAw==',
    'num2': 'AAAAAQAAAAEAAAABAw==',
    'num3': 'AAAAAQAAAAEAAAACAw==',
    'num4': 'AAAAAQAAAAEAAAADAw==',
    'num5': 'AAAAAQAAAAEAAAAEAw==',
    'num6': 'AAAAAQAAAAEAAAAFAw==',
    'num7': 'AAAAAQAAAAEAAAAGAw==',
    'num8': 'AAAAAQAAAAEAAAAHAw==',
    'num9': 'AAAAAQAAAAEAAAAIAw==',
    'num0': 'AAAAAQAAAAEAAAAJAw==',
    'num11': 'AAAAAQAAAAEAAAAKAw==',
    'num12': 'AAAAAQAAAAEAAAALAw==',
    'enter': 'AAAAAQAAAAEAAAALAw==',
    'gguide': 'AAAAAQAAAAEAAAAOAw==',
    'channelup': 'AAAAAQAAAAEAAAAQAw==',
    'channeldown': 'AAAAAQAAAAEAAAARAw==',
    'volumeup': 'AAAAAQAAAAEAAAASAw==',
    'volumedown': 'AAAAAQAAAAEAAAATAw==',
    'mute': 'AAAAAQAAAAEAAAAUAw==',
    'TOGGLE': 'AAAAAQAAAAEAAAAVAw==',
    'audio': 'AAAAAQAAAAEAAAAXAw==',
    'nediaaudiotrack': 'AAAAAQAAAAEAAAAXAw==',
    'tv2': 'AAAAAQAAAAEAAAAkAw==',
    'input': 'AAAAAQAAAAEAAAAlAw==',
    'tvinput': 'AAAAAQAAAAEAAAAlAw==',
    'tvantennacable': 'AAAAAQAAAAEAAAAqAw==',
    'ON': 'AAAAAQAAAAEAAAAuAw==',
    'OFF': 'AAAAAQAAAAEAAAAvAw==',
    'sleep': 'AAAAAQAAAAEAAAAvAw==',
    'right': 'AAAAAQAAAAEAAAAzAw==',
    'left': 'AAAAAQAAAAEAAAA0Aw==',
    'sleeptimer': 'AAAAAQAAAAEAAAA2Aw==',
    'analog2': 'AAAAAQAAAAEAAAA4Aw==',
    'tvanalog': 'AAAAAQAAAAEAAAA4Aw==',
    'display': 'AAAAAQAAAAEAAAA6Aw==',
    'jump': 'AAAAAQAAAAEAAAA7Aw==',
    'picoff': 'AAAAAQAAAAEAAAA+Aw==',
    'pictureoff': 'AAAAAQAAAAEAAAA+Aw==',
    'teletext': 'AAAAAQAAAAEAAAA/Aw==',
    'video1': 'AAAAAQAAAAEAAABAAw==',
    'video2': 'AAAAAQAAAAEAAABBAw==',
    'analogrgb1': 'AAAAAQAAAAEAAABDAw==',
    'home': 'AAAAAQAAAAEAAABgAw==',
    'exit': 'AAAAAQAAAAEAAABjAw==',
    'picturmode': 'AAAAAQAAAAEAAABkAw==',
    'confirm': 'AAAAAQAAAAEAAABlAw==',
    'up': 'AAAAAQAAAAEAAAB0Aw==',
    'down': 'AAAAAQAAAAEAAAB1Aw==',
    'closedcaption': 'AAAAAgAAAKQAAAAQAw==',
    'component1': 'AAAAAgAAAKQAAAA2Aw==',
    'component2': 'AAAAAgAAAKQAAAA3Aw==',
    'eide': 'AAAAAgAAAKQAAAA9Aw==',
    'rpg': 'AAAAAgAAAKQAAABbAw==',
    'pap': 'AAAAAgAAAKQAAAB3Aw==',
    'tenkey': 'AAAAAgAAAJcAAAAMAw==',
    'bscs': 'AAAAAgAAAJcAAAAQAw==',
    'ddata': 'AAAAAgAAAJcAAAAVAw==',
    'stop': 'AAAAAgAAAJcAAAAYAw==',
    'pause': 'AAAAAgAAAJcAAAAZAw==',
    'play': 'AAAAAgAAAJcAAAAaAw==',
    'rewind': 'AAAAAgAAAJcAAAAbAw==',
    'forward': 'AAAAAgAAAJcAAAAcAw==',
    'dot': 'AAAAAgAAAJcAAAAdAw==',
    'rec': 'AAAAAgAAAJcAAAAgAw==',
    'return': 'AAAAAgAAAJcAAAAjAw==',
    'blue': 'AAAAAgAAAJcAAAAkAw==',
    'red': 'AAAAAgAAAJcAAAAlAw==',
    'green': 'AAAAAgAAAJcAAAAmAw==',
    'yellow': 'AAAAAgAAAJcAAAAnAw==',
    'subtitle': 'AAAAAgAAAJcAAAAoAw==',
    'cs': 'AAAAAgAAAJcAAAArAw==',
    'bs': 'AAAAAgAAAJcAAAAsAw==',
    'digital': 'AAAAAgAAAJcAAAAyAw==',
    'options': 'AAAAAgAAAJcAAAA2Aw==',
    'media': 'AAAAAgAAAJcAAAA4Aw==',
    'prev': 'AAAAAgAAAJcAAAA8Aw==',
    'next': 'AAAAAgAAAJcAAAA9Aw==',
    'dpadcenter': 'AAAAAgAAAJcAAABKAw==',
    'cursorup': 'AAAAAgAAAJcAAABPAw==',
    'cursordown': 'AAAAAgAAAJcAAABQAw==',
    'cursorleft': 'AAAAAgAAAJcAAABNAw==',
    'cursorright': 'AAAAAgAAAJcAAABOAw==',
    #'shopremotecontrolforceddynamic': 'AAAAAgAAAJcAAABqAw==',
    'flashplus': 'AAAAAgAAAJcAAAB4Aw==',
    'flashminus': 'AAAAAgAAAJcAAAB5Aw==',
    'demomode': 'AAAAAgAAAJcAAAB8Aw==',
    'analog': 'AAAAAgAAAHcAAAANAw==',
    'mode3d': 'AAAAAgAAAHcAAABNAw==',
    'digitaltoggle': 'AAAAAgAAAHcAAABSAw==',
    'demosurround': 'AAAAAgAAAHcAAAB7Aw==',
    'ad': 'AAAAAgAAABoAAAA7Aw==',
    'audiomixup': 'AAAAAgAAABoAAAA8Aw==',
    'audiomixdown': 'AAAAAgAAABoAAAA9Aw==',
    'photoframe': 'AAAAAgAAABoAAABVAw==',
    'tv_radio': 'AAAAAgAAABoAAABXAw==',
    'syncmenu': 'AAAAAgAAABoAAABYAw==',
    'hdmi1': 'AAAAAgAAABoAAABaAw==',
    'hdmi2': 'AAAAAgAAABoAAABbAw==',
    'hdmi3': 'AAAAAgAAABoAAABcAw==',
    'hdmi4': 'AAAAAgAAABoAAABdAw==',
    'topmenu': 'AAAAAgAAABoAAABgAw==',
    'popupmenu': 'AAAAAgAAABoAAABhAw==',
    'onetouchtimerec': 'AAAAAgAAABoAAABkAw==',
    'onetouchview': 'AAAAAgAAABoAAABlAw==',
    'dux': 'AAAAAgAAABoAAABzAw==',
    'footballmode': 'AAAAAgAAABoAAAB2Aw==',
    'imanual': 'AAAAAgAAABoAAAB7Aw==',
    'netflix': 'AAAAAgAAABoAAAB8Aw==',
    'assists': 'AAAAAgAAAMQAAAA7Aw==',
    'featuredapp': 'AAAAAgAAAMQAAABEAw==',
    'featuredappvod': 'AAAAAgAAAMQAAABFAw==',
    'googleplay': 'AAAAAgAAAMQAAABGAw==',
    'actionmenu': 'AAAAAgAAAMQAAABLAw==',
    'help': 'AAAAAgAAAMQAAABNAw==',
    'tvsatellite': 'AAAAAgAAAMQAAABOAw==',
    'wirelesssubwoofer': 'AAAAAgAAAMQAAAB+Aw==',
    'androidmenu': 'AAAAAgAAAMQAAABPAw==',
    'youtube': 'AAAAAgAAAMQAAABHAw=='
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the zmote connection and devices."""
    devices = []
    for data in config.get(CONF_DEVICES):
        name = data.get(CONF_NAME)
        host = data.get(CONF_HOST)
        psk  = data.get(CONF_PSK)
        devices.append(BraviaRemote(name, host, psk))
    add_entities(devices, True)
    return True

class HTTPTransport(object):
    def __init__(self, ip, psk):
        self._ip  = ip
        self._psk = psk
        self._session = None

    def connect(self):
        self._session = Session()

    def call(self, data):
        msg = ("<?xml version=\"1.0\"?>"
                "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">"
                    "<s:Body>"
                        "<u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\">"
                            "<IRCCCode>{0}</IRCCCode>"
                        "</u:X_SendIRCC>"
                    "</s:Body>"
                "</s:Envelope>").format(data)
        headers = {
            'Content-Type': "text/xml; charset=UTF-8",
            'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
            'X-Auth-PSK': self._psk,
        }
        output = self._session.post(
            url='http://{0}/sony/IRCC'.format(self._ip),
            data=msg,
            headers=headers,
            timeout=5,
        ).text
        return output

    def disconnect(self):
        self._session = None

class BraviaRemote(remote.RemoteDevice):
    """Device that sends commands to an BraviaTV device."""

    def __init__(self, name, host, psk):
        """Initialize device."""
        self.connector = HTTPTransport(host, psk)
        self._power = False
        self._name = name or DEVICE_DEFAULT_NAME

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._power

    def toggle(self, **kwargs):
        """Toggle device."""
        self._power = not self._power
        self.send_command(["TOGGLE"])
        self.schedule_update_ha_state()

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._power = True
        self.send_command(["ON"])
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._power = False
        self.send_command(["OFF"])
        self.schedule_update_ha_state()

    def send_command(self, command, **kwargs):
        """Send a command to one device."""
        self.connector.connect()
        for single_command in command:
            if single_command in COMMANDS:
                self.connector.call(COMMANDS[single_command])
        self.connector.disconnect()

    def update(self):
        """Update the device."""
