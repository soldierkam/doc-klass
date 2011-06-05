# -*- coding: UTF-8 -*-

import sys
import os

class Document:

    def Document(self, path, klass=None):
        self.__path = path
        self.__klass = klass

    def path(self):
        return str(self.__path)

class LearningSet:

    def __init__(self, dir):
        self.__dirName = dir
        self.__readDir()

    def __readDir(self):
        self.__klasses = ()
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            if not os.path.isdir(single_klass_dir):
                print "Ignoring entry (not dir): ", single_klass_dir
                continue
            self.klasses.add(singleKlassDir)
            for doc_path in os.listdir(single_klass_dir):
                if not os.path.isfile(doc_path):
                    print "Ignoring entry (not file): ", doc_path
                    continue
                self.__documents.append(Document(doc_path))

    def __len__(self):
        return len(self.__documents)

    def klasses(self):
        return set(self.__klasses)

     
class TestingSet:
    def __init__(self, dir):
        self.__dirPath = dir
        self.__documents = []
        for docPath in os.listdir(dir):
            self.__documents.append(Document(docPath))

    def __len__(self):
        return len(self.__documents)        

def main(learning_set_dir, testing_set_dir):
    learning_set = LearningSet(learning_set_dir)
    testing_set = TestingSet(testing_set_dir)
    print "Created learning (%d) and testiong (%d) sets" % (len(learning_set), len(testing_set))
    print "Class count: %d" % (len(learning_set.klasses()))
        