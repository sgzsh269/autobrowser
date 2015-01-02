autobrowser: Toolset for automated browsing
===========================================

autobrowser aims to provide tools, with the help of 3rd party modules, to allow users to browse the web programmatically using a web browser.
It particularly helps to identify and access content from websites that do not have APIs.


Dependencies
------------

- Web browser (preferably Firefox)
- Python 2.7
- Python module: Tornado
- Python module: Selenium


Features
--------

- **Probe**:
    to help identify HTML elements and their exact css location in the DOM tree by user mousedown event on the HTML element in the web browser.
    The HTML elements identified will have a certain attribute set and this attribute set will be saved in the provided file, separated by the caret character ( ^ )

- **execution loop**:
    accepts a user function and can run it repeatedly in, either single-threaded sequential manner or multi-process periodical manner


Installation
------------

.. code-block:: bash

    $ pip install autobrowser

Usage
-----


- **For probing HTML elements in web browser**


  - *Please ensure to only use the default active tab in the invoked browser for probing.*
  - *Please let the browser completely load the webpage before starting to probe.*

.. code-block:: python

    from selenium import webdriver
    from autobrowser import probe

    wd = webdriver.Firefox()

    probe.Probe(wd, <path/to/ssl_privatekey_file>, <path/to/ssl_certificate_file>, <activity_output_file>).start()


*Example output*

.. code-block:: bash

    event^datetime^elem_location^elem_id^elem_tagName^elem_className^elem_innerHTML^css_location
    mousedown^2015-01-01T12:41:00.691Z^www.google.com.hk/^lst-ib^INPUT^gsfi lst-d-f^^BODY>DIV:nth-child(1)>DIV:nth-child(5)>FORM:nth-child(3)>DIV:nth-child(2)>DIV:nth-child(2)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(2)>DIV:nth-child(1)>INPUT:nth-child(1)
    mousedown^2015-01-01T12:41:05.202Z^www.google.com.hk/^^INPUT^^^BODY>DIV:nth-child(1)>DIV:nth-child(5)>FORM:nth-child(3)>DIV:nth-child(2)>DIV:nth-child(3)>CENTER:nth-child(1)>INPUT:nth-child(1)
    mousedown^2015-01-01T12:41:09.108Z^www.google.com.hk/^^A^^Giant panda - Wikipedia, the free encyclopedia^BODY>DIV:nth-child(1)>DIV:nth-child(7)>DIV:nth-child(3)>DIV:nth-child(7)>DIV:nth-child(2)>DIV:nth-child(3)>DIV:nth-child(1)>DIV:nth-child(2)>DIV:nth-child(2)>DIV:nth-child(2)>DIV:nth-child(2)>OL:nth-child(1)>DIV:nth-child(6)>LI:nth-child(1)>DIV:nth-child(1)>H3:nth-child(1)>A:nth-child(1)
    mousedown^2015-01-01T12:41:13.397Z^en.wikipedia.org/wiki/Giant_panda^^SPAN^^Giant panda^BODY>DIV:nth-child(3)>H1:nth-child(4)>SPAN:nth-child(1)


- **For running a function in the execution loop**

.. code-block:: python

    from autobrowser import utility
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    settings = dict()
    settings["repeat_feature"] = utility.FunctionRunner.REPEAT_SEQ
    settings["repeat_delay"] = 10

    wd = webdriver.Firefox()

    def foo():
        wd.get("http://google.com")

        # you can use the css_location retrieved from the autobrowser Probe in the css selector
        elem = wd.find_element_by_css_selector("BODY>DIV:nth-child(1)>DIV:nth-child(5)>FORM:nth-child(3)>DIV:nth-child(2)>DIV:nth-child(2)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(1)>DIV:nth-child(2)>DIV:nth-child(1)>INPUT:nth-child(1)")

        elem.send_keys("cricket")
        elem.send_keys(Keys.RETURN)

    utility.FunctionRunner(foo, settings = settings).start()


License
-------

The MIT License

Copyright (c) 2014 Sagar Nilesh Shah

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


Contribute
----------

