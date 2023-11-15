import urllib.parse
import sys

json = sys.argv[1]

json_query = urllib.parse.quote(json)
print(json_query)