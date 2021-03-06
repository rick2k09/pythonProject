import unittest
import time
from htmltestrunner import HTMLTestRunner
from YMK_unit_test import MyTestCase
import shutil
import os

if __name__ == '__main__':
    source = 'testreport/'
    destination = '/Users/hyde/unittest_server/YMK_unit_test/testreport_backup/'
    files = os.listdir(source)
    for f in files:
        if not f.startswith('.') and os.path.isfile(os.path.join(source, f)):
            new_path = shutil.copyfile(f"{source}/{f}", f"{destination}/{f}")
            print('copy file to:' + new_path)
            for d in files:
                os.remove(source + d)
                print('delete file:' + d)
    # unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestSuite()
    test1 = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    test2 = unittest.defaultTestLoader.discover('./', pattern='test_ImageCompare.py')
    suite.addTests([test1, test2])
    # suite.addTests(test2)

    timestr = time.strftime('%Y%m%d', time.localtime(time.time()))  # 本地日期作為報告名字
    filename = 'testreport/'  # 文件名字及保存路徑
    fp = open(filename + (timestr + '.html'), 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Result', description='Test Report： ')
    # runner = HTMLReport.TestRunner(title='Test Result', description='Test Report： ')
    runner.run(suite)
    fp.close()
    # test_SendReport.send(filename, timestr)
