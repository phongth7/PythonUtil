# coding = utf-8

def calc_IoU(predicted_coordinate, true_coordinate):
    """
    
    :param predicted_coordinate: 预测的坐标，shape=[4], [y, x, h, w]
    :param true_coordinate: 真实的坐标，shape=[4], [y, x, h, w]
    :return: 
    """
    t_min_y, t_max_y, t_min_x, t_max_x = \
        [true_coordinate[0] - 0.5 * true_coordinate[2],
         true_coordinate[0] + 0.5 * true_coordinate[2],
         true_coordinate[1] - 0.5 * true_coordinate[3],
         true_coordinate[1] + 0.5 * true_coordinate[3]]
    p_min_y, p_max_y, p_min_x, p_max_x = \
        [predicted_coordinate[0] - 0.5 * predicted_coordinate[2],
         predicted_coordinate[0] + 0.5 * predicted_coordinate[2],
         predicted_coordinate[1] - 0.5 * predicted_coordinate[3],
         predicted_coordinate[1] + 0.5 * predicted_coordinate[3]]
    if (abs(true_coordinate[0] - predicted_coordinate[0]) < 0.5 * (predicted_coordinate[2] + true_coordinate[2]) and
                abs(true_coordinate[1] - predicted_coordinate[1]) < 0.5 * (predicted_coordinate[3] + true_coordinate[3])):
        y_up = max(t_min_y, p_min_y)
        y_bottom = min(t_max_y, p_max_y)
        x_left = max(t_min_x, p_min_x)
        x_right = min(t_max_x, p_max_x)

        overlap_area = (y_bottom - y_up) * (x_right - x_left)
        return overlap_area
    else:
        return None
    pass
