#!/usr/bin/env python

"""
Copyright (C) 2012 by Kelly L. McLaughlin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys
import argparse
import urllib2
import httplib
import json
import base64

def get_item(AuthCreds, ProductId, ItemId):
    SprintlyUrl = 'https://sprint.ly/api/products/' + ProductId + '/items/' + str(ItemId) + '.json'
    print SprintlyUrl
    req = urllib2.Request(SprintlyUrl, None, {'Authorization': 'Basic ' + AuthCreds})
    opener = urllib2.build_opener()
    f = opener.open(req)
    return json.load(f)

def update_item_tags(AuthCreds, ProductId, ItemId, Tags):
    Url = '/api/products/' + ProductId + '/items/' + str(ItemId) + '.json'
    conn = httplib.HTTPSConnection('sprint.ly')
    conn.request("POST", Url, 'tags=' + Tags, {'Authorization': 'Basic ' + AuthCreds})
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return True

parser = argparse.ArgumentParser(description='Tag a set of sprint.ly items.')
parser.add_argument('-i', metavar='Item', type=int, nargs='+', required=True,
                   help='Items to tag. e.g. 56 44 32')
parser.add_argument('-t', metavar='Tag', nargs='+', required=True,
                    help='List of one or more tags. e.g. red blue')
parser.add_argument('-u', metavar='UserId', nargs=1, required=True,
                   help='Sprintly user id (email address)')
parser.add_argument('-k', metavar='ApiKey', nargs=1, required=True,
                   help='Sprintly API Key')
parser.add_argument('-p', metavar='ProductId', nargs=1, required=True,
                   help='Sprintly Product Id')
parser.add_argument('--replace', action='store_true',
                   help='replace all existing tags')
args = parser.parse_args()

item_ids = args.i
new_tags = args.t
replace = args.replace
user_id = args.u[0]
api_key = args.k[0]
product_id = args.p[0]
auth_creds = base64.encodestring('%s:%s' % (user_id, api_key))[:-1]

for item_id in item_ids:
    if not replace:
        print 'Fetching item ' + str(item_id)
        item_json = get_item(auth_creds, product_id, item_id)
        print item_json
        tags = ",".join(item_json['tags'])
        for tag in new_tags:
            tags += ',' + tag
    else:
        tags = ",".join(new_tags)

    # Update the item
    update_item_tags(auth_creds, product_id, item_id, tags)
