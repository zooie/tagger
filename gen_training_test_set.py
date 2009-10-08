
# Must have run python crawl_delicious.py or have vector_data.cpickle before this

# Usage:
#  python gen_training_test_split.py [tag1] [tag2]

#  tag1, tag2 must be tags listed in tags.txt

# Creates two files: training_data.txt test_data.txt
# 1 label corresponds to tag1, -1 for tag2

import cPickle
import random
import sys

tag1 = sys.argv[1].lower()
tag2 = sys.argv[2].lower()

outputs = {tag1: 1, tag2: -1}

tr = cPickle.load(open("vector_data.cpickle", "r"))

selected = []
for vector, tag in tr:
  if tag in outputs:
    selected.append( (outputs[tag], vector) )

random.shuffle(selected)
split = int(len(selected) * 0.80)

def format_features(vector):
  return " ".join(["%d:%f" % (k, v) for k, v in sorted(vector.iteritems())])

training_file = open("training_data.txt", "w")

for tag, vector in selected[:split]:
  training_file.write("%d %s\n" % (tag, format_features(vector)))

test_file = open("test_data.txt", "w")

for tag, vector in selected[split:]:
  test_file.write("%d %s\n" % (tag, format_features(vector)))

training_file.close()
test_file.close()
