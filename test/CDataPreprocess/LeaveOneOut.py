# coding = utf-8
import CDataPreprocess.LeaveOneOut as LOO
import json

def test_csv_features_seperated():
    a = LOO.LeaveOneOut()
    a.csv_features_seperated(
        ['./data/test_LeaveOneOut.csv', './data/test_LeaveOneOut2.csv'],
        rate=0.3,
        unique_identification=0,
        out_put_file_path='./data/test_csv_features_seperated.json',
        ignore_indexes=[0])
    pass

def test_csv_reader_features_seperated():
    a = LOO.LeaveOneOut()
    indexes = a.csv_reader_features_seperated('./data/test_csv_features_seperated.json')
    with open('./data/test_csv_features_seperated_read_inf.json', 'w') as fp:
        fp.write(json.dumps(indexes, indent=4))
        fp.close()
    pass


if __name__ == '__main__':
    test_csv_features_seperated()
    test_csv_reader_features_seperated()