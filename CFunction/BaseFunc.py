# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
import psys.Info as pinf

def sigmoid(x):
    y = 1/(1 + np.exp(-x))
    return y


def _draw_sigmoid():
    x = np.linspace(-20, 20, 1000)
    y = sigmoid(x)
    plt.plot(x, y)
    return plt


def list_not_shorter_than(list1, length):
    """
    判断list1的长度大于len
    :param list1:
    :param len:
    :return:
    """
    assert (len(list1) >= length) is True, pinf.CError('list is shorter than %d' % length)
    return True
    pass