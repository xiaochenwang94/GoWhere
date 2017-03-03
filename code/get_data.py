import foursquare
client_id = 'KX1FBBNOJQ00KMIFG3DKCZMQZGIWEGPHHHGHUHKNKF4J1SQE'
client_secret = '1YUQX32MGD0FOPEHGMSRNXGJ0LOBXJNBJ3HYVH4IGHGVTRSB'

client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret,redirect_uri='http://localhost:9000')
access_token = client.oauth.get_token('')
client.set_access_token(access_token)
user = client.users()
print(user)