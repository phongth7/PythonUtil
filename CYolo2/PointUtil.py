# coding = utf-8
import numpy as np
import psys.Info as Cinf

class Point:
    def __init__(self, image_shape, scalar, point_num, num_class, visiable_exist=True, point_unify=False):
        """
        
        :param image_shape: 图像的[height, width]
        :param scalar: 下采样的尺度[height, width]
        :param point_num: 点的数量
        :param num_class: 点的类别数
        :param visiable_exist: 是否有可见性该属性的存在
        :param point_unify: 是否每个对象的点都是统一的，即每个对象都拥有全体点的合集的点，
                如A对象拥有A类点而不拥有B类点，B对象拥有B类点而不拥有A类点，此为point not unify
        """
        self.ImageShape = image_shape
        self.Scalar = scalar
        self.PointNum = point_num
        self.ClassNum = num_class
        self.VisibleExit = visiable_exist
        self.PointUnify = point_unify
        self.FeatureShape = list(np.array(self.ImageShape) / 32.0)
        assert False not in [(int(i) - i) == 0.0 for i in self.FeatureShape], \
                Cinf.CError('Image shape is not the integral multiple of 32 : %d' % (self.ImageShape))
        if visiable_exist is True:
            if point_unify is False:
                # 如果有可见性与点性质不统一的性质，则需要：[x_shift, y_shift, confidence, visiable, exit]
                self.FeatureShapeChannel = self.Scalar[0] * self.Scalar[1] * (self.ClassNum + 2 + 1 + 1 + 1)
            else:
                self.FeatureShapeChannel = self.Scalar[0] * self.Scalar[1] * (self.ClassNum + 2 + 1+ 1)
        else:
            if self.PointUnify is False:
                self.FeatureShapeChannel = self.Scalar[0] * self.Scalar[1] * (self.ClassNum + 2 + 1 + 1)
            else:
                self.FeatureShapeChannel = self.Scalar[0] * self.Scalar[1] * (self.ClassNum + 2 + 1)
        self.FeatureOutputShape = self.FeatureShape.append(self.FeatureShapeChannel)
        pass

    def _calc_indexe_by_y_x_indexe(self, y, x):
        """
        通过y，x索引计算label中哪个位置进行label设定，默认输出的排列为先x，再y
        :param y:y索引，可以输入list ndarray 或者单指
        :param x:x索引， 可以输入list ndarray 或者单指
        :return: 
        """
        assert type(y).__name__ in ['list', 'int', 'ndarray'], \
            Cinf.CError('y has the unlawful type : %s' % (type(y).__name__))
        assert type(x).__name__ in ['list', 'int', 'ndarray'], \
            Cinf.CError('x has the unlawful type : %s ' % (type(x).__name__))
        assert len(list(y)) == len(list(x)), \
            Cinf.CError('y must has the same length with x, y: %s, x: %s' % (len(list(y)), len(list(x))))
        if type(y).__name__ == 'list':
            y = np.array(x)
        if type(x).__name__ == 'list':
            x = np.array(x)
        return (x * self.Scalar[1] + y % self.Scalar) * 2 - 1
        pass

    def _generate_shift(self, point):
        """
        产生点偏移的label
        :param point: 点集， shape=[N, 2], [[x, y], ...]
        :return: 
        """
        assert len(point) <= self.PointNum, \
            Cinf.CError('Point number is larger then the stipulated number %d' % (len(point)))
        indexes = np.trunc(np.array(point) / 32)
        indexes_in_indexes = np.trunc((np.array(point) % 32 ) * 10)
        shift = np.array(point) - np.trunc(np.array(point))
        x_y_shift = np.zeros(
            shape=[
                self.FeatureShape.append(
                    self.Scalar[0] * self.Scalar[1] * 2)])
        x_y_shift[
            indexes[1, :],
            indexes[0, :],
            self._calc_indexe_by_y_x_indexe(indexes_in_indexes[0, :], indexes_in_indexes[1, :])] = shift[0]
        x_y_shift[
            indexes[1, :],
            indexes[0, :],
            self._calc_indexe_by_y_x_indexe(indexes_in_indexes[0, :], indexes_in_indexes[1, :])] = shift[1]
        pass

    def _generate_conf(self):
        pass

    def _generate_visible(self):
        pass

    def _generate_class(self):
        pass
