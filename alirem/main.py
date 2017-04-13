#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import argparse
import alirem.logger as log
import alirem.exception as exception
import alirem.alirm as Alirem

REMOVE = 1
RESTORE = 2
SHOW_BASKET_LIST = 3
CLEAN_BASKET = 4
GET_CONFIG = 5

def create_parser(mode=REMOVE):
    parser = argparse.ArgumentParser()
    parser.add_argument('--showparam', action='store_true')
    parser.add_argument('--dryrun', action='store_true', default=None)
    parser.add_argument('-i', '--interactive', action='store_true', default=None)
    parser.add_argument('-f', '--force', action='store_true', default=None)
    parser.add_argument('--configfile', action='store', help='path to config file')
    parser.add_argument('--logfilepath', action='store',
                        help='path to logging file without file extension')
    parser.add_argument('--silent', action='store_true', default=None,
                        help='silent mode')
    parser.add_argument('--logmodecmd', action='store',
                        choices=['info', 'debug', 'warning', 'error'],
                        help='logging level for file')
    parser.add_argument('--logmodefile', action='store',
                        choices=['info', 'debug', 'warning', 'error'], default=None,
                        help='logging level for cmd')

    if mode == REMOVE:
        parser.add_argument('removepath', nargs='+')
        parser.add_argument('-d', '--dir', action='store_true', help='is it dir')
        parser.add_argument('-r', '--recursive', action='store_true', help='is it not empty dir')
        parser.add_argument('-b', '--basket', action='store_true', default=None,
                            help='remove to basket')
        parser.add_argument('-s', '--symlinks', action='store_true', default=None,
                            help='Follow the symlinks')
        parser.add_argument('-p', '--basketpath', action='store', help='path to basket')
        parser.add_argument('-g', '--progress', action='store_true',
                            help='show progress', default=None)
        parser.add_argument('--regexp', action='store', help='regexp for searching in file-tree')

    if mode == RESTORE:
        parser.add_argument('restorename', nargs='+')
        parser.add_argument('-p', '--basketpath', action='store', help='path to basket')
        parser.add_argument('-m', '--merge', action='store_true', default=None,
                            help='merge directores')
        parser.add_argument('-r', '--replace', action='store_true', default=None,
                            help='replace existing files')
        parser.add_argument('-g', '--progress', action='store_true',
                            help='show progress', default=None)
    if mode == CLEAN_BASKET:
        parser.add_argument('-m', '--clearmode', action='store', choices=['size', 'time'],
                            help='cleaning mode for basket')
        parser.add_argument('-t', '--deltatime', action='store', type=int,
                            help='file storage time in basket')
        parser.add_argument('-x', '--maxsize', action='store', type=int,
                            help='max size of basket')
        parser.add_argument('-p', '--basketpath', action='store',
                            help='path to basket')
        # parser.add_argument('-s', '--show', action='store_true', default=None,
        #                     help='show the contents of the basket')

    if mode == SHOW_BASKET_LIST:
        pass
    if mode == GET_CONFIG:
        pass

    namespace = parser.parse_args()
    return namespace



def update_params(cmd, default_config, config=None):
    if config is not None:
        #Overlap default_config by config
        for key, value in default_config.iteritems():
            if value != config.get(key) and config.get(key) is not None:
                default_config[key] = config.get(key)
    for key, value in default_config.iteritems():
        if value != cmd.get(key) and cmd.get(key) is not None:
            default_config[key] = cmd.get(key)



def remove():
    main(REMOVE)
def restore():
    main(RESTORE)
def clean_basket():
    main(CLEAN_BASKET)
def show_basket_list():
    main(SHOW_BASKET_LIST)
def show_config():
    main(GET_CONFIG)


def load_config_file(path):
    if path is not None:
        with open(path) as config:
            return json.load(config)
    else:
        return None

def show_params(default_config):
    for key, value in default_config.iteritems():
        print key+':'+str(value)

def get_logger(config):
    return log.Logger(mode_for_file=config['logmodefile'],
                      mode_for_cmd=config['logmodecmd'],
                      path=config['logfilepath'],
                      is_silent=config['silent'],
                      is_force=config['force'])


def main(mode=REMOVE):
    args = create_parser(mode)
    config = load_config_file(args.configfile)
    default_config = load_config_file('config_file_default.json')
    update_params(vars(args), default_config, config)
    logger = get_logger(default_config)
    alirem = Alirem.Alirem(logger=logger)

    def run():
        if mode == REMOVE:
            for path in args.removepath:
                alirem.remove(path=path, is_dir=args.dir,
                              is_recursive=args.recursive,
                              is_interactive=default_config['interactive'],
                              is_dryrun=default_config['dryrun'],
                              is_basket=default_config['basket'],
                              basket_path=default_config['basketpath'],
                              regexp=args.regexp,
                              symlinks=default_config['symlinks'],
                              is_progress=default_config['progress'])
        if mode == RESTORE:
            for path in args.restorename:
                alirem.restore(restorename=path, basket_path='basket',
                               is_merge=default_config['merge'],
                               is_replace=default_config['replace'],
                               is_progress=default_config['progress'])

        if mode == CLEAN_BASKET:
            alirem.check_basket_for_cleaning(is_show=default_config['show'],
                                             basket_path=default_config['basketpath'],
                                             mode=default_config['clearmode'],
                                             time=default_config['deltatime'],
                                             size=default_config['maxsize'])
        if mode == SHOW_BASKET_LIST:
            alirem.show_basket_list()
        if mode == GET_CONFIG:
            show_params(default_config)

    try:
        run()
    except exception.Error as error:
        print error.exit_code
        exit(error.exit_code)
