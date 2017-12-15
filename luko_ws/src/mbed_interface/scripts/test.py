import sys
import json

flags = [int(i) for i in sys.argv[1:]]

print json.loads(str(flags))
