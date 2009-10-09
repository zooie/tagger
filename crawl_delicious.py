
import cPickle
import urllib

import simplejson

import featurize

BOSS = "http://boss.yahooapis.com/ysearch/web/v1/%s?appid=DfNrQ3bV34H_Ll3bncrHNjWL6z_1K_1xX8UIfpugGKdPGTZ_CkCJjNq8FxTLlvI-&abstract=long&view=delicious_toptags&start=%d&count=50"

vector_data = []

for q in open("tags.txt", "r"):
  for o in xrange(0, 5):
    offset = o * 50
    req = BOSS % (q.strip(), offset)
    resp = urllib.urlopen(req).read()
    data = simplejson.loads(resp)
    if "resultset_web" not in data["ysearchresponse"]:
      continue
    for r in data["ysearchresponse"]["resultset_web"]:
      text = r["title"] + " " + r["abstract"]
      vector = featurize.vectorize(text)
      tt = r["delicious_toptags"]
      if len(tt) > 0:
        tags = tt["tags"]
        for t in tags:
          name = t["name"].lower()
          vector_data.append( (vector, name) )

cPickle.dump(vector_data, open("vector_data.cpickle", "w"))
