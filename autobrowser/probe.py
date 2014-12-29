import os
import socket
import re
from flask import Flask, make_response, request
from selenium import webdriver
from OpenSSL import SSL

_REPORT_JS = open(os.path.join(os.path.dirname(__file__), "reporter.js"))
_PROBE = None
_LISTENER = Flask(__name__)
_ACTIVITY_OUTPUT_FILE = None

class Probe():

    """
    This class helps to probe the webpage by identifying HTML elements of
    interest on user click event. It saves the elements of interest in the
    'activity_output_file' provided.

    It relies on:-
    1. selenium webdriver - to start web browser and embed 'reporter.js'
    2. reporter.js - js file to catch user click events on HTML element of
    interest and report them back to Probe
    3. Flask webserver - listener for the user click events reported by
    reporter.js
    """

    def __init__(self, selenium_webdriver, ssl_privatekey_file,
                 ssl_certificate_file, activity_output_file):
        global _PROBE
        global _ACTIVITY_OUTPUT_FILE

        self._ssl_context = SSL.Context(SSL.TLSv1_2_METHOD)
        self._ssl_context.use_privatekey_file(ssl_privatekey_file)
        self._ssl_context.use_certificate_file(ssl_certificate_file)
        self.webdriver = selenium_webdriver
        self.activity_output_file = activity_output_file
        self._report_js = None

        _ACTIVITY_OUTPUT_FILE = open(activity_output_file, "w")
        _ACTIVITY_OUTPUT_FILE.write("event^datetime^elem_location^elem_id^"
                                    "elem_tagName^elem_className^"
                                    "elem_innerHTML^elem_locator\n")
        _ACTIVITY_OUTPUT_FILE.flush()
        _PROBE = self

    def _get_random_open_port(self):
        sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def _read_report_js(self, port):
        report_js = ""
        for l in _REPORT_JS:
            replaced = re.sub("%port%", str(port), l)
            report_js += replaced
        return report_js

    def _exec_report_js(self):
        self.webdriver.execute_script(self._report_js + "return null;")

    def start(self):
        port = self._get_random_open_port()
        self._report_js = self._read_report_js(port)
        self._exec_report_js()
        _LISTENER.run(port = port, ssl_context = self._ssl_context)

@_LISTENER.route("/")
def _report():
    event = request.args.get("event")
    if event == "click":
        datetime = request.args.get("datetime")
        elem_location = request.args.get("elem_location")
        elem_id = request.args.get("elem_id")
        elem_tagName = request.args.get("elem_tagName")
        elem_className = request.args.get("elem_className")
        elem_innerHTML = request.args.get("elem_innerHTML")
        elem_locator = request.args.get("elem_locator")
        elem_signature = "{0}^{1}^{2}^{3}^{4}^{5}^{6}^{7}".format(
                                                event, datetime,
                                                elem_location, elem_id,
                                                elem_tagName, elem_className,
                                                elem_innerHTML, elem_locator)

        _ACTIVITY_OUTPUT_FILE.write("{0}\n".format(elem_signature))
        _ACTIVITY_OUTPUT_FILE.flush()

    elif event == "unload":
        _PROBE.webdriver.current_url
        _PROBE._exec_report_js()

    response = make_response("")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

