# Wrapper for SUDS to provide HTTPS client authentication for the SUDS SOAP library
# Modified from http://www.threepillarglobal.com/soap_client_auth
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

import httplib
import urllib2

from suds.transport.http import HttpTransport
from suds.client import Client
from suds.options import Options
from suds.properties import Unskin

def getClient(url, key, cert):
    transport = HttpClientAuthTransport(key, cert, timeout=60)
    return Client(url, transport = transport)

# SUDS Client Auth solution
# Modified by Liam Friel (liam.friel@s3group.co): use of kwargs directly
class HttpClientAuthTransport(HttpTransport):
    def __init__(self, key, cert, **kwargs):
        HttpTransport.__init__(self, **kwargs)
        self.urlopener = urllib2.build_opener(HTTPSClientAuthHandler(key, cert))
        
#HTTPS Client Auth solution for urllib2, inspired by
# http://bugs.python.org/issue3466
# and improved by David Norton of Three Pillar Software. In this
# implementation, we use properties passed in rather than static module
# fields.
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert
        
    def https_open(self, req):
        #Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)
    
    def getConnection(self, host):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)