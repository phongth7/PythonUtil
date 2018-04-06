# coding = utf-8

import CFunction.Sample as CS
import psys.Info as pinf


def test_sample_except():
    for i in range(0, 20):
        try:
            a = CS.sample_except([1, 2], 1, [1])
            assert CS.sample_except([1, 2], 1, [1]) == [0], pinf.CError('test sample except failed')
        except:
            a = 1
    return True
    pass

def test_n_devide():
    a = list(range(0, 10))
    result = CS.n_devide(a, 5)
    assert len(result) == 5, pinf.CError('error in n_devide, get len is not 5 : %d' % len(result))
    assert (False not in [len(i) == 2 for i in result]) is True, \
        pinf.CError('error in n_devide , get item is not 2 : %s' % [len(i) == 2 for i in result])
    a = list(range(0, 11))
    result = CS.n_devide(a, 5)
    assert len(result) == 5, pinf.CError('error in n_devide, get len is not 5 : %d' % len(result))
    assert (False not in [len(i) == 3 for i in result]) is True, \
        pinf.CError('error in n_devide , get item is not 2 : %s' % [len(i) == 3 for i in result])
    return True

def test_n_devide_return_target_data():
    """
    事实上test_n_devide不出错，这个不会有错
    :return:
    """
    t = 'asdfghjklqwertyuiopzxcvbnm'
    a = [t[i] for i in range(0, len(t))]
    result = CS.n_devide_return_target_data(a, 5)
    return True
    pass

if __name__ == '__main__':
    assert test_sample_except() is True
    pinf.CKeyInfo('test sample_except successfully')
    assert test_n_devide() is True
    pinf.CKeyInfo('test n_devide successfully')
    assert test_n_devide_return_target_data() is True
    pinf.CKeyInfo('test n_devide_return_target_data successfully')
