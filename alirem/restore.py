#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os.path import join, exists, isfile, dirname, isdir, islink
from os import remove, makedirs, unlink
import logging
import shutil
import alirem.basket_list as basketlist
import alirem.copy as copy

def restore(name, basket_path, logger, is_merge=True, is_replace=False, is_progress=False):
    basket_list = basketlist.BasketList(basket_path)
    basket_list.load()
    index_name = join(basket_path, name)
    element = basket_list.search(name, basket_path)
    if element is not None:
        if not exists(dirname(element.rm_path)):
            makedirs(dirname(element.rm_path))
        dst = element.rm_path
        copyhandler = copy.CopyHandler(logger=logger,
                                       is_merge=is_merge,
                                       is_replace=is_replace,
                                       is_progress=is_progress,
                                       symlinks=False)
        copyhandler.run(index_name, dst)

        if isfile(index_name):
            remove(index_name)
        elif isdir(index_name):
            shutil.rmtree(index_name)
        elif islink(index_name):
            unlink(index_name)
        basket_list.remove(element)
        return True
    else:
        logger.log("Cannot find such file <{}> in <{}>".format(name, basket_path), logging.WARNING)
        basket_list.save()
        return False













    #   if isfile(index_name):
    #         if not exists(dst):#if not such file
    #             shutil.copyfile(index_name, dst)
    #             remove(index_name)
    #             basket_list.remove(element)
    #             logger.log("File {} restored".format(basename(dst)), logging.INFO)

    #         elif not is_force:#if file exists and force=False
    #             logger.log("""File {} can not be restored. File with
    #                                 the same name already exists""".format(basename(dst)),
    #                        logging.WARNING)

    #         elif is_force:
    #             if isfile(dst):
    #                 remove(dst)
    #                 logger.log("""Old file was replaced by restored
    #                                     file {}""".format(basename(dst)),
    #                            logging.INFO)

    #             else:
    #                 shutil.rmtree(dst)
    #                 logger.log("""Old directory was replaced by restored
    #                                     file {}""".format(basename(dst)),
    #                            logging.INFO)
    #             shutil.copyfile(index_name, dst)
    #             remove(index_name)
    #             basket_list.remove(element)


    #     if isdir(index_name):

    #         if not exists(dst):
    #             shutil.copytree(index_name, dst)
    #             shutil.rmtree(index_name)
    #             basket_list.remove(element)
    #             logger.log("Directory {} restored".format(basename(dst)), logging.INFO)

    #         elif not is_force:#if file exists and force=False
    #             logger.log("""Directory {} can not be restored. Directory or file with
    #                             the same name already exists""".format(basename(dst)),
    #                        logging.WARNING)

    #         elif is_force:
    #             if isfile(dst):
    #                 remove(dst)
    #                 logger.log("""Old file was replaced by restored
    #                                 directory {}""".format(basename(dst)),
    #                            logging.INFO)
    #             else:
    #                 shutil.rmtree(dst)#delete file if exist the same name
    #                 logger.log("""Old directory was replaced by restored
    #                                 directory {}""".format(basename(dst)),
    #                            logging.INFO)
    #             shutil.copytree(index_name, dst)
    #             shutil.rmtree(index_name)


