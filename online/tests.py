# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from skmultilearn.dataset import load_dataset
from skmultilearn.problem_transform import BinaryRelevance as BRl
from sklearn.svm import SVC
import sklearn.metrics as M

X_train, Y_train, feature_names, label_names = load_dataset('emotions', 'train')
X_test, Y_test, _, _ = load_dataset('emotions', 'test')

print('X_train       is {}'.format(X_train))
print('Y_train       is {}'.format(Y_train))
print('feature_names is {}'.format(feature_names))
print('label_names   is {}'.format(label_names ))