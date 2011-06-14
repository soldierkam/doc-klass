import os.path
# -*- coding: UTF-8 -*-

import re
import os
import nltk
from nltk.stem.lancaster import LancasterStemmer

remove_headers_pattern = re.compile(r"\n\n(.*)", re.DOTALL)
extract_subject_pattern = re.compile(r"Subject:[ ]*(Re:[ ]*)*(.*)", re.IGNORECASE )

class Document:
    __max_important_samples=5
    __part_of_samples=4

    def __init__(self, path, klass=None, test_klass=None):
        self.__path = path
        self.__klass = klass
        self.__test_klass = test_klass
        f=open(path)
        raw=f.read()
        body_results = remove_headers_pattern.search(raw)
        title_results = extract_subject_pattern.search(raw)
        title = title_results.group(2)
        only_body = body_results.group(1)
        only_body = only_body.replace(">", " ") #usuwamy cytowania
        message = only_body + " " + title
        tokens = nltk.word_tokenize(message)
        stemmer = LancasterStemmer()
        self.__tokens = set()
        for token in tokens:
            self.__tokens.add(stemmer.stem(token))
        self.__text = nltk.Text(self.__tokens)
        
    def get_tokens(self):
        return self.__text

    def get_klass(self):
        return self.__klass
        
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
        return self.__fdist.keys()
        

class LearningSet:

    def __init__(self, dir):
        self.__dirName = dir
        self.__read_dir()
        self.freq_dist()
        self.cut_freq_dist()

    def __read_dir(self):
        self.__klasses = set()
        self.__fdist = {}
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            full_path = os.path.join(self.__dirName, single_klass_dir);
            if not os.path.isdir(full_path):
                print "Ignoring entry (not dir): ", full_path
                continue
            self.__klasses.add(single_klass_dir)
            self.__fdist[single_klass_dir] = nltk.FreqDist()
            print "Class: %s" % (single_klass_dir)
            listing=os.listdir(full_path)
            print "Total: " + str(len(listing))
            counter=0
            prevmsg=""
            for doc_path in listing:
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    print "\nIgnoring entry (not file): ", doc_full_path,
                    prevmsg=""
                    continue
                counter+=1
                print "\b" * (len(prevmsg)+2),
                prevmsg="Current: "+str(counter)
                print prevmsg,
                self.__documents.append(Document(doc_full_path, single_klass_dir))
            print

    def __len__(self):
        return len(self.__documents)
    
    def klasses(self):
        return set(self.__klasses)
    
    def documents(self):
        return self.__documents

    def __len__(self):
        return len(self.__documents)
    
    def freq_dist(self):
        for doc in self.__documents:
            klass_name = doc.get_klass()
            klass_dist = self.__fdist[klass_name]
            klass_dist.update(doc.get_tokens())
            
    def cut_freq_dist(self):
        start_index = 0
        end_index = 0
        self.__tokens = {}
        for klass_name, freq_dist in self.__fdist.items():
            half_max_count = freq_dist[freq_dist.max()] / 2
            for token, count in freq_dist.items():
                end_index += 1
                if count > half_max_count:
                    start_index += 1
                elif count < 3:
                    break
            self.__tokens[klass_name] = freq_dist.items()[start_index:end_index]
            
    def print_tokens(self):
        for klass_name, klass_tokens in self.__tokens.items():
            print klass_name
            print klass_tokens
            
    def print_freq_dist(self):
        for klass_name, freq_dist in self.__fdist.items():
            print klass_name
            print freq_dist.items()

class TestingSet:
    def __init__(self, dir):
        self.__dirName = dir
        self.__read_dir()
   
    def __read_dir(self):
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            full_path = os.path.join(self.__dirName, single_klass_dir);
            if not os.path.isdir(full_path):
                print "Ignoring entry (not dir): ", full_path
                continue
            print "Class: "+single_klass_dir
            listing=os.listdir(full_path)
            print "Total: "+str(len(listing))
            counter=0
            prevmsg=""
            for doc_path in os.listdir(full_path):
                doc_full_path = os.path.join(full_path, doc_path);
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
#    for doc in learning_set.documents():
#        print doc.path()
#        print doc.important_samples()
    learning_set.print_tokens()
        
    raw_input("Press enter")
    for doc in testing_set.documents():
        print doc.path()
        print doc.important_samples()
