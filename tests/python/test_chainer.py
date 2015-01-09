# vim: ts=8 sts=4 expandtab autoindent

"""
  Copyright (c) 2014 Péter Vörös

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation
  files (the "Software"), to deal in the Software without
  restriction, including without limitation the rights to use, copy,
  modify, merge, publish, distribute, sublicense, and/or sell copies
  of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.
"""

from Zorp.Core import *
from Zorp.Zorp import quit
from traceback import *
from Zorp.SockAddr import SockAddrInet, SockAddrInet6
from Zorp.Chainer import SourceIPBasedChainer, LeastConnectionChainer
import Zorp.Matcher
import unittest

config.options.kzorp_enabled = FALSE

class MockOwner(object):
    def __init__(self, client_address):
        self.client_address = client_address

class MockSession(object):
    def __init__(self, client_address, target_address):
        self.owner = MockOwner(client_address)
        self.target_address = target_address
        self.target_local = "local"


class SourceIPTestIPv4(unittest.TestCase):
    def setUp(self):
        self.target_addresses = [SockAddrInet('1.1.1.1', 1111), SockAddrInet('2.2.2.2', 2222), SockAddrInet('3.3.3.3', 3333)]
        self.chainer = SourceIPBasedChainer()

    def test_same_hashing(self):
        session = MockSession(SockAddrInet("1.2.3.4", 80), self.target_addresses)
        for i in range(100):
            (target_local, target_remote) = self.chainer.getNextTarget(session)
            self.assertEqual(target_local, "local")
            self.assertEqual(target_remote, self.target_addresses[1])

    def test_different_hashing(self):
        for i in range(4):
            session = MockSession(SockAddrInet("1.2.3.%i" % i, 80), self.target_addresses)
            (target_local, target_remote) = self.chainer.getNextTarget(session)
            self.assertEqual(target_local, "local")
            self.assertEqual(target_remote, self.target_addresses[i % len(self.target_addresses)])

class SourceIPTestIPv6(unittest.TestCase):
    def setUp(self):
        self.target_addresses = [SockAddrInet('1.1.1.1', 1111), SockAddrInet('2.2.2.2', 2222), SockAddrInet('3.3.3.3', 3333)]
        self.chainer = SourceIPBasedChainer()

    def test_same_hashing(self):
        session = MockSession(SockAddrInet6("ff::", 80), self.target_addresses)
        for i in range(100):
            (target_local, target_remote) = self.chainer.getNextTarget(session)
            self.assertEqual(target_local, "local")
            self.assertEqual(target_remote, self.target_addresses[0])

    def test_different_hashing(self):
        for i in range(4):
            session = MockSession(SockAddrInet6("ff::%i" % i, 80), self.target_addresses)
            (target_local, target_remote) = self.chainer.getNextTarget(session)
            self.assertEqual(target_local, "local")
            self.assertEqual(target_remote, self.target_addresses[i % len(self.target_addresses)])

class LeastConnections(unittest.TestCase):
    def setUp(self):
        self.target_addresses = [SockAddrInet('1.1.1.1', 1111), SockAddrInet('2.2.2.2', 2222), SockAddrInet('3.3.3.3', 3333)]
        self.chainer = LeastConnectionChainer()

    def MockZorpCTLSzig_first_least(self, target_addresses, selected_index):
	return selected_index

    def MockZorpCTLSzig_all_same(self, target_addresses, selected_index):
	return 1

    def MockZorpCTLSzig_second_least(self, target_addresses, selected_index):
	if selected_index == 1:
	    return 0
	else:
	    return 1

    def MockZorpCTLSzig_last_least(self, target_addresses, selected_index):
	return len(target_addresses)-selected_index

    def test_first_server_has_least_conn(self):
	session = MockSession(SockAddrInet("1.2.3.4", 80), self.target_addresses)
	(target_local, target_remote) = self.chainer.getNextTarget(session, self.MockZorpCTLSzig_first_least)
        self.assertEqual(target_local, "local")
        self.assertEqual(target_remote, self.target_addresses[0])

    def test_all_server_has_same_conn(self):
	session = MockSession(SockAddrInet("1.2.3.4", 80), self.target_addresses)
	(target_local, target_remote) = self.chainer.getNextTarget(session, self.MockZorpCTLSzig_all_same)
        self.assertEqual(target_local, "local")
        self.assertEqual(target_remote, self.target_addresses[0])

    def test_second_server_has_least_conn(self):
	session = MockSession(SockAddrInet("1.2.3.4", 80), self.target_addresses)
	(target_local, target_remote) = self.chainer.getNextTarget(session, self.MockZorpCTLSzig_second_least)
        self.assertEqual(target_local, "local")
        self.assertEqual(target_remote, self.target_addresses[1])

    def test_last_server_has_least_conn(self):
	session = MockSession(SockAddrInet("1.2.3.4", 80), self.target_addresses)
	(target_local, target_remote) = self.chainer.getNextTarget(session, self.MockZorpCTLSzig_last_least)
        self.assertEqual(target_local, "local")
        self.assertEqual(target_remote, self.target_addresses[2])


def init(name, virtual_name, is_master):
    unittest.main(argv=('/',))

# Local Variables:
# mode: python
# indent-tabs-mode: nil
# python-indent: 4
# End:
