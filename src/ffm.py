# -*- encoding:utf-8 -*-
import subprocess
from datetime import datetime

NR_THREAD = 8

path = '../output/'

start = datetime.now()

# 训练
cmd = './ffm-train -l 0.00002 -k 8 -t 100 -r 0.02 -s {nr_thread} -p {save}test.ffm  {save}train.ffm ' \
      '{save}model'.format(nr_thread=NR_THREAD, save=path)
subprocess.call(cmd, shell=True)
# 预测
cmd = './ffm-predict {save}test.ffm {save}model {save}test.out'.format(save=path)
subprocess.call(cmd, shell=True)

with open(path + 'submission.csv', 'w') as fo:
    fo.write('instanceID,prob\n')
    for t, row in enumerate(open(path + 'test.out'), start=1):
        fo.write('{0},{1}'.format(t, row))

cmd = 'rm {path}model {path}test.out {path}train.ffm {path}test.ffm'.format(path=path)
subprocess.call(cmd, shell=True)

print('时间: {0}'.format(datetime.now() - start))
