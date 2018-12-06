#!/usr/bin/env python
import zeep
from zeep import Client
from zeep.plugins import HistoryPlugin
from zeep import xsd

LDB_TOKEN = ''
WSDL = 'http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

if LDB_TOKEN == '':
    raise Exception(
        "Please configure your OpenLDBWS token in getDepartureBoardExample!")

history = HistoryPlugin()

client = Client(wsdl=WSDL, plugins=[history])

header = xsd.Element(
    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
    xsd.ComplexType([
        xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
            xsd.String()),
    ])
)
header_value = header(TokenValue=LDB_TOKEN)
tlc = input("Enter your station's three letter code: ")

res = client.service.GetDepartureBoard(
    numRows=10, crs=tlc, _soapheaders=[header_value])

print("Trains at " + res.locationName)
print("===============================================================================")

services = res.trainServices.service

i = 0
while i < len(services):
    t2 = services[i]
    print(t2.std + " to " +
          t2.destination.location[0].locationName + " - " + t2.etd)
    i += 1
