# coding = utf-8

import csv

import psys.Info as pinf

CountModelDefault = 'Default'
CountModelRejectNoneEnd = 'RejectNoneEnd'
CountModelRejetNoneMiddle = 'RejetNoneMiddle'


# tested
def count_csv_file_row(csv_file, model=CountModelDefault):
    """
    计算csv文件的行数，提供三种模式：CountModelDefault：完全计算csv文件
    CountModelRejectNoneEnd 除去为[]的结尾端，进行计算行数
    CountModelRejetNoneMiddle 除去所有[]进行计算行数
    :param csv_file: 
    :param model: 
    :return: 
    """
    assert model in [CountModelDefault, CountModelRejectNoneEnd, CountModelRejetNoneMiddle], \
        pinf.CError('model : %s not supported' % model)
    with open(csv_file) as fp:
        read = csv.reader(fp)
        if model == CountModelDefault:
            i = 0
            for raw in read:
                i += 1
            return i
        elif model == CountModelRejectNoneEnd:
            i = 0
            attribute = list()
            for raw in read:
                if raw == []:
                    attribute.append(0)
                else:
                    attribute.append(1)
                i += 1
            for raw in attribute[::-1]:
                if raw == 0:
                    i -= 1
                else:
                    return i
            return i
            pass
        elif model == CountModelRejetNoneMiddle:
            i = 0
            for raw in read:
                if raw == []:
                    pass
                else:
                    i += 1
                    pass
                pass
            return i
    pass