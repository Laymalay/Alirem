#!/usr/bin/python
# -*- encoding: utf-8 -*-
#python -m unittest test
import unittest
import subprocess
from os.path import join, exists, basename
from os import mkdir, makedirs
from alirem.remove import RemoveHandler
import alirem.logger as log
from alirem.logger import DefaultLogger

class TestRemoveToBasket(unittest.TestCase):
    testbead_path = "testbead"
    basket = join(testbead_path, "basket")
    empty_dir_path = join(testbead_path, "empty_dir")
    file_path = join(testbead_path, "file")
    dir_path = join(testbead_path, "dir")
    # logger = log.Logger(mode_for_file='info', mode_for_cmd='info',
    #                     path='test', is_silent=False, is_force=False)
    logger = DefaultLogger()
    def setUp(self):
        mkdir(self.testbead_path)
        mkdir(self.empty_dir_path)
        open(self.file_path, 'w')
        makedirs(self.dir_path+"/dir2"+"/dir3")

    def test_run_remove_empty_dir_to_basket(self):
        handler_empty_dir = RemoveHandler(is_dir=True, is_basket=True,
                                          basket_path=self.basket, logger=self.logger)
        handler_empty_dir.remove(self.empty_dir_path)
        self.assertEqual(exists(self.empty_dir_path), False)
        self.assertTrue(exists(join(self.basket, basename(self.empty_dir_path))))
    def test_run_remove_dir_to_basket(self):
        handler_dir = RemoveHandler(is_recursive=True, is_basket=True,
                                    basket_path=self.basket, logger=self.logger)
        handler_dir.remove(self.dir_path)
        self.assertEqual(exists(self.dir_path), False)
        self.assertTrue(exists(join(self.basket, basename(self.dir_path))))
    def test_run_remove_file_to_basket(self):
        handler_file = RemoveHandler(logger=self.logger, is_basket=True, basket_path=self.basket,)
        handler_file.remove(self.file_path)
        self.assertEqual(exists(self.file_path), False)
        self.assertTrue(exists(join(self.basket, basename(self.file_path))))

    def tearDown(self):
        subprocess.call(["rm", "-rf", self.testbead_path])


if __name__ == '__main__':
    unittest.main()
