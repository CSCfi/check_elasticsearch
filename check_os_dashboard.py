#!/usr/bin/python
import argparse
import requests
from pprint import pprint as pprint
import urllib3
import sys
def get_parser():
    parser = argparse.ArgumentParser(description='Check_os_dashboard checks the status of Open Search Dashboard')
    parser.add_argument('--user', type=str, required=False,
                    help='user to use if anonymus user is not allowed')
    parser.add_argument('--password', type=str, required=False,
                    help='password to use if anonymus user is not allowed')
    parser.add_argument('--fqurl', type=str, required=True,
                    help='FQURL to status page useally: https://example.org/api/status')
    parser.add_argument('--no-verify', action='store_false',
                    help='If ssl certificates should be verified')
    args = parser.parse_args()
    return args

def get_status(args):
    if not args.no_verify:
        urllib3.disable_warnings()
    if args.user is not None:
        auth=(args.user, args.password)
    else:
        auth=()
    try:
        r = requests.get(args.fqurl, verify=args.no_verify, auth=auth)
    except:
        crit('Failed to connect to the server is, the fqurl correct?')
    if r.status_code != 200:
        unknown('return code: ' + str(r.status_code))
    return r.json()

def ok(reason):
    print ('OK - ' + reason )
    exit(0)
def warn(reason):
    print ('WARNING - ' + reason )
    exit(1)
def crit(reason):
    print ('CRITICAL - ' + reason )
    exit(2)
def unknown(reason):
    print ('UNKNOWN - ' + reason )
    exit(3)

def parse_status(status):
    i_ok = 0
    i_warning = 0
    i_critical = 0
    i_unknow = 0
    reason = ''
    try:
        for service in status['status']['statuses']:
            if service['state'] == 'green':
               i_ok += 1
               continue
            elif service['state'] == 'yellow':
               i_warning += 1
            elif service['state'] == 'red':
               i_critical += 1
            else:
               i_unknow += 1
            reason += service['id']
            reason += ' - ' + service['message'] + ' -- '
    except:
       unknown('Failed parsing the output - possible issue: ' + reason)
       return None
    if i_unknow > 0:
        unknow(reason)
    elif i_critical > 0:
        critical(reason)
    elif i_warning > 0:
        warning(reason)
    else:
        ok('Everything is fine')

def main():
    args = get_parser()
    status_json = get_status(args)
    parse_status(status_json)

main()
