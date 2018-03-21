# coding = ut f-8

import numpy as np
import util.Util as cutil
import evaluate.CIoU as ciou


class Yolo2Util:
    def __init__(self, image_shape, number_class, cluster_number, scalar, prior_shape):
        """
        
        :param image_shape:输入图像的形状[width, height]
        :param number_class:目标检测类别数+1
        :param cluster_number:先验框数量
        :param scalar:yolo2特征提取尺度，论文采用的32x32
        :param prior_shape:聚类获得的先验框的宽高[[w, h], [w, h], ...]
        """
        self.ImageShape = image_shape
        self.NumberClass = number_class
        self.ClusterNumber = cluster_number
        self.PriorShape = prior_shape
        self.Scalar = scalar
        self.CoordinateLabelData = None
        self.ClassLabelData = None
        self.Check = \
            (np.array(self.ImageShape, np.float64) / self.Scalar * 10
             - np.array(self.ImageShape, np.float64) / self.Scalar)
        assert ((self.Check[0] != 0.0) & (self.Check[1] != 0.0)) is True, \
            cutil.CError('image shape is %s, scalar is %s' % (self.ImageShape, self.Scalar))
        self.Check = np.array(self.ImageShape, np.int64) / self.Scalar
        pass

    def _set_label_data(self, coordinate_data, classes_data):
        """
        :param coordinate_data:shape=[obj_num, 4],[[x, y, w, h], ...]
        :param classes_data:shape=[obj_num],[class, ...]
        :return:
        """
        self.CoordinateLabelData = coordinate_data
        self.ClassLabelData = classes_data
        pass

    def _abandon_or_not(self, x_y):
        """
        先验box超出图像的部分，不进行采用，原因：label与数据变得无关，反而会使回归混乱
        :param x_y:单个样本真实的x, y 坐标:[x, y]
        :return:bool_list:对于一系列prior box建议采用的判断：true采用， false不采用
        """
        [x_conformity, y_conformity] = np.array(x_y) - np.array(x_y) % np.float64(self.Scalar)
        [min_x_in_image, min_y_in_image] = np.min(
            np.array(
                [[x_conformity, self.ImageShape[0] - x_conformity],
                 [y_conformity, self.ImageShape[1] - y_conformity]]),
            axis=1)
        flag = np.ceil(np.array(self.PriorShape) / 2.0) < np.array([min_x_in_image, min_y_in_image])
        flag = flag[:, 0] & flag[:, 1]
        return list(flag)
        pass

    def _generate_coordinate_x_y(self,  x_y):
        """

        :param x_y:真值box的中心坐标，shape=[2], [x, y] list
        :return:返回X, Y, X_Shift, Y_Shift: 上采样之后位置[X, Y]为coordinate输出位置， [X_shift,Y_Shift]:论文中提到的偏移量
        """
        [X, Y] = np.array(np.array(x_y) / self.Scalar, np.int64)
        shift = np.array(x_y) % self.Scalar
        [X_Shift, Y_Shift] = shift / np.float64(self.Scalar)
        return X, Y, X_Shift, Y_Shift
        pass

    def _generate_coordinate_w_h(self, prior_w_h, w_h):
        """

        :param prior_w_h:先验box的宽与高，shape=[2], [width, height] list
        :param w_h:真值box的宽与高，shape=[2], [width, height] list
        :return:输出偏移量, shape=[2], [width_shift, height_shift], list
        """
        w_h_shift = np.log(np.array(prior_w_h, np.float64) / np.array(w_h, np.float64))
        return list(w_h_shift)
        pass

    def _generate_coordinate_confidence(self, pre_coordinate, coordinate):
        """
        
        :param pre_coordinate:预测的坐标四元组， shape=[4], [pre_x_shift, pre_y_shift, pre_w_shift, pre_h_shift] 
        :param coordinate: 真实的坐标四元组， shape=[4], [x_shift, y_shift, w_shift, h_shift]
        :return: 
        """
        p = [self.Scalar * pre_coordinate[1],
             self.Scalar *pre_coordinate[0],
             pre_coordinate[3],
             pre_coordinate[2]]
        t = [self.Scalar * coordinate[1],
             self.Scalar * coordinate[0],
             self.PriorShape[0] * np.exp(coordinate[3]),
             self.PriorShape[0] * np.exp(coordinate[2])]
        iou = ciou.calc_IoU(predicted_coordinate=p, true_coordinate=t)
        if iou is None:
            return 0
        else:
            return iou
        pass

    def _argv_to_label(self, argv_list):
        """
        通过参数列表生成label tensor
        :param argv_list: 参数列表，{'0': 
        [
        {indexes': [indexes_x, indexes_y], 
        'x_y_shift': [x_shift, y_shift], 
        'w_h_shift': [[w_shift, h_shift], ...],
        'pre_truth_IoU': [ , , ...],
        'class': 
        }, ...},
         dict 有多组先验w 与 h 需要有多组w_h_shift
        :return: 返回label tensor：[H, W, C]
        """
        LabelCoordinateArray = np.zeros([self.Check[1], self.Check[0], self.ClusterNumber * 5], np.float64)
        LabelClassesArray = np.zeros([self.Check[1], self.Check[0], self.ClusterNumber * self.NumberClass], np.float64)
        LabelMaskObjArray = np.zeros([self.Check[1], self.Check[0]], np.float64)
        LabelMaskNoobjArray = np.ones([self.Check[1], self.Check[0]], np.float64)
        for i in list(argv_list.keys()):
            cla = [0.0] * self.NumberClass
            cla[argv_list[i]['class']] = 1.0
            y = argv_list[i]['indexes'][1]
            x = argv_list[i]['indexes'][0]
            x_shift = argv_list[i]['x_y_shift'][0]
            y_shift = argv_list[i]['x_y_shift'][1]
            for j in range(0, self.ClusterNumber):
                w_shift = argv_list[i]['w_h_shift'][j][0]
                h_shift = argv_list[i]['w_h_shift'][j][1]
                iou = argv_list[i]['pre_truth_IoU'][j]
                LabelCoordinateArray[y, x, j * 5: (j + 1) * 5] = [x_shift, y_shift, w_shift, h_shift, iou]
            LabelClassesArray[y, x] = cla * self.ClusterNumber
            LabelMaskObjArray[y, x] = 1.0
            LabelMaskNoobjArray[y, x] = 0.0
        return {'coordinate': LabelCoordinateArray,
                'class': LabelClassesArray,
                'obj': LabelMaskObjArray,
                'no_obj': LabelMaskNoobjArray}
        pass

    def _check_info(self, coordinate_data, classes_data, pre_coordinate):
        """
        检查info是否符合要求， 被label_data_to_label调用
        :param coordinate_data: 
        :param classes_data: 
        :param pre_coordinate: 
        :return: 
        """
        obj_num = len(coordinate_data)
        # 判别同等obj数量
        assert (len(classes_data) == obj_num & len(pre_coordinate) == obj_num) is True
        assert (False not in [len(i) == 4 for i in coordinate_data]) is True
        assert (False not in [len(i) == 1 for i in classes_data]) is True
        assert (False not in len(i) == self.ClusterNumber for i in pre_coordinate) is True
        for i in pre_coordinate:
            assert (False not in len(j) == 4 for j in i) is True
        return True
        pass

    def label_data_to_label(self, coordinate_data, classes_data, pre_coordinate):
        """
        预测了单张图像，可含有多个obj，建议不要有多个obj都在同一cell之中
        :param coordinate_data:真值坐标数据， shape=[obj_num, 4], [[x, y, w, h], ...], list
        :param classes_data:真值类别数据，shape=[obj_num], [[0], [1], ...],list， 0代表背景，
        顺序需要与coordinate_data相对应
        :param pre_coordinate:obj位置预测生成的坐标数据，shape=[obj_num, cluster_num, 4]
        [[[pre_x_shift, pre_y_shift, pre_w_shift, pre_h_shift], ...], ...]
        :return:
        """
        if type(coordinate_data).__name__ == 'ndarray':
            coordinate_data = np.ndarray.tolist(coordinate_data)
        if type(classes_data).__name__ == 'ndarray':
            classes_data = np.ndarray.tolist(classes_data)
        if type(pre_coordinate).__name__ == 'ndarray':
            pre_coordinate = np.ndarray.tolist(pre_coordinate)
        assert self._check_info(coordinate_data, classes_data, pre_coordinate) is True
        argv_dict = dict()
        for i in range(0, len(coordinate_data)):
            indexes_x, indexes_y, x_shift, y_shift = \
                self._generate_coordinate_x_y([coordinate_data[i][0], coordinate_data[i][1]])
            argv_dict[i] = dict()
            argv_dict[i]['indexes'] = [indexes_x, indexes_y]
            argv_dict[i]['x_y_shift'] = [x_shift, y_shift]
            w_h_shift = list()
            pre_truth_IoU = list()
            for j in range(0, len(self.PriorShape)):
                w_shift, h_shift = \
                    self._generate_coordinate_w_h(
                        self.PriorShape[j], [coordinate_data[j][2], coordinate_data[j][3]])
                t_confidence = \
                    self._generate_coordinate_confidence(
                        pre_coordinate[i][j],
                        [x_shift, y_shift, w_shift, h_shift])
                w_h_shift.append([w_shift, h_shift])
                pre_truth_IoU.append(t_confidence)
            argv_dict[i]['w_h_shift'] = w_h_shift
            argv_dict[i]['pre_truth_IoU'] = pre_truth_IoU
            argv_dict[i]['class'] = classes_data
        Label = self._argv_to_label(argv_list=argv_dict)
        pass
    pass
