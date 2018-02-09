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

def makeKey(vendorkey, devicepassword, userpassword) :
    vendorkeyb = base64.b64decode(vendorkey)
    key1 = hashlib.md5(devicepassword.replace('-','').encode('iso8859-1') + vendorkeyb).digest()
    key2 = hashlib.md5(vendorkeyb + userpassword.encode('iso8859-1')).digest()
    return key1 + key2

def fetchData(host, path) :
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "TeleHeater/2.2.3"), ('Accept', "application/json")]
    url = 'http://' + host + path
    resp = opener.open(url)
    return resp.read()

def decrypt(key, data) :
    BS = AES.block_size
    INTERRUPT = '\u0001'
    PAD = '\u0000'
    decobj = AES.new(key, AES.MODE_ECB)
    cleartext = decobj.decrypt(base64.b64decode(data))
    return cleartext.rstrip(PAD.encode()).rstrip(INTERRUPT.encode())

def get(host, path, key) :
    response = fetchData(host, path)
    return decrypt(key, response)

def main() :
    parser = argparse.ArgumentParser(description='Read data from REGO2000')
    parser.add_argument('-m', '--mode', default='json')
    parser.add_argument('-c', '--configfile', required=True)
    parser.add_argument('-s', '--configsection', required=True)
    parser.add_argument('-p', '--path', required=True)
    parser.add_argument('-x', '--explore', action='store_true', help='use the list of starting points in <path> to fetch and enumerate all available URLs')
    args = parser.parse_args()

    config = configparser.SafeConfigParser()
    config.read(args.configfile)
    host = config.get(args.configsection, 'host');
    vendorkey = config.get(args.configsection, 'vendorkey');
    devicepassword = config.get(args.configsection, 'devicepassword');
    userpassword = config.get(args.configsection, 'userpassword');
    key = makeKey(vendorkey, devicepassword, userpassword)

    if args.explore :
        startpaths = args.path.split(',')
        leaves = []
        while startpaths :
            sp = startpaths.pop().strip()
            sys.stderr.write("Trying " + sp + "\n")
            try :
                res = json.loads(get(host, sp, key).decode())
                if res["type"] == "refEnum" :
                    for nsp in res["references"] :
                        startpaths.append(nsp["id"])
                elif "value" in res :
                    leaves.append("scalar:" + sp)
                elif "values" in res :
                    leaves.append("vector:" + sp)
                else :
                    leaves.append("unknown:" + sp)
            except:
                sys.stderr.write('Caught exception\n')
                pass
        leaves.sort()
        for leaf in leaves :
            print(leaf)
                    
    else :
        data = get(host, args.path, key)

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
        elif args.mode == 'values':
            pdata = json.loads(data.decode())
            print(json.dumps(pdata["values"], sort_keys=True, indent=4))
        elif args.mode == 'errcodes':
            ecfile = config.get(args.configsection, 'errcodes');
            with open(ecfile) as data_file:
                errcodes = json.load(data_file)
            pdata = json.loads(data.decode())
            for v in pdata["values"] :
                print(json.dumps(v, sort_keys=True, indent=4))
                if v["ccd"] in errcodes :
                    print(json.dumps(errcodes[v["ccd"]], sort_keys=True, indent=4))
                print("--------------")

if __name__ == "__main__":
    main()
