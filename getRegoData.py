#!/usr/bin/env python3

import sys
import base64
import json
import binascii
import hashlib
import urllib.request
import argparse
import configparser
from Crypto.Cipher import AES

def main():
    parser = argparse.ArgumentParser(description='Read data from REGO2000')
    parser.add_argument('-m', '--mode', default='json')
    parser.add_argument('-c', '--configfile', required=True)
    parser.add_argument('-s', '--configsection', required=True)
    parser.add_argument('-p', '--path', required=True)
    args = parser.parse_args()

    config = configparser.SafeConfigParser()
    config.read(args.configfile)
    host = config.get(args.configsection, 'host');
    vendorkey = config.get(args.configsection, 'vendorkey');
    devicepassword = config.get(args.configsection, 'devicepassword');
    userpassword = config.get(args.configsection, 'userpassword');

    vendorkeyb = base64.b64decode(vendorkey)
    key1 = hashlib.md5(devicepassword.replace('-','').encode('iso8859-1') + vendorkeyb).digest()
    key2 = hashlib.md5(vendorkeyb + userpassword.encode('iso8859-1')).digest()
    key = key1 + key2
    
    BS = AES.block_size
    INTERRUPT = '\u0001'
    PAD = '\u0000'
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "TeleHeater/2.2.3"), ('Accept', "application/json")]
    url = 'http://' + host + args.path
    resp = opener.open(url)
    decobj = AES.new(key, AES.MODE_ECB)
    data = decobj.decrypt(base64.b64decode(resp.read()))
    data = data.rstrip(PAD.encode()).rstrip(INTERRUPT.encode())

    if args.mode == 'raw':
        print(data)
    elif args.mode == 'string':
        print(data.decode())
    elif args.mode == 'json':
        pdata = json.loads(data.decode())
        print(json.dumps(pdata, sort_keys=True, indent=4))
    elif args.mode == 'value':
        pdata = json.loads(data.decode())
        print(pdata["value"])

if __name__ == "__main__":
    main()
