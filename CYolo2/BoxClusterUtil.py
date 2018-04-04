# coding = utf-8
import sklearn
import psys.Info as pI
import numpy as np


class BoxCluster:
    """
    BoxCluster: for the technology in the yolo2
    in yolo2 , in order to reduce the difficulty of regression on boxdetection ，
    it make the prior anchor box approach to the ground truth, using anchor box[h, w] cluster
    to get the more reasonable prior box anchor
    在yolo2中，为了减少box坐标回归的难度，使用了聚类算法，对坐标的h，w进行聚类
    """
    """
    in this class we deal with the normal cluster use different clustering algorithm
    and evaluate each of them in every class of object
    at the same time , we calculate the distribution of anchor box in every class
    使用不同的聚类算法，进行每个聚类算法中的不同目标类别的评价
    """
    def __init__(self, class_amount, gt_anchor_box):
        """
        
        :param class_amount: the number of class in all dataset
        :param gt_anchor_box: a dict constant box anchor(ground truth) information,format:
                {'class_name':[[center_y, center_x, height, width], ...],...}
                
                center is use to calculate the performance of the cluster, according to we 
                tacitly approve the prior center is at the point[top,left] in the cell,take 
                 a look at : https://pjreddie.com/darknet/yolo/
        """
        self.ClassAmount = class_amount
        self.GT_AnchorBox = gt_anchor_box
        self.SupportClusterAlgorithm = ['k-means']
        pass

    def _kmeans_cluster(self):
        pass

    def cluster(self, method='k-means'):
        assert method in self.SupportClusterAlgorithm, \
            pI.CError('cluster algorithm : %s is not support\n' % method)
        class_key = list(self.GT_AnchorBox.get_keys())
        data = np.array([self.GT_AnchorBox[i][2: ] for i in class_key])

        pass

    def evaluate(self):
        pass