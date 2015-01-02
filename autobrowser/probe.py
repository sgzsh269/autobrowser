import os
import socket
import re
import json
import traceback
import logging
import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.httpserver
from selenium import webdriver

_report_js = open(os.path.join(os.path.dirname(__file__), "reporter.js"))
_probe = None
_activity_output_file = None

_logger = logging.getLogger("autobrowser.probe")
_logger.setLevel(logging.INFO)
_logger.propagate = False
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("%(message)s"))
_logger.addHandler(_handler)

class Probe():

    """
    This class helps to probe the webpage by identifying HTML elements of
    interest on user mousedown event, in particular it identifies the css
    location of the element which can then be used by a css selector to
    retrieve the element. It saves the elements of interest in the
    'activity_output_file' provided.

    It relies on:-
    1. selenium webdriver - to start web browser and embed 'reporter.js'
    2. reporter.js - js file to catch user click events on HTML element of
    interest and report them back to Probe
    3. Tornado webserver - listener for the user click events reported by
    reporter.js
    """

    def __init__(self, selenium_webdriver, ssl_privatekey_file,
                 ssl_certificate_file, activity_output_file):
        global _probe
        global _activity_output_file

        self.ssl_certificate_file = ssl_certificate_file
        self.ssl_privatekey_file = ssl_privatekey_file
        self.webdriver = selenium_webdriver
        self.activity_output_file = activity_output_file
        self._report_js = None

        _activity_output_file = open(activity_output_file, "w")
        _activity_output_file.write("event^datetime^elem_location^elem_id^"
                                    "elem_tagName^elem_className^"
                                    "elem_innerHTML^css_location\n")
        _activity_output_file.flush()
        _probe = self

    def _get_random_open_port(self):
        sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def _read_report_js(self, port):
        report_js = ""
        for l in _report_js:
            replaced = re.sub("%port%", str(port), l)
            report_js += replaced
        return report_js

    def _exec_report_js(self):
        self.webdriver.execute_script(self._report_js + "return null;")

    def start(self):
        port = self._get_random_open_port()
        self._report_js = self._read_report_js(port)
        ssl_options = {
            "certfile": self.ssl_certificate_file,
            "keyfile": self.ssl_privatekey_file
        }
        _listener = tornado.web.Application([(r"/", ListenerHandler)])
        _http_server = tornado.httpserver.HTTPServer(_listener,
                                                    ssl_options = ssl_options)
        _http_server.listen(port)
        self._exec_report_js()
        tornado.ioloop.IOLoop.instance().start()

class ListenerHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.current_url = _probe.webdriver.current_url
        _logger.info("Probe READY on {0}".format(_probe.webdriver.current_url))

    def on_message(self, message):
        try:
            msgObj = json.loads(message)
            event = msgObj["event"]
            _logger.info(u"Probe EVENT received: {0}".format(message))
            if event == "mousedown":
                datetime = msgObj["datetime"]
                elem_location = msgObj["elem_location"]
                elem_id = msgObj["elem_id"]
                elem_tagName = msgObj["elem_tagName"]
                elem_className = msgObj["elem_className"]
                elem_innerHTML = msgObj["elem_innerHTML"]
                css_location = msgObj["css_location"]
                elem_signature = u"{0}^{1}^{2}^{3}^{4}^{5}^{6}^{7}\n".format(
                                                event, datetime,
                                                elem_location, elem_id,
                                                elem_tagName, elem_className,
                                        elem_innerHTML, css_location)

                _activity_output_file.write(elem_signature.encode("utf-8"))
                _activity_output_file.flush()

        except Exception:
            _logger.info(traceback.format_exc())

    def on_close(self):
        _probe.webdriver.current_url
        _probe._exec_report_js()
        _logger.info("Probe CLOSED on {0}".format(self.current_url))

    def check_origin(self, origin):
        return True

