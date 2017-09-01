#!/usr/bin/env python
# -*- coding: utf-8

# ThePirateWhoSmellsOfSunflowers - https://github.com/ThePirateWhoSmellsOfSunflowers

from flask import Flask, jsonify
import Ice

app = Flask(__name__)
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

#
# Route
#

@app.route('/users')
def get_users():
    
    users = []
    
    # Connection 
    try:
        meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy("Meta:tcp -h %s -p %s" % (icehost, iceport)))
        server=meta.getServer(1)
    except Exception as e:
        ice.shutdown()
        return jsonify({'error' : str(e)})

    # Users
    onlineusers = server.getUsers()
    for key in onlineusers.keys():
        users.append({'name' : onlineusers[key].name, 'selfMute' : onlineusers[key].selfMute})
    ice.shutdown()
    
    return jsonify({'users' : users})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)

