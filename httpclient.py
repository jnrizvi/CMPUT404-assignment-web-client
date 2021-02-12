#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

# I don't like doing it like this, but regex is not working
status_codes = ['200', '300', '301', '302', '400', '404']

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def pretty_print(self):
        print("Code:", self.code)
        print("Body:", self.body)

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    # TODO - String format the result returned by recvall
    def get_code(self, data):
        headers = data.split("\r\n\r\n")[0]
        http_status_header = headers.split("\r\n")[0]
        
        # print(http_status_header, type(http_status_header))

        # match = re.match("\d{3}", http_status_header)
        # if match:
        for code in status_codes:
            if code in http_status_header:
                # print(code)
                return code
            # print(match.group())
            # return match.group()

        return None
    
    # TODO - String format the result returned by recvall
    def get_headers(self,data):
        headers = data.split("\r\n\r\n")[0]
        headers_as_list = headers.split("\r\n")
        
        # print(headers_as_list)
        return headers_as_list
        return None

    # TODO - String format the result returned by recvall
    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]

        # print(body)
        return body
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # TODO - handle 404 requests and 200 requests
    def GET(self, url, args=None):
        code = 500
        body = ""

        print("THE URL IS:", url)
        print("THE ARGS ARE:", args)
        print()

        # can we use this?
        components = urllib.parse.urlparse(url)
        port = components.port
        host = components.hostname
        # print("port:", port, "host:", host)
        if port == None:
            # if there's no host, set port to 80 as default
            port = 80

        # host, port from url
        self.connect(host, port)

        # make up payload string, format with path and host. Encode it after?
        payload = f'GET / HTTP/1.1\r\nHost: {host}\r\n\r\n'

        # (encoded) payload goes in here?
        self.sendall(payload)

        result = self.recvall(self.socket)
        
        # status code (within headers)
        code = self.get_code(result)

        # headers
        headers = self.get_headers(result)

        # body
        body = self.get_body(result)

        self.close()

        # Is it possible to pretty print this?
        return HTTPResponse(int(code), body)

    # TODO - handle 404 requests and 200 requests
    # I think args is referring to what's in the url: parameter=value
    def POST(self, url, args=None):
        code = 500
        body = ""

        print("THE URL IS:", url)
        print("THE ARGS ARE:", args)
        print()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()

    
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
        # client.command( sys.argv[2], sys.argv[1] ).pretty_print()
    else:
        print(client.command( sys.argv[1] ))

# Remember that a client (socket) starts a connection to a server socket that is listening.
# There is no server in this assignment, which is why we just print out the result of GET/POST

# just use urllib.parseurl and send the data? with a standard GET / POST request
# then print the body that gets returned

# http://www.cs.ualberta.ca/
# http://softwareprocess.es/static/SoftwareProcess.es.html
# http://c2.com/cgi/wiki?CommonLispHyperSpec
# http://slashdot.org