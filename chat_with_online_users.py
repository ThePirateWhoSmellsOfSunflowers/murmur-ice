#!/usr/bin/env python
# -*- coding: utf-8

# ThePirateWhoSmellsOfSunflowers - https://github.com/ThePirateWhoSmellsOfSunflowers

import Ice
import sys

messagesizemax = "65535"
iceslice = "/usr/share/Ice/slice/Murmur.ice"
iceincludepath = "/usr/share/Ice/slice"
icehost = "127.0.0.1"
iceport = 6502
icesecret = "SheSellsSeashellsOnTheSeeShore"

Ice.loadSlice("--all -I%s %s" % (iceincludepath, iceslice))
props = Ice.createProperties([])
props.setProperty("Ice.MessageSizeMax", str(messagesizemax))
props.setProperty("Ice.ImplicitContext", "Shared")
props.setProperty("Ice.Default.EncodingVersion", "1.0")
id = Ice.InitializationData()
id.properties = props
ice = Ice.initialize(id)
ice.getImplicitContext().put("secret", icesecret)

import Murmur

class CallbacksMurmur(Murmur.ServerCallback):
    def __init__(self, server, adapter):
        self.server = server
        self.adapter = adapter

    def userTextMessage(self, user, msg, current=None):
        print "\r<%s> : %s" % (user.name,msg.text)
        
try:
    meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy("Meta:tcp -h %s -p %s" % (icehost, iceport)))
except Ice.ConnectionRefusedException:
    print 'Could not connect'
    ice.shutdown()
    sys.exit(1)

try:
    server=meta.getServer(1)
except Murmur.InvalidSecretException:
    print 'Wrong secret'
    ice.shutdown()
    sys.exit(1)

adapter = ice.createObjectAdapterWithEndpoints("Callback.Client", "tcp -h %s" % icehost)
adapter.activate()
callback = Murmur.ServerCallbackPrx.uncheckedCast(adapter.addWithUUID(CallbacksMurmur(server, adapter)))
server.addCallback(callback)

while True:
    try:
        sys.stdout.write('<You> ')
        message = sys.stdin.readline()
        sys.stdout.flush()
        server.sendMessageChannel(0,True,message)
    except KeyboardInterrupt:
        ice.shutdown()
        sys.exit(0)

ice.shutdown()

