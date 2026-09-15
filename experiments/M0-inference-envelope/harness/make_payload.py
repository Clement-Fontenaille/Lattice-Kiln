import json
import sys

text = open("/tmp/longprompt.txt").read()
payload = {"prompt": text, "n_predict": 64}
open(sys.argv[1], "w").write(json.dumps(payload))
