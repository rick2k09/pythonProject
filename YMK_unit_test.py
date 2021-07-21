import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("/Users/hyde/pythonProject/venv/lib/site-packages")
import unittest
from appium import webdriver
import json
import time
from htmltestrunner import HTMLTestRunner
# import HTMLReport
# import test_SendReport

ip = "http://192.168.0.206:8000/config.json"

class MyTestCase(unittest.TestCase):
    # Input Device setting
    def setUp(self):
        with open('desired_capabilities.json') as json_file:
            desired_caps = json.load(json_file)
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
        self.driver.implicitly_wait(3)

    # Go to Secrect page
    def test_goto_secretpage(self):
        self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/bc_me_icon").click()
        self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/bc_top_bar_left_btn").click()
        while True:
            try:
                self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/aboutBtn").click()
                break
            except:
                self.driver.swipe(400, 1000, 400, 300, 400)
        for x in range(5):
            self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/launcherTestSettingBtn").click()
        while True:
            try:
                self.driver.find_element_by_xpath("//*[contains(@text, 'Apply effect test')]").click()
                break
            except:
                self.driver.swipe(400, 1000, 400, 300, 400)
        self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/resetButton").click()
        self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/testJsonUrlEditText").send_keys(ip)
        self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/startButton").click()

        # Image Upload
        start = time.time()  # 記錄開始套圖上傳的時間
        image_int = 0
        while image_int == 0: # try until images start upload
            image_count = self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/imageCountTextView").text  # 抓出圖片數量
            image_int = int(image_count)  # 算出case id 的個數
        all_case_id = self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/testIdsTextView").text  # 抓出case id
        case_id = all_case_id.split(",")  # 把all case id 變成一個list
        case_count = len(case_id)  # 算出case id 的個數
        progress_number = str(case_count * image_int)  # 算出總共有幾張圖片跑 (幾個case x 幾張圖片)，轉換成string
        finished = self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/progressTextView").text  # 抓出prgoress 的字串
        while (finished != progress_number + "/" + progress_number):  # prgoress 如果不等於progress_number/progress_number
            finished = self.driver.find_element_by_id("com.cyberlink.youcammakeup:id/progressTextView").text  # 再抓一次prgoress 的字串，直到prgoress 等於progress_number/progress_number，表示圖片已全部上傳完成
        end = time.time()  # 記錄完成上傳的時間
        print("finish upload time: %s (s)" %(end - start))

    # Close APP when test done
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    # unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestSuite()
    test1 = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    test2 = unittest.defaultTestLoader.discover('./', pattern='test_ImageCompare.py')
    # suite.addTests([test1, test2])
    suite.addTests(test2)

    timestr = time.strftime('%Y%m%d', time.localtime(time.time()))  # 本地日期作為報告名字
    filename = '/testreport/'  # 文件名字及保存路徑
    fp = open(filename + (timestr + '.html'), 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Result', description='Test Report： ')
    # runner = HTMLReport.TestRunner(title='Test Result', description='Test Report： ')
    runner.run(suite)
    fp.close()
    # test_SendReport.send(filename, timestr)
