# coding = utf-8

import random
import CFunction.BaseFunc as CBF

def sample_except(input_list, sample_amount, except_list=[]):
    """
    输入一个列表与想要忽略的成员索引位置
    :param input_list:输入采样对象，数据安全
    :param except_list:输入忽略的成员的索引， 数据安全
    :return:采样到的样本的索引位置
    """
    CBF.list_not_shorter_than(input_list, sample_amount + len(except_list))
    CBF.list_not_shorter_than(input_list, max(except_list))
    target_list = list(range(0, len(input_list)))
    [target_list.remove(i) for i in except_list]
    target = random.sample(target_list, sample_amount)
    return target
    pass