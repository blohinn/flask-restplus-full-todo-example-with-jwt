import jwt
encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')

print(encoded.decode('utf-8'))
# print(encoded)
# decoded = jwt.decode(encoded, 'secret', algorithms=['HS256'])
# print(decoded)
sdf = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lZSI6InBheWxvYWQifQ.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
print(jwt.decode(sdf, 'secret'))