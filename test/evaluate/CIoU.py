# coding = utf-8

import evaluate.CIoU as Ciou
import psys.Info as Cinfo

def test_calc_IoU():
    truth = [100, 100, 100, 100]
    predict = [50, 50, 100, 100]
    result = Ciou.calc_IoU(predicted_coordinate=predict, true_coordinate=truth)
    Cinfo.CKeyInfo('truth: %s, predict: %s, IoU: %f' % (truth, predict, result))


if __name__ == '__main__':
    test_calc_IoU()
