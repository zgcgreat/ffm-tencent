# -*- encoding:utf-8 -*-
import collections
from csv import DictReader
from datetime import datetime

train_path = '../data_ori/train.csv'
test_path = '../data_ori/test.csv'
train_ffm = '../output/train.ffm'
test_ffm = '../output/test.ffm'


field = ['clickTime', 'creativeID', 'userID', 'positionID', 'connectionType', 'telecomsOperator']

table = collections.defaultdict(lambda: 0)


# 为特征名建立编号, filed
def field_index(x):
    index = field.index(x)
    return index

# 为特征值建立编号
def getIndices(key):
    indices = table.get(key)
    if indices is None:
        indices = len(table)
        table[key] = indices
    return indices


feature_indices = set()
with open(train_ffm, 'w') as fo:
    for e, row in enumerate(DictReader(open(train_path))):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + ':' + v
                    features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
                    feature_indices.add(kv + '\t' + str(getIndices(kv)))
        if e % 100000 == 0:
            print(datetime.now(), 'creating train.ffm...', e)
        fo.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))

with open(test_ffm, 'w') as fo:
    for t, row in enumerate(DictReader(open(test_path))):
        features = []
        for k, v in row.items():
            if k in field:
                if len(v) > 0:
                    idx = field_index(k)
                    kv = k + ':' + v
                    if kv + '\t' + str(getIndices(kv)) in feature_indices:
                        features.append('{0}:{1}:1'.format(idx, getIndices(kv)))
        if t % 100000 == 0:
            print(datetime.now(), 'creating validation data and test.ffm...', t)
        fo.write('{0} {1}\n'.format(row['label'], ' '.join('{0}'.format(val) for val in features)))
fo.close()

