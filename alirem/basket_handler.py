#!/usr/bin/python
# -*- coding: UTF-8 -*-
import shutil
import os
from os import listdir, mkdir, access, makedirs
from os.path import join, exists, isfile, basename, isdir, dirname, islink
import logging
import datetime
import alirem.basket_list as basketlist
import alirem.exception as exception
import alirem.copy as copy

def create_basket(basket_path, logger):
    makedirs(basket_path)
    logger.log("Basket was created", logging.INFO)


class BasketHandler(object):
    def __init__(self, logger, path,
                 regexp=None, is_dir=False,
                 is_recursive=False,
                 basket_path='basket',
                 is_dryrun=False, is_interactive=False, symlinks=False, is_progress=True):
        self.basket_path = basket_path
        self.path = path
        self.is_dir = is_dir
        self.is_recursive = is_recursive
        self.logger = logger
        self.is_interactive = is_interactive
        self.is_dryrun = is_dryrun
        self.file_copied = True
        self.regexp = regexp
        self.symlinks = symlinks
        self.is_progress = is_progress

    def check_access_for_dir(self, path):
        if isdir(path):
            if os.access(path, os.R_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
                return True
            else:
                self.logger.log("Permission Denied: {}".format(path),
                                logging.ERROR, exception.PermissionDenied)
                return False
        else:
            return True

    # def create_basket(self):
    #     makedirs(self.basket_path)
    #     self.logger.log("Basket was created", logging.INFO)

    def move_to_basket(self):
        if not exists(self.basket_path):
            create_basket(basket_path=self.basket_path, logger=self.logger)
        if self.check_access_for_dir(self.path) and self.check_flags():
            basket_list = basketlist.BasketList(self.basket_path)
            basket_list.load()

            name = basename(self.path)
            new_name = self.check_in_basket(name, self.basket_path)
            dst = join(self.basket_path, new_name)

            copyhandler = copy.CopyHandler(logger=self.logger, is_merge=True,
                                           is_interactive=self.is_interactive,
                                           is_dryrun=self.is_dryrun,
                                           regexp=self.regexp, symlinks=self.symlinks,
                                           is_progress=self.is_progress)

            copyhandler.run(self.path, dst)


            basket_list.add(new_name,
                            os.path.abspath(self.path),
                            self.basket_path, join(self.basket_path, new_name),
                            datetime.datetime.now())
            basket_list.save()

    def check_in_basket(self, path, dst):
        path_check = join(dst, basename(path))

        if exists(path_check):
            index = 1
            while True:
                if not exists(path_check+'({})'.format(index)):
                    break
                index += 1
            new_name = path+'({})'.format(index)
        else:
            new_name = path

        return new_name

    def check_flags(self):
        if isdir(self.path) and not islink(self.path):
            if (len(listdir(self.path)) != 0 and self.is_recursive
                    and not self.is_dir) or (len(listdir(self.path)) == 0
                                             and (self.is_dir or self.is_recursive)):
                return True
            else:
                if not self.is_recursive and not  self.is_dir:
                    self.logger.log("It's a directory", logging.ERROR, exception.ItIsDirectory)
                elif len(listdir(self.path)) != 0 and  self.is_dir:
                    self.logger.log("Directory not empty",
                                    logging.ERROR, exception.NotEmptyDirectory)
                    return False
        else:
            return True


