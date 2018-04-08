# coding = utf-8
import CDataPreprocess.LeaveOneOut as LOO
import json
import psys.Info as pinf

def test_csv_features_seperated():
    a = LOO.LeaveOneOut()
    a.csv_features_seperated(
        ['./data/test_LeaveOneOut.csv', './data/test_LeaveOneOut2.csv'],
        rate=0.3,
        unique_identification=0,
        out_put_file_path='./data/test_csv_features_seperated.json',
        ignore_indexes=[0])
    a.csv_features_seperated(
        ['./data/test_LeaveOneOut.csv'],
        rate=0.3,
        unique_identification=0,
        out_put_file_path='./data/test_csv_features_seperated_only_1.json',
        ignore_indexes=[0]
    )
    pass

def test_csv_reader_features_seperated():
    a = LOO.LeaveOneOut()
    indexes = a.csv_reader_features_seperated('./data/test_csv_features_seperated.json')
    with open('./data/test_csv_features_seperated_read_inf.json', 'w') as fp:
        fp.write(json.dumps(indexes, indent=4))
        fp.close()
    return True
    pass

def test_csv_item_seperated():
    a = LOO.LeaveOneOut()
    indexes = a.csv_item_seperated(
        ['./data/test_LeaveOneOut-test_csv_item_seperated1.csv', './data/test_LeaveOneOut-test_csv_item_seperated2.csv'],
        rate = 0.1,
        out_put_file_path='./data/test_LeaveOneOut-test_csv_item_seperated.json',
        ignore_indexes=[[0, 1], [38]]
    )
    indexes = a.csv_item_seperated(
        ['./data/test_LeaveOneOut-test_csv_item_seperated1.csv'],
        rate=0.1,
        out_put_file_path='./data/test_LeaveOneOut-test_csv_item_seperated-only_one.json',
        ignore_indexes=[[0, 1]]
    )
    return True
    pass


if __name__ == '__main__':
    pinf.CKeyInfo('-------------testing csv_features_seperated--------------')
    test_csv_features_seperated()
    pinf.CKeyInfo('-------------testing csv_reader_features_seperated--------------')
    assert test_csv_reader_features_seperated() is True
    pinf.CKeyInfo('successed')
    pinf.CKeyInfo('-------------testing csv_item_seperated--------------')
    test_csv_item_seperated()
    pinf.CKeyInfo('successed')