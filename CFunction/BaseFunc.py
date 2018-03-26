# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    y = 1/(1 + np.exp(-x))
    return y


def _draw_sigmoid():
    x = np.linspace(-20, 20, 1000)
    y = sigmoid(x)
    plt.plot(x, y)
    return plt