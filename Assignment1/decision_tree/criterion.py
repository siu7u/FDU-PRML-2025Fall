"""
criterion
"""
import math

def get_criterion_function(criterion):
    if criterion == "info_gain":
        return __info_gain
    elif criterion == "info_gain_ratio":
        return __info_gain_ratio
    elif criterion == "gini":
        return __gini_index
    elif criterion == "error_rate":
        return __error_rate


def __label_stat(y, l_y, r_y):
    """Count the number of labels of nodes"""
    left_labels = {}
    right_labels = {}
    all_labels = {}
    for t in y.reshape(-1):
        if t not in all_labels:
            all_labels[t] = 0
        all_labels[t] += 1
    for t in l_y.reshape(-1):
        if t not in left_labels:
            left_labels[t] = 0
        left_labels[t] += 1
    for t in r_y.reshape(-1):
        if t not in right_labels:
            right_labels[t] = 0
        right_labels[t] += 1

    return all_labels, left_labels, right_labels


def _entropy(y):
    ent = 0.0
    times = 0
    for key in y:
        times += y[key]

    if times == 0:
        return 0

    for key in y:
        p = y[key] / times
        ent -= p * math.log2(p)

    return ent


def __info_gain(y, l_y, r_y):
    """
    Calculate the info gain

    y, l_y, r_y: label array of father node, left child node, right child node
    """
    all_labels, left_labels, right_labels = __label_stat(y, l_y, r_y)
    info_gain = 0.0
    ###########################################################################
    # TODO:                                                                   #
    # Implement this method. Calculate the info gain if splitting y into      #
    # l_y and r_y                                                             #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    l_times = 0
    r_times = 0
    all_times = 0
    for key in all_labels:
        all_times += all_labels[key]

    for key in left_labels:
        l_times += left_labels[key]

    for key in right_labels:
        r_times += right_labels[key]

    parent_ent = _entropy(all_labels)
    left_ent = _entropy(left_labels)
    right_ent = _entropy(right_labels)

    info_gain = parent_ent
    info_gain -= left_ent * (l_times / all_times)
    info_gain -= right_ent * (r_times / all_times)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return info_gain


def __info_gain_ratio(y, l_y, r_y):
    """
    Calculate the info gain ratio

    y, l_y, r_y: label array of father node, left child node, right child node
    """
    info_gain = __info_gain(y, l_y, r_y)
    all_labels, left_labels, right_labels = __label_stat(y, l_y, r_y)
    ###########################################################################
    # TODO:                                                                   #
    # Implement this method. Calculate the info gain ratio if splitting y     #
    # into l_y and r_y                                                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    split_info = 0.0

    n = n_l = n_r = 0
    for key in all_labels:
        n += all_labels[key]

    for key in left_labels:
        n_l += left_labels[key]

    for key in right_labels:
        n_r += right_labels[key]

    p_l = n_l / n
    p_r = n_r / n

    # print(p_r,p_l)

    if p_l > 0 :
        split_info -= p_l * math.log2(p_l)

    if p_r > 0:
        split_info -= p_r * math.log2(p_r)

    if split_info ==0:
        return 0
    else:
        info_gain /= split_info

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    return info_gain


def _gini(labels):
    """辅助函数：计算一个节点的基尼指数"""
    n = sum(labels.values())
    if n == 0:
        return 0

    gi = 1.0
    for count in labels.values():
        p = count / n
        gi -= p ** 2
    return gi


def __gini_index(y, l_y, r_y):
    """
    Calculate the gini index

    y, l_y, r_y: label array of father node, left child node, right child node
    """
    all_labels, left_labels, right_labels = __label_stat(y, l_y, r_y)
    before = 0.0
    after = 0.0

    ###########################################################################
    # TODO:                                                                   #
    # Implement this method. Calculate the gini index value before and        #
    # after splitting y into l_y and r_y                                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    n = n_l = n_r = 0
    for key in all_labels:
        n += all_labels[key]

    for key in left_labels:
        n_l += left_labels[key]

    for key in right_labels:
        n_r += right_labels[key]

    p_l = n_l / n
    p_r = n_r / n

    before = _gini(all_labels)
    after = p_l * _gini(left_labels) + p_r * _gini(right_labels)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    return before - after

def _err(label):
    n = sum(label.values())
    if n == 0:
        return 0

    max_t = 0
    for key in label:
        if label[key] > max_t:
            max_t = label[key]

    return 1-max_t/n


def __error_rate(y, l_y, r_y):
    """Calculate the error rate"""
    all_labels, left_labels, right_labels = __label_stat(y, l_y, r_y)
    before = 0.0
    after = 0.0

    ###########################################################################
    # TODO:                                                                   #
    # Implement this method. Calculate the error rate value before and        #
    # after splitting y into l_y and r_y                                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****


    n = n_l = n_r = 0
    for key in all_labels:
        n += all_labels[key]

    for key in left_labels:
        n_l += left_labels[key]

    for key in right_labels:
        n_r += right_labels[key]

    p_l = n_l / n
    p_r = n_r / n

    before = _err(all_labels)
    after = p_l * _err(left_labels) + p_r * _err(right_labels)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    return before - after
