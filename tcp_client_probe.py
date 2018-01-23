##
# Just a TCP connection probe utility.
#
# Attempts to establish a plain TCP socket connection
# to a specified host on a specified port.
#
# Works on Python 2.7+ and 3.x
##
import sys
import argparse
import socket
import logging

# CONSTANTS
DEFAULT_TCP_PAYLOAD = "TEST_TCP_PAYLOAD"
DEFAULT_SOCKET_TIMEOUT_SECS = 30
BUFFER_SIZE_BYTES = 4096

# log to STDOUT with a decent timestamp
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def collect_command_line_params():
    argParser = argparse.ArgumentParser(description="TCP Connection Test")
    argParser.add_argument("--host", help="Hostname / IP Address of the server", required=True)
    argParser.add_argument("--port", help="Port on the server to connect to", required=True)
    argParser.add_argument("--payload", help="Payload to send over the TCP socket", required=False)
    argParser.add_argument("--timeout", help="Timeout (in seconds) for all operations. Default = 30", required=False)
    return vars(argParser.parse_args())

def main():
    args = collect_command_line_params()

    host = args["host"]
    port = args["port"]
    payload = args["payload"]
    timeout = args["timeout"]

    if payload is None:
        payload = DEFAULT_TCP_PAYLOAD

    # set the timeout (if provided)
    if timeout is None:
        timeout = DEFAULT_SOCKET_TIMEOUT_SECS
    socket.setdefaulttimeout(timeout)

    # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    logging.info("About to connect to %s on port %s ...", host, port)
    try:
        client.connect((host, int(port)))
        logging.info("Successfully connected to %s on port %s", host, port)
    except socket.error:
        logging.exception("Failed to connect to %s on port %s", host, port)
        sys.exit(-1)

    # send something on the socket
    logging.info("Sending something over the TCP connection ...")
    client.send(payload)
    logging.info("Successfully sent data over the TCP connection")

    # receive the response data
    logging.info("Waiting to receive data over the TCP connection [timeout=%s secs] ...", timeout)
    # if the server has closed the connection, we'll fail to read anything
    # from the socket ('connection reset by peer')
    try:
        client.recv(BUFFER_SIZE_BYTES)
    except socket.timeout:
        logging.info("Socket timeout after %s seconds", timeout)
    except socket.error:
        logging.exception("Seems like the server has reset the TCP connection.")
        sys.exit(-2)

if __name__ == '__main__':
    main()
