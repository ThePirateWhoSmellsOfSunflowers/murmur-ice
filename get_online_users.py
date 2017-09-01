#!/usr/bin/env python
# -*- coding: utf-8

# ThePirateWhoSmellsOfSunflowers - https://github.com/ThePirateWhoSmellsOfSunflowers

import Ice
import sys

iceslice = "/usr/share/Ice/slice/Murmur.ice"
iceincludepath = "/usr/share/Ice/slice"
icehost = "127.0.0.1"
iceport = 6502
icesecret = "SheSellsSeashellsOnTheSeeShore"
messagesizemax = "65535"

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

try:
    meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy("Meta:tcp -h %s -p %s" % (icehost, iceport)))
except Ice.ConnectionRefusedException:
    print 'Could not connect'
    ice.shutdown()
    sys.exit(1)

try:
    server=meta.getServer(1)
except Murmur.InvalidSecretException:
    print 'Ice password is wrong.'
    ice.shutdown()
    sys.exit(1)

#Get users
onlineusers = server.getUsers()

if len(onlineusers) == 0:
    print "No user connected"
    sys.exit(0)

print "Users list :"
for key in onlineusers.keys():
    print "\t" + onlineusers[key].name + (" (Mute)" if onlineusers[key].selfMute == True else "")

ice.shutdown()

