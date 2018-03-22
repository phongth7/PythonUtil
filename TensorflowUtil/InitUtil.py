# coding = utf-8
import tensorflow as tf
import sys
import psys.Info as Util
"""
本程序提供各种权值初始化方式，初始化可训练参数
按照初始化方式，默认添加到GraphKeys.GLOBAL_VARIABLES
同时如果不指定collection，还会添加到'TRAINABLED'
如果指定collection，则会添加到该collection
同时输出添加的信息
"""

def bias_init(
        name='undefined',
        method='zero',
        output_channel=None,
        collection='TRAINABLED'
):
         assert method in ['zero', 'one'], print('method not support')
         if method == 'zero':
                  b = tf.get_variable(
                           name=name + '_bias',
                           shape=[output_channel],
                           dtype=tf.float32,
                           initializer=tf.zeros_initializer()
                  )
         elif method == 'one':
                  b = tf.get_variable(
                           name=name + '_bias',
                           shape=[output_channel],
                           dtype=tf.float32,
                           initializer=tf.ones_initializer()
                  )
         else:
                  sys.exit()
         Util.AddToCollectionInfo(tf.GraphKeys.GLOBAL_VARIABLES, b)
         tf.add_to_collection(collection, b)
         Util.AddToCollectionInfo(collection, b)
         return  b
         pass


def weight_init(
        name='undefined',
        method='msra',
        height=None,
        width=None,
        input_channel=None,
        output_channel=None,
        collection='TRAINABLED'
):

         assert method in ['msra'], print('mothod not support')
         if method == 'msra':
                  initer = tf.contrib.layer.variance_scaling_initializer(
                           factor=2.0,
                           model='FAN_IN',
                           uniform=False
                  )
         # elif:
         #          sys.exit()
         else:
                  sys.exit()

         w = tf.get_variable(
                  name=name + '_weight',
                  shape=[height, width,
                         input_channel, output_channel],
                  dtype=tf.float32,
                  initializer=initer
         )
         Util.AddToCollectionInfo(tf.GraphKeys.GLOBAL_VARIABLES, w)
         tf.add_to_collection(collection, w)
         Util.AddToCollectionInfo(collection, w)
         return w