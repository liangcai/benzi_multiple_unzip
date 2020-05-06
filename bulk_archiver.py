#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sudo apt install p7zip-full
from zipfile import ZipFile, ZIP_DEFLATED
from rarfile import RarFile
from py7zr import SevenZipFile

from abc import ABC, abstractmethod
from os import getcwd, listdir, walk, chdir
from os.path import isfile, isdir, join, splitext, basename, relpath, dirname
from __init__ import logger


class Archiver(ABC):
    def __init__(self, archiver=None, path=None, file_list=[], pwd=None):
        self.archiver = archiver
        self.path = path
        self.file_list = file_list
        if pwd:
            self.pwd = pwd.encode()

    @abstractmethod
    def un_archive(self):
        pass

    @abstractmethod
    def make_archive(self):
        pass


class Zip(Archiver):
    def un_archive(self):
        with ZipFile(self.archiver, 'r') as z:
            z.extractall(path=self.path, members=None, pwd=self.pwd)

    def make_archive(self):
        with ZipFile(self.archiver, 'w') as z:
            # z.write(self.path, None, ZIP_DEFLATED)
            archiver_root = dirname(self.archiver)
            for root, dirs, files in walk(self.path):
                for f in files:
                    filepath = join(root, f)
                    arcname = join(archiver_root, relpath(filepath, self.path))
                    logger.debug("write file to archiver file ,filepath: {}, arcname: {}".format(filepath, arcname))
                    z.write(filepath, arcname)


class Rar(Archiver):
    def un_archive(self):
        with RarFile(self.archiver, 'r') as z:
            z.extractall(path=self.path, members=None, pwd=self.pwd)

    def make_archive(self):
        with RarFile(self.archiver, 'w') as z:
            archiver_root = dirname(self.archiver)
            for root, dirs, files in walk(self.path):
                for f in files:
                    filepath = join(root, f)
                    arcname = join(archiver_root, relpath(filepath, self.path))
                    logger.debug("write file to archiver file ,filepath: {}, arcname: {}".format(filepath, arcname))
                    z.write(filepath, arcname)


class SevenZip(Archiver):
    def un_archive(self):
        with SevenZipFile(self.archiver, mode='r', password=self.pwd) as z:
            z.extractall(path=self.path)
            
    def make_archive(self):
        return super().make_archive()

class Task(ABC):
    def __init__(self, archivers=None, extracts=None, pwd=None):
        self.archivers = archivers
        self.extracts = extracts
        self.pwd = pwd
        self.start()

    def __del__(self):
        self.end()

    def start(self):
        logger.debug("Start task, archiver in {}, extracts files in {}".format(
            self.archivers, self.extracts))

    def end(self):
        logger.debug("*****End task*****")

    def get_archivers(self):
        allowed_ext = ['.zip', '.7z', '.rar']
        
        files = [
            join(root, f)
            for root, dirs, files in walk(self.archivers) 
            for f in files 
            if splitext(f)[1] in allowed_ext
            ]
        return files

    def get_extracts(self):
        logger.info('extracts: {}'.format(self.extracts))
        onlydirs = [
            f for f in listdir(self.extracts) if isdir(join(self.extracts, f))
        ]
        return onlydirs

    @abstractmethod
    def run(self):
        pass


class Extractall(Task):
    def run(self):
        extracts = self.extracts
        archives = self.get_archivers()
        logger.debug('archives: {}'.format(archives))
        for file in archives:
            fileext = splitext(file)[1]
            # if fileext.lower() == 'zip':
            #     Zip(path=file).un_archive()
            logger.debug('unzip file:{}, to dir: {}, pwd: {}'.format(
                file, self.extracts, self.pwd))
            if fileext == '.7z':
                SevenZip(archiver=file, path=extracts, pwd=self.pwd).un_archive()
            else:
                globals()[fileext.replace('.', '').capitalize()](
                    archiver=file, path=extracts, pwd=self.pwd).un_archive()


class MakeArchiver(Task):
    def run(self):
        archivers = self.archivers
        extracts = self.extracts
        dirs = self.get_extracts()
        logger.debug('dirs: {}'.format(dirs))
        chdir(archivers)
        for dir in dirs:
            globals()['zip'.capitalize()](archiver=dir + '.zip',
                                          path=join(extracts,
                                                    dir)).make_archive()
