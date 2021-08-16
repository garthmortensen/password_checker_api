#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
#implement SQLite

#an api to manage user lockout when they get the password wrong too many times
#instead of the application itself lockout out the user, our API will manage the status of the user
#if they are locked out cause of wrong password

#define some "actions" that we'll need
#a "strike" is defined as getting their password wrong once

#add a strike, when they get their password wrong
#clearout strikes, action
#how long delay to automatically unlock the account, property
#how many strikes do they currently have?

#something about password reset?


def reply_message(self, message):
    """format message as utf-8 for display requirements"""

    message = str(message).format(self.path).encode('utf-8')
    self.wfile.write(message)


def parse_commands(self) -> list:
    """take in a string, parse it, and return the & split commands"""

    command = self.path.split("?")[1]
    commands = command.split("&")

    return commands


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        msg = '<html><head>LockoutAPI Admin page</head><body><p>Welcome to the LockoutAPI Admin page.<br>Enter your credentials to continue.<br></p><p>Username: <input type="text"><br>Password:  <input type="password"></p></body></html>'.format(self.path).encode('utf-8')

        if self.path == "/":
            reply_message(self, msg)

        if "/addStrike" in self.path:
            # print(self.path)

            commands = parse_commands(self)

            for cmd in commands:
                if "user=" in cmd:
                    user = cmd.split("=")[1]

            strike = ""  # select strike from table1 where user = "user"
            strike_message = "Added strike #:" + strike + " to user: " + user
            reply_message(self, strike_message)

        if "/getStrikeCount" in self.path:

            commands = parse_commands(self)
            print(commands)

            # issue: refactor this into a function
            for cmd in commands:
                if "user=" in cmd:
                    # user = cmd.split("=")[1]
                    strike_count = "2"  # select strike_count from table1 where user = "user"
                    count_message = "User strikes: " + strike_count
                    print(count_message)

                    reply_message(self, count_message)

        if self.path == "/clearStrikes":

            commands = parse_commands(self)

            for cmd in commands:
                if "org=" in cmd:
                    organization = cmd.split("=")[1]

                if "user=" in cmd:
                    user = cmd.split("=")[1]

            reply_message(self, "Clearing all strikes for user")

        # http://localhost:80/addStrike?u=ogagnon

        #path = self.path
        #command = path.split("?")[0]
        #arguments = path.split("?")[1].split("&")
        #print(command)
        #print(arguments)
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()