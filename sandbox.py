import gzip
import json

path = "data/de_rus.gz"
data = []
with gzip.open(path, "rt", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 3:
            data.append(json.loads(line))
            
        
