
# Very simple feature setup here ...

def ht(term):
  return abs(hash(term))

def norm(d):
  denom = float( sum(d.itervalues()) )
  for ht in d:
    d[ht] = d[ht] / denom
  return d

def remove_tag(tag, d):
  h = ht(tag)
  if h in d:
    del d[h]
  return norm(d)

def vectorize(text):
  tokens = [t.lower() for t in text.split()]
  weights = {}
  for t in tokens:
    h = ht(t)
    if h in weights:
      weights[h] += 1
    else:
      weights[h] = 1

  top = sorted(weights.iteritems(), key=lambda p: p[1], reverse=True)
  weights = dict(top[:24])
  return norm(weights)

def format_features(vector):
  return " ".join(["%d:%f" % (k, v) for k, v in sorted(vector.iteritems())])
