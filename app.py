# -*- coding: UTF-8 -*-

import sys
import os

class Document:

    def __init__(self, path, klass=None, test_klass=None):
        self.__path = path
        self.__klass = klass
        self.__test_klass = test_klass

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
            full_path = self.__dirName + single_klass_dir;
            if not os.path.isdir(full_path):
                print "Ignoring entry (not dir): ", single_klass_dir
                continue
            self.__klasses += (single_klass_dir,)
            for doc_path in os.listdir(full_path):
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    print "Ignoring entry (not file): ", doc_full_path
                    continue
                self.__documents.append(Document(doc_full_path, single_klass_dir))

    def __len__(self):
        return len(self.__documents)

    def klasses(self):
        return set(self.__klasses)

     
class TestingSet:
    def __init__(self, dir):
        self.__dirName = dir
        self.__readDir()
   
    def __readDir(self):
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            full_path = self.__dirName + single_klass_dir;
           
            if not os.path.isdir(full_path):
                print "Ignoring entry (not dir): ", single_klass_dir
                continue
            for doc_path in os.listdir(full_path):
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    print "Ignoring entry (not file): ", doc_full_path
                    continue
                self.__documents.append(Document(doc_full_path, test_klass=single_klass_dir))
   
    def __len__(self):
        return len(self.__documents)        

def main(learning_set_dir, testing_set_dir):
    learning_set = LearningSet(learning_set_dir)
    testing_set = TestingSet(testing_set_dir)
    print "Created learning (%d) and testing (%d) sets" % (len(learning_set), len(testing_set))
    print "Class count: %d" % (len(learning_set.klasses()))
        
