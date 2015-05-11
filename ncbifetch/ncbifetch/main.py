#!/usr/bin/env python

# Copyright 2015 Nabil-Fareed Alikhan. Licensed under the
#     Educational Community License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may
#     obtain a copy of the License at
#
#      http://www.osedu.org/licenses/ECL-2.0
#
#     Unless required by applicable law or agreed to in writing,
#     software distributed under the License is distributed on an "AS IS"
#     BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#     or implied. See the License for the specific language governing
#     permissions and limitations under the License.


"""
Fetching data from NCBI

TODO: Detailed description

### CHANGE LOG ###
2015-05-10 Nabil-Fareed Alikhan <nabil@happykhan.com>
    * Initial build
"""
import sys, os, traceback, argparse
import time
import __init__ as meta
import logging
import re


epi = "Licence: "+meta.__licence__ +  " by " +meta.__author__ + " <" +meta.__author_email__ + ">"

def x():
    return 'ping'

def fetch_wgs(organism='Escherichia'):
    import requests
    import json
    import xml.etree.ElementTree as ET


    print('Running for %s ' %organism)
    esearch = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    elink = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    efetch = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    traces =  'http://www.ncbi.nlm.nih.gov/Traces/wgs/fdump.cgi'
    # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=genome&term=txid28901&retmax=10
    search_param = dict(db='genome', term=organism, retmode='json')
    r = requests.get(esearch, search_param)
    genome_ids = json.loads(r.text)['esearchresult']['idlist']
    from httplib import IncompleteRead
    import xmltodict

    # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=genome&db=nuccore&id=152&term=wgs[prop]
    for genome_id in genome_ids:
        link_param = dict(dbfrom='genome', id=genome_id, term='wgs[prop]', db='nuccore', retmode='json')
        r = requests.get(elink, link_param)
        seq_ids = []
        for line in r.text.split('\n'):
            m = re.search('<Id>(\d+)<\/Id>', line)

            if m != None: seq_ids.append(m.group(1))
      #  for seq_id in seq_ids[1:]:
        for listid in seq_ids:
            fetch_param = dict(db='nuccore', id=str(listid), rettype='native', retmode='xml')
            try:
                # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=816135311
                time.sleep(3)
                r = requests.get(efetch, fetch_param)
                read_record(r.text.split('\n'))
            except IncompleteRead as e:  #
                print 'Error with %s' % listid

    # How to retieve raw sequence:
    # http://www.ncbi.nlm.nih.gov/Traces/wgs/fdump.cgi?JMML02,89


def read_record(text):
    row = ''
    headers = []
    dat = []
    for line in text:
        m = re.search('<Object-id_str>(.+)</Object-id_str>', line)
        if m != None: headers.append(m.group(1))

        m = re.search('<Dbtag_db>WGS:(.+)</Dbtag_db>', line)
        if m != None: dat.append(m.group(1))

        m = re.search('<Textseq-id_accession>(.+)</Textseq-id_accession>', line)
        if m != None: dat.append(m.group(1))

        m = re.search('<User-field_data_str>(.+)</User-field_data_str>', line)
        if m != None: dat.append(m.group(1))

    print  '#' + '\t'.join(headers)
    print '\t'.join(dat)




def main ():

    global args
    # TODO: Do something more interesting here...
    print 'Hello world!'
    # READ AND PRINT first positional argument (if any)
    # If you want to access positional arguments with argparse:
    # Use global "args" (declared above) not argv[0]
    if args.output != None:
        print 'Output: ' + args.output
    print args

    print args.verbose
    print args.output
    print args.arg1

if __name__ == '__main__':
    try:
        start_time = time.time()
        desc = __doc__.split('\n\n')[1].strip()
        parser = argparse.ArgumentParser(description=desc,epilog=epi)
        # EXAMPLE OF BOOLEAN FLAG: verbose
        parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument('--version', action='version', version='%(prog)s ' + meta.__version__)
        # EXAMPLE OF command line variable: 'output'
        parser.add_argument('-o','--output',action='store',help='output prefix')
        # EXAMPLE OF POSITIONAL ARGUMENT
        parser.add_argument ('arg1', action='store', type=int, help='First positional argument (INT)')
        parser.add_argument ('arg2', action='store', help='2nd positional argument (STRING)')
        # EXAMPLE OF NESTED PARAMETERS

        # subparsers = parser.add_subparsers(help='commands')
        # list_parser = subparsers.add_parser('list', help='List contents')
        # list_parser.add_argument('dirname', action='store', help='Directory to list')

        args = parser.parse_args()
        if args.verbose: print "Executing @ " + time.asctime()
        main()
        if args.verbose: print "Ended @ " + time.asctime()
        if args.verbose: print 'total time in minutes:',
        if args.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
