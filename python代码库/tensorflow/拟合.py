import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np


x_data=np.random.rand(100).astype(np.float32)
y_data=x_data*0.1+0.3

#设置初始值
Weights=tf.Variable(tf.random_uniform([1],-1.0,1.0))
biases=tf.Variable(tf.zeros([1]))

y=Weights*x_data+biases

#提升y的准确度
loss=tf.reduce_mean(tf.square(y-y_data))

#优化器  减少误差
#学习效率
optimizer=tf.train.GradientDescentOptimizer(0.5)
train=optimizer.minimize(loss)

#初始化变量 活化
init = tf.initialize_all_variables()
#激活
sess=tf.Session()
sess.run(init)

#训练

for step in range(10000):
    sess.run(train)
    if step%20==0:
        print(step,sess.run(Weights),sess.run(biases))
