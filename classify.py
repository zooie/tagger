
# Usage
#  python classify.py [tag1] [tag2] some free text

# 'some free text' actually needs to be quite a bit
# (about an abstract's size) to be more accurate

# This does the training from scratch each time

import os
import sys
import time

import conf
import featurize

tag1 = sys.argv[1].lower()
tag2 = sys.argv[2].lower()
text = " ".join(sys.argv[3:])

os.popen("python gen_training_test_set.py %s %s" % (tag1, tag2)).read()

cmd = os.popen("python autosvm.py training_data.txt test_data.txt")
output = cmd.read()
dir = output[output.rfind(":") + 1:].strip()

vector = featurize.vectorize(text)
line = featurize.format_features(vector)

f = dir + "%f.classify" % time.time()
open(f, "w").write(line)

os.popen(conf.LIBSVM_DIR + "svm-predict %s %s %s" % (f, dir + "model", f + ".predict")).read()
if open(f + ".predict", "r").read().split()[0] == "-1":
  print tag2
else:
  print tag1
