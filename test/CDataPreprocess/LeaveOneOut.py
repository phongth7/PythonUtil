# coding = utf-8
import CDataPreprocess.LeaveOneOut as LOO

def test_csv_features_seperated():
    a = LOO.LeaveOneOut()
    a.csv_features_seperated(
        ['./data/test_LeaveOneOut.csv', './data/test_LeaveOneOut2.csv'],
        rate=0.1,
        unique_identification=0,
        out_put_file_path='./data/test_csv_features_seperated.json',
        ignore_indexes=[0])
    pass


if __name__ == '__main__':
    test_csv_features_seperated()