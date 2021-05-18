import requests


request = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
ditto_pydict = request.json()
print(ditto_pydict)