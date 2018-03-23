# coding = utf-8
import tensorflow as tf
import TensorflowUtil.InitUtil as init
import tensorflow.contrib.keras as keras
import psys.Info as Util
import sys

def Conv_Layer(
        name='undefined',
        input=None,
        height=None,
        width=None,
        output_channel=None
):
         conv = tf.nn.conv2d(
                  input=input,
                  filter=init.weight_init(
                           name=name,
                           height=height,
                           width=width,
                           input_channel=input.get_shape().as_list()[-1],
                           output_channel=output_channel,
                      collection='ConvWeight'
                  ),
                  strides=[1, 1, 1, 1],
                  padding='SAME',
                  name=name
         )
         tf.add_to_collection(name='ConvOut', value=conv)
         Util.AddToCollectionInfo('ConvOut', conv)
         Util.CLayerInfo(name, input, conv)
         return conv
         pass
def Bias_Layer(
        name='undefined',
        input=None,

):
         """
         默认格式'NHWC'
         :param name:
         :param input:
         :return:
         """
         bias = tf.nn.bias_add(
                  value=input,
                  bias=init.bias_init(
                           name=name,
                           output_channel=input.get_shape().as_list()[-1],
                      collection='BiasBias'
                  ),
                  data_format='NHWC',
                  name=name
         )
         tf.add_to_collection(name='BiasOut', value=bias)
         Util.AddToCollectionInfo('BiasOut', bias)
         Util.CLayerInfo(name, input, bias)
         return bias
         pass

def Activate_Layer(
        name='undefined',
        input=None,
        method='LeakReLU'
):
         """
         默认格式'NHWC'
         :param name:
         :param input:
         :param method:
         :return:
         """
         assert method in ['LeakReLU', 'ReLU'], Util.CError('method is not supported')
         if method == 'LeakReLU':
                  activate = keras.layers.LeakyReLU(
                           alpha=0.1,
                           name=name + 'LeakReLU'
                  )(input)
         elif method == 'ReLU':
             activate = keras.layers.ReL

         else:
                  Util.CError('method is not supported!')
                  sys.exit()
         tf.add_to_collection(name='ActiOut', value=activate)
         Util.CLayerInfo(name, input, activate)
         Util.AddToCollectionInfo('ActiOut', activate)
         return activate
         pass

def BatchNormal_Layer(
        name='undefined',
        input=None,
        train=tf.bool(True),
):
         """
         默认格式'NHWC'
         :param input:
         :return:
         """
         global MOVING_DECAY
         global BNEPS
         assert Util.CGlobalExit('MOVING_DECAY')
         assert Util.CGlobalExit('BNEPS')
         train_mean = tf.reduce_mean(
                  input_tensor=input,
                  axis=3,
                  name=name + '_t_mean',
         )

         train_var = tf.reduce_mean(
                  tf.square(
                           x=tf.subtract(
                                    x=input,
                                    y=train_mean
                           )
                  ),
                  axis=[0, 1, 2]
         )

         beta = init.bias_init(
                  name=name + '_beta',
                  method='zero',
                  output_channel=input.get_shape().as_list()[-1],
             collection='BnBeta'
         )
         gama= init.bias_init(
                  name=name + '_gama',
                  method='one',
                  output_channel=input.get_shape().as_list()[-1],
             collection='BnGama'
         )
         ema = tf.train.ExponentialMovingAverage(MOVING_DECAY)

         predict_mean, predict_var = ema.apply([train_mean, train_var])

         def depend_in_train():
                  with tf.control_dependencies([predict_mean, predict_var]):
                           return tf.identity(train_mean), tf.identity(train_var)
                  pass
         mean, var = tf.cond(
                  train,
                  lambda: depend_in_train(),
                  lambda: (predict_mean, predict_var)
         )
         bn = tf.nn.batch_normalization(
                  x=input,
                  mean=mean,
                  variance=var,
                  offset=beta,
                  scale=gama,
                  variance_epsilon=BNEPS
         )
         tf.add_to_collection(name='BnOut', value=bn)
         Util.AddToCollectionInfo('BnOut', bn)
         Util.CLayerInfo(name, input, bn)
         # bn = tf.add(
         #          x=beta,
         #          y=tf.div(
         #                   tf.multiply(
         #                            x=gama,
         #                            y=tf.subtract(
         #                                     x=input,
         #                                     y=mean
         #                            )
         #                   ),
         #                   y=var
         #          ),
         #          name=name + 'bn_output'
         # )
         return bn
         pass

def Pool_Layer(
        name='undefined',
        input=None,
        height=None,
        width=None,
        stride=None,
        method='MAX'
):
         assert method in ['max', 'global-avg'], Util.CError('method is not support!')

         if method == 'max':
                  tmp = tf.nn.pool(
                           input=input,
                           window_shape=[height, width],
                           pooling_type='MAX',
                           padding='SAME',
                           dilation_rate=None,
                           strides=stride,
                      name=name + '_max'
                  )
                  pass
         elif method == 'global-avg':
             tmp = tf.reduce_mean(
                 input_tensor=input,
                 axis=3,
                 name=name + '_global-avg'
             )
             pass
         else:
                  Util.CError('method is not support!')
                  sys.exit()
                  pass

         Util.CLayerInfo(name, input, tmp)
         return tmp
         pass
