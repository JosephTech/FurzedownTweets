import ConfigParser
config = ConfigParser.ConfigParser()
config.read('lastid.ini')
lastid = config.get('DEFAULT','LastID')
print lastid
lastid = 999999
config.set('DEFAULT', 'LastID', lastid)

with open('lastid.ini', 'wb') as configfile:
	config.write(configfile)
#config['DEFAULT']['LastID'] = 999999

#with open('lastid.ini', 'w') as configfile:
#	config.write(configfile)
