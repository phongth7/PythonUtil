# coding = utf-8
import csv
import random
import json
import sys

import CFunction.Sample as CFS

class LeaveOneOut:
    def __init__(self):
        self.Type = str()
        self.File = list()
        pass

    def csv_features_seperated(
            self,
            file_list_full_path,
            rate,
            unique_identification,
            out_put_file_path,
            type='speed',
            ignore_range=[]):
        """
        针对样本的特征存储在多个文件中，但是这多个文件有对应的唯一标志，比如a特征存在a文件，b特征存在b文件，但是对于K样本，
        在两个文件中都有对应的第m列标志k在相同，同时对于其他样本又不同
        csv多文件留一数据预处理，要求file_list_full_path中的标记拥有同等数据量
        :param file_list_full_path:list 多个文件的列表，考虑到可能多种标记
        :param out_put_file_path:输出文件，依靠该文件，规范化读取数据
        :param unique_identification:json文件，考虑到不同csv文件中可能有不同的排序，我们通过标志列来进行数据安排
        :param rate:留一比率 , float
        :param type:主要考虑到，可能总的文件比较大，同时读取会爆内存，提供两种选择方式，
        一种是速度导向，吃内存"speed"，一种是内存导向，损速度"memory"
        :return:
        """
        if type == 'speed':
            info = dict()
            key_info = dict()
            part_num = round(1 / rate)
            for i in file_list_full_path:
                reader = csv.reader(open(i, 'r'))
                # 取标识列信息，存到字典key_info中，该文件的绝对路径作为键值
                key_info[i] = [row[unique_identification] for row in reader]
            assert self._check_same_length(key_info) is True, 'not all csv file has the same number of data'
            # part_num次留一法，每个留一法验证集互斥
            for i in range(0, part_num):
                index = CFS.sample_except(
                    key_info[unique_identification[0]],
                    sample_amount=int(rate * len(key_info[unique_identification[0]])),
                    except_list=ignore_range)
                info[i] = dict()
                info[i][file_list_full_path] = index
                for j in file_list_full_path[1: ]:
                    l = [key_info[j].index(key_info[file_list_full_path[j]][k]) for k in index]
                    info[i][j] = l
                    pass
        elif type == 'memory':
            print('this kind method is not complete!')
            sys.exit()
            pass
        else:
            print('illegal type')
            sys.exit()
            pass

        fs = open(out_put_file_path, 'w')
        js = json.dumps(info)
        fs.write(info)
        fs.close()
        pass

    def csv_reader(self):

        pass

    def _remove_ignore_element(self):
        """
        对csv.reader读取出来的
        :return:
        """
        pass

    def _check_same_length(self, dict_input):
        """
        比较字典中，每个的长度相同，要求：字典只是一级字典，且内容为列表
        :param dict_input: 输入的字典
        :return:
        """
        a = dict()
        keys = list(dict_input.keys())
        for i in keys:
            try:
                assert type(dict_input[i]).__str__ == 'list', 'content is not all list'
            except AssertionError:
                return False
        len_init = len(dict_input[keys])
        for i in keys:
            try:
                assert len_init == len(dict_input[i]), 'not all the same length'
            except AssertionError:
                return False
        return True


    def _random_select(self, list_input, rate):
        """
        以rate概率随机选择列表中的成员，删除选中的成员，返回选择到的成员的索引
        :param list_input:输入的list
        :param rate:概率。
        :return:
        """
        x = range(0, len(list))
        for i in x:
            del list_input[i]
        return random.sample(x, int(len(x) * rate))
        pass
