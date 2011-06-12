# -*- coding: UTF-8 -*-

import sys
import os
import nltk


class Document:
    __max_important_samples=5
    __part_of_samples=4

    def __init__(self, path, klass=None, test_klass=None):
        self.__path = path
        self.__klass = klass
        self.__test_klass = test_klass
        f=open(path)
        raw=f.read()
        self.__tokens = nltk.word_tokenize(raw)
        self.__text = nltk.Text(self.__tokens)
        self.__fdist = nltk.FreqDist(self.__text);      
        

    def path(self):
        return str(self.__path)
    
    def important_samples(self):
        n=self.__fdist.N()
        if n/self.__part_of_samples>self.__max_important_samples:
            samples_number=self.__max_important_samples
        else:
            samples_number=n/self.__part_of_samples
        if samples_number==0:
            samples_number=1
        return self.__fdist.samples()[(n/2-samples_number):(n/2+samples_number)]
        

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
            print "Class: "+single_klass_dir
            listing=os.listdir(full_path)
            print "Total: "+str(len(listing))
            counter=0
            prevmsg=""
            for doc_path in listing:
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    print "\nIgnoring entry (not file): ", doc_full_path,
                    prevmsg=""
                    continue
                counter+=1
                print "\b"*(len(prevmsg)+2),
                prevmsg="Current: "+str(counter)
                print prevmsg,
                self.__documents.append(Document(doc_full_path, single_klass_dir))
            print

    def klasses(self):
        return set(self.__klasses)
    
    def documents(self):
        return self.__documents

    def __len__(self):
        return len(self.__documents)

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
            print "Class: "+single_klass_dir
            listing=os.listdir(full_path)
            print "Total: "+str(len(listing))
            counter=0
            prevmsg=""
            for doc_path in os.listdir(full_path):
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    print "\nIgnoring entry (not file): ", doc_full_path
                    prevmsg=""
                    continue
                counter+=1
                print "\b"*(len(prevmsg)+2),
                prevmsg="Current: "+str(counter)
                print prevmsg,
                self.__documents.append(Document(doc_full_path, test_klass=single_klass_dir))
            print
    
    def documents(self):
        return self.__documents
    
    def __len__(self):
        return len(self.__documents)        

def main(learning_set_dir, testing_set_dir):
    learning_set = LearningSet(learning_set_dir)
    print "Created learning (%d) set" % (len(learning_set))
    testing_set = TestingSet(testing_set_dir)
    print "Created testing (%d) set" % (len(testing_set))
    print "Class count: %d" % (len(learning_set.klasses()))

    #test Document.important_samples
    
    raw_input("Press enter")
    for doc in learning_set.documents():
        print doc.path()
        print doc.important_samples()
        
    raw_input("Press enter")
    for doc in testing_set.documents():
        print doc.path()
        print doc.important_samples()
