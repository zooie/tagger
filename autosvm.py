
# A quick script that simplifies libsvm's interface and autotunes key parameters
# Resulting model and prediction files stored in new local dir named by creation timestamp

# Usage:
#   python autosvm.py [training_data_filename] [test_data_filename]

import itertools
import os
import sys
import time

LIBSVM_DIR = "libsvm-2.89/"

# Setup temporary files for training and predictions

DIR = str(time.time()) + "/"
os.mkdir(DIR)

tr = sys.argv[1]
trm = DIR + tr.replace("/", "_") + ".model"

ts = sys.argv[2]
tp = DIR + ts.replace("/", "_") + ".predict"


def parse_accuracy(resp):
  return float(resp[resp.rfind("=") + 1:].strip()[:-1])
  
def cross_validate(c, g):
  resp = os.popen(LIBSVM_DIR + "svm-train -c %f -g %f -v 5 -m 400 %s %s" % (c, g, tr, trm)).read()
  return parse_accuracy(resp)

def finalize(c, g):
  os.popen(LIBSVM_DIR + "svm-train -c %f -g %f -m 400 %s %s" % (c, g, tr, trm)).read()

def brute_train():
  """ Exhaust & select the c, g values that result in the most accurate model during cross validation """
  best_c = None
  best_g = None
  best_accuracy = -1

  for c_exp in (-5, 5):
    cost = float(2 ** c_exp)
    for g_exp in (-5, 5):
      gamma = float(2 ** g_exp)
      accuracy = cross_validate(cost, gamma)
      if accuracy > best_accuracy:
        best_c = cost
        best_g = gamma
        best_accuracy = accuracy
        print "____Trained A Better Model:", accuracy

  finalize(best_c, best_g)


print "__Searching / Training Best Model"

brute_train()

print "__Predicting Test Data"

os.popen(LIBSVM_DIR + "svm-predict %s %s %s" % (ts, trm, tp)).read()

print "__Evaluation"

right = 0
total = 0
for tsl, tpl in itertools.izip(open(ts, "r"), open(tp, "r")):
  a = tsl.split()[0]
  b = tpl.split()[0]
  if a == b:
    right += 1
  total += 1

print "____Right: %d" % right
print "____Wrong: %d" % (total - right)
print "____Total: %d" % total
print "____Accuracy: %f" % (right / float(total))
