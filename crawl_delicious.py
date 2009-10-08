
import cPickle
import urllib

import simplejson

BOSS = "http://boss.yahooapis.com/ysearch/web/v1/%s?appid=DfNrQ3bV34H_Ll3bncrHNjWL6z_1K_1xX8UIfpugGKdPGTZ_CkCJjNq8FxTLlvI-&abstract=long&view=delicious_toptags&start=%d&count=50"

def cleans(text):
  tokens = [t.lower() for t in text.split()]
  weights = {}
  for t in tokens:
    ht = abs(hash(t))
    if ht in weights:
      weights[ht] += 1
    else:
      weights[ht] = 1

  top = sorted(weights.iteritems(), key=lambda p: p[1], reverse=True)
  weights = dict(top[:24])
  denom = float( sum(weights.itervalues()) )
  for ht in weights:
    weights[ht] = weights[ht] / denom
  return weights

vector_data = []

for q in open("tags.txt", "r"):
  for offset in [0, 50, 100, 150]:
    req = BOSS % (q.strip(), offset)
    resp = urllib.urlopen(req).read()
    data = simplejson.loads(resp)
    for r in data["ysearchresponse"]["resultset_web"]:
      text = r["title"] + " " + r["abstract"]
      vector = cleans(text)
      tt = r["delicious_toptags"]
      if len(tt) > 0:
        tags = tt["tags"]
        for t in tags:
          name = t["name"].lower()
          vector_data.append( (vector, name) )

cPickle.dump(vector_data, open("vector_data.cpickle", "w"))
