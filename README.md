# murmur-ice
Simple scripts to intereact with the mumble's ice API

## get_online_users.py
```
$ ./get_online_users.py
Users list :
	J4CK (Mute)
	Titi
	Mfw_dude
```


## chat_with_online_users.py 
```
$ ./chat_with_online_users.py 
<You> hi!
<Titi> : yo
<J4CK> : sup ?
```
## rest_api_murmur.py
PoC to wrap Mumble API with flask, because Ice su***

implemented route :

* `http://example.com:5000/users` : return in JSON connected users, with mute status (`selfMute`)
