# coding = utf-8
import CFunction.CsvFile as Ccsv
import csv
import psys.Info as pinf


def test_count_csv_file_row():
    file = './Data/CsvFile-test_count_csv_file_row.csv'
    with open(file, 'w', newline='') as fp:
        writer = csv.writer(fp)
        for i in range(0, 22):
            if i == 10:
                writer.writerow([])
            elif i == 21:
                writer.writerow([])
            else:
                writer.writerow(['a'])
        fp.close()
    return_inf = list()
    try:
        assert Ccsv.count_csv_file_row(file, Ccsv.CountModelDefault) == 22
        return_inf.append(True)
    except AssertionError:
        return_inf.append(False)
    try:
        assert Ccsv.count_csv_file_row(file, Ccsv.CountModelRejectNoneEnd) == 21
        return_inf.append(True)
    except:
        return_inf.append(False)
    try:
        assert Ccsv.count_csv_file_row(file, Ccsv.CountModelRejetNoneMiddle) == 20
        return_inf.append(True)
    except AssertionError:
        return_inf.append(False)
    return return_inf
    pass

def test_check_no_empty_between_two_significative_data():
    file = './Data/CsvFile-check_no_empty_between_two_significative_data-False.csv'
    file2 = './Data/CsvFile-check_no_empty_between_two_significative_data-True.csv'
    with open(file, 'w', newline='') as fp:
        writer = csv.writer(fp)
        for i in range(0, 22):
            if i == 10:
                writer.writerow([])
            elif i == 21:
                writer.writerow([])
            else:
                writer.writerow(['a'])
        fp.close()
    with open(file2, 'w', newline='') as fp:
        writer = csv.writer(fp)
        for i in range(0, 22):
            if i == 0:
                writer.writerow([])
            elif i == 21:
                writer.writerow([])
            else:
                writer.writerow(['a'])
        fp.close()
    flag = [
        Ccsv.check_no_empty_between_two_significative_data(file),
        Ccsv.check_no_empty_between_two_significative_data(file2)
    ]
    return flag
    pass

if __name__ == '__main__':
    pinf.CKeyInfo('-----------------------testing count_csv_file_row-------------------------')
    return_inf = test_count_csv_file_row()
    if return_inf[0] is True:
        pinf.CKeyInfo('OK: test_count_csv_file_row, model %s successed' % Ccsv.CountModelDefault)
    else:
        pinf.CError('FAILED: test_count_csv_file_row, model %s failed' % Ccsv.CountModelDefault)
    if return_inf[1] is True:
        pinf.CKeyInfo('OK: test_count_csv_file_row, model %s successed' % Ccsv.CountModelRejectNoneEnd)
    else:
        pinf.CError('FAILED: test_count_csv_file_row, model %s failed' % Ccsv.CountModelRejectNoneEnd)
    if return_inf[2] is True:
        pinf.CKeyInfo('OK: test_count_csv_file_row, model %s successed' % Ccsv.CountModelRejetNoneMiddle)
    else:
        pinf.CError('FAILED: test_count_csv_file_row, model %s failed' % Ccsv.CountModelRejetNoneMiddle)
    pinf.CKeyInfo('-------------------testing check_no_empty_between_two_significative_data---------------------')
    return_inf = test_check_no_empty_between_two_significative_data()
    if return_inf[0] is False:
        pinf.CError('OK: test_check_no_empty_between_two_significative_data in negative successed')
    else:
        pinf.CKeyInfo('FAILED: test_check_no_empty_between_two_significative_data in negative failed')
    if return_inf[1] is True:
        pinf.CError('OK: test_check_no_empty_between_two_significative_data in positive successed')
    else:
        pinf.CKeyInfo('FAILED: test_check_no_empty_between_two_significative_data in positive failed')