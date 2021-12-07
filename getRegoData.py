#!/usr/bin/env python3

import sys
import traceback
import base64
import json
import binascii
import hashlib
import urllib.request
import argparse
import configparser
from Crypto.Cipher import AES
from quik import FileLoader

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

def postData(host, path, d) :
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', "TeleHeater/2.2.3"), ('Accept', "application/json"), ('Content-Type', 'application/json')]
    url = 'http://' + host + path
    resp = opener.open(url, data=d)
    return resp.read()

def decrypt(key, data) :
    BS = AES.block_size
    INTERRUPT = '\u0001'
    PAD = '\u0000'
    decobj = AES.new(key, AES.MODE_ECB)
    cleartext = decobj.decrypt(base64.b64decode(data))
    return cleartext.rstrip(PAD.encode()).rstrip(INTERRUPT.encode())

def addPadding(data, interrupt, pad, block_size):
    new_data = ''.join([data, interrupt])
    new_data_len = len(new_data)
    remaining_len = block_size - new_data_len
    to_pad_len = remaining_len % block_size
    pad_string = pad * to_pad_len
    return ''.join([new_data, pad_string])
                        
def encrypt(key, data) :
    BS = AES.block_size
    INTERRUPT = '\u0001'
    PAD = '\u0000'
    encobj = AES.new(key, AES.MODE_ECB)
    pdata = addPadding(data, INTERRUPT, PAD, AES.block_size)
    ciphertext = base64.b64encode(encobj.encrypt(pdata))
    return ciphertext

def get(host, path, key) :
    response = fetchData(host, path)
    return decrypt(key, response)

def post(host, path, key, data) :
    cdata = encrypt(key, data)
    response = postData(host, path, cdata)
    return response

def main() :
    parser = argparse.ArgumentParser(description='Read data from REGO2000')
    parser.add_argument('-m', '--mode', default='json')
    parser.add_argument('-c', '--configfile', required=True)
    parser.add_argument('-s', '--configsection', required=True)
    parser.add_argument('-p', '--path', required=True)
    parser.add_argument('-x', '--explore', action='store_true', help='use the list of starting points in <path> to fetch and enumerate all available URLs')
    parser.add_argument('-S', '--set', help='Set a new value')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.configfile)
    host = config.get(args.configsection, 'host');
    vendorkey = config.get(args.configsection, 'vendorkey');
    devicepassword = config.get(args.configsection, 'devicepassword');
    userpassword = config.get(args.configsection, 'userpassword');
    key = makeKey(vendorkey, devicepassword, userpassword)
    htmltemplate = config.get(args.configsection, 'htmltemplate');

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
                sys.stderr.write('Caught exception!\n')
                traceback.print_exc()
                pass
        leaves.sort()
        for leaf in leaves :
            print(leaf)

    elif args.set:
        data = get(host, args.path, key)
        pdata = json.loads(data.decode())
        sys.stderr.write('Change value of ' + args.path + ' from ' + pdata["value"] + ' to ' + args.set + '\n')
        newdict = {"value" : args.set}
        newdata = json.dumps(newdict)
        sys.stderr.write(post(host, args.path, key, newdata).decode())
        
    else :
        try:
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
                notifications=[]
                for v in pdata["values"] :
                    note={}
                    note["orig"] = v
                    if str(v["ccd"]) in errcodes :
                        note["explanation"] = errcodes[str(v["ccd"])]
                    notifications.append(note)
                loader = FileLoader('')
                template = loader.load_template(htmltemplate)
                if notifications : 
                    print (template.render(locals(), loader=loader))
                else :
                    print ('<html><head></head><body><h1>No active notifications</h1></body></html>');
        except:
            print ('N/A')
            pass

if __name__ == "__main__":
    main()
