import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("/Users/hyde/pythonProject/venv/lib/site-packages")
import unittest
from wand.image import Image
import time
import os

class CompareImages(unittest.TestCase):
    def test_compares(self):
        folder1 = '/Users/hyde/unittest_server/YMK_unit_test/base/'
        folder2 = '/Users/hyde/unittest_server/YMK_unit_test/upload/'
        resultfolder = '/Users/hyde/unittest_server/YMK_unit_test/test4results/'
        d1 = os.listdir(folder1)
        d2 = os.listdir(folder2)
        cropsize = 0.05
        current_time = time.time()
        files = list(set(d1) & set(d2))

        for i in files:
            if not i.startswith('.') and os.path.isfile(os.path.join(folder1, i)):
                with Image(filename=folder1 + i) as base:
                    with Image(filename=folder2 + i) as img:
                        # Crop left, top, right, bottom
                        base.crop(int(base.width*cropsize), int(base.height*cropsize), int(base.width*(1-cropsize)), int(base.height*(1-cropsize)))
                        img.crop(int(img.width*cropsize), int(img.height*cropsize), int(img.width*(1-cropsize)), int(img.height*(1-cropsize)))
                        # Compare
                        base.fuzz = base.quantum_range * 0.01  # Threshold of 1%
                        result_image, result_metric = base.compare(img, 'absolute')
                        # Save Difference
                        result_image.save(filename=resultfolder + i)
                        with self.subTest(msg=resultfolder+i, i=i, time=(time.time()-current_time)):
                            if result_metric == 0:
                                self.assertEqual(result_metric, 0)
                            else:
                                self.assertEqual(result_metric, 0, f'photo ({i}) is Fail')

        # print("Compare result ok, execution time = %s (s)" % (time.time() - current_time))

if __name__ == '__main__':
    unittest.main()
