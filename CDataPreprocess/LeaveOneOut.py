# coding = utf-8
import csv
import random
import json
import sys

import CFunction.Sample as CFS
import psys.Info as pinf
import CFunction.CsvFile as Ccsv

class LeaveOneOut:
    def __init__(self):
        self.Type = str()
        self.File = list()
        self.CsvFeaturesSeperated = 'csv_features_seperated'
        self.CsvItemSeperated = 'csv_item_seperated'
        pass

    # tested
    def csv_features_seperated(
            self,
            file_list_full_path,
            rate,
            unique_identification,
            out_put_file_path,
            type='speed',
            ignore_indexes=[]):
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
        :param ignore_indexes:针对csv文件需要忽略行的索引
        :return:
        """
        pinf.CKeyInfo(
            'all file path: %s\n'
            'sample rate: %f\n'
            'unique identification: %d\n'
            'output file path: %s\n'
            'ignore indexes: %s' %
            (file_list_full_path, rate,
             unique_identification,
             out_put_file_path,
             ignore_indexes))
        info = dict()
        part_num = round(1 / rate)
        info['k-part'] = part_num
        info['config_file_format'] = self.CsvFeaturesSeperated
        info['ignore_indexes'] = ignore_indexes
        if type == 'speed':
            key_info = dict()
            for i in file_list_full_path:
                reader = csv.reader(open(i, 'r'))
                # 取标识列信息，存到字典key_info中，该文件的绝对路径作为键值
                key_info[i] = [row[unique_identification] for row in reader]
            assert self._check_same_length(key_info) is True, \
                pinf.CError('not all csv file has the same number of data')
            info['sample_amount'] = len(key_info[file_list_full_path[0]])
            # part_num次留一法，每个留一法验证集互斥
            index = CFS.n_devide(
                key_info[file_list_full_path[0]],
                part=part_num,
                except_list=ignore_indexes)
            for i in range(0, part_num):
                info[i] = dict()
                info[i][file_list_full_path[0]] = index[i]
                for j in file_list_full_path[1: ]:
                    l = [key_info[j].index(key_info[file_list_full_path[0]][k]) for k in index[i]]
                    info[i][j] = l
                    pass
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
        js = json.dumps(info, indent=4)
        fs.write(js)
        fs.close()
        pass
    #   tested
    def csv_reader_features_seperated(self, config_file):
        f = open(config_file, 'r')
        inf = json.load(f)
        assert inf['config_file_format'] == self.CsvFeaturesSeperated, \
            pinf.CError('config file is not %s format' % self.CsvFeaturesSeperated)
        all = range(0, inf['sample_amount'])
        indexes = dict()
        indexes['file_queue'] = list(inf['0'].keys())
        for i in range(0, inf['k-part']):
            indexes[i] = dict()
            indexes[i]['eval'] = [inf[str(i)][j] for j in indexes['file_queue']]
            indexes[i]['train'] = [inf[str(i)][j] for j in indexes['file_queue']]
        return indexes
        pass

    # tested
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
                assert type(dict_input[i]).__name__ == 'list', 'content is not all list'
            except AssertionError:
                return False
        len_init = len(dict_input[keys[0]])
        for i in keys:
            try:
                assert len_init == len(dict_input[i]), 'not all the same length'
            except AssertionError:
                return False
        return True

    def csv_item_seperated(
            self,
            file_list_full_path,
            rate,
            out_put_file_path,
            ignore_indexes=[]):
        """
        针对使用csv存储大量数据，总数据被分为几个文件，每个文件存储一定量的数据集，本程序要求每个数据文件中不能
        不能再两个数据文件中穿插空数据行，但可以在两端最后又空行
        :param file_list_full_path: 文件列表[]
        :param rate: 留一比率,float
        :param out_put_file_path: 信息输出文件路径， str
        :param ignore_indexes: 无效行，每个文件需要有自己的无效行[[], [], ...]
        :return: 
        """
        info = dict()
        info['k-part'] = round(1 / rate)
        info['config_file_format'] = self.CsvItemSeperated
        info['ignore_indexes'] = ignore_indexes
        info['source_file_queue'] = file_list_full_path
        info['source_file_data_amount'] = dict()
        pinf.CKeyInfo(
            'all file path: %s\n'
            'sample rate: %f\n'
            'output file path: %s\n'
            'ignore indexes: %s' %
            (file_list_full_path, rate,
             out_put_file_path,
             ignore_indexes))
        assert False not in [Ccsv.check_no_empty_between_two_significative_data(i) for i in file_list_full_path]
        for i in file_list_full_path:
            info['source_file_data_amount'][i] = Ccsv.count_csv_file_row(i)
        total_amount = sum([info['source_file_data_amount'][i] for i in file_list_full_path])
        ignore_list = list()
        begin = 0
        for i in range(0, len(file_list_full_path)):
            append_list = [j + begin for j in ignore_indexes[i]]
            ignore_list += append_list
            begin += info['source_file_data_amount'][file_list_full_path[i]]
        gather = CFS.n_devide(list(range(0, total_amount)), info['k-part'], ignore_list)
        for i in range(0, info['k-part']):
            info[i] = gather[i]
        fs = open(out_put_file_path, 'w')
        js = json.dumps(info, indent=4)
        fs.write(js)
        fs.close()
        pass

