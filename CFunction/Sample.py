# coding = utf-8

import random
import CFunction.BaseFunc as CBF
import psys.Info as pinf
import math
import copy

# tested
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

# tested
def n_devide(input_list, part, except_list=[]):
    """
    对input_list进行part等分， 除去except_list索引之外，返回索引表
    :param input_list:输入的list
    :param part:
    :param except_list:不参与分割的索引
    :return:返回分割的索引，因此上层需要保留input_list才能获得正确的数据
    """
    assert float(len(input_list) - len(except_list)) / part >= 1.0, \
        pinf.CError('len of input_list : %d seperate part : %d, cannot be possible' % (len(input_list  ), part))
    target_list = list(range(0, len(input_list)))
    [target_list.remove(i) for i in except_list]
    sample_amount = math.ceil(len(target_list) / part)
    residue_amount = sample_amount * part - len(target_list)
    gather = list()
    for i in range(0, part - 1):
        sample = random.sample(target_list, sample_amount)
        if i < residue_amount:
            del_sample = random.sample(sample, 1)
            gather.append(copy.deepcopy(sample))
            sample.remove(del_sample[0])
        else:
            del_sample = []
            gather.append(copy.deepcopy(sample))
        [target_list.remove(j) for j in sample]
        pass
    gather.append(target_list)
    return gather
    pass

# tested
def n_devide_return_target_data(input_list, part, except_list=[]):
    indexes = n_devide(input_list, part, except_list)
    gather = list()
    for i in indexes:
        gather.append([input_list[j] for j in i])
    return gather
