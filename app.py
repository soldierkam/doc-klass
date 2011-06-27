import os.path
# -*- coding: UTF-8 -*-

import re
import os
import nltk
import logging
import datetime
from nltk.stem.lancaster import LancasterStemmer
from nltk import bigrams
from nltk.corpus import stopwords
#import enchant

remove_headers_pattern = re.compile(r"\n\n(.*)", re.DOTALL)
extract_subject_pattern = re.compile(r"Subject:[ ]*(Re:[ ]*)*(.*)", re.IGNORECASE )
word_pattern = re.compile(r"\w+[-\w]*", re.IGNORECASE)
BIGRAM_MIN_COUNT = 1

class NullStream():
    def write(self, msg):
        pass

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, stream=NullStream())
logger = logging.getLogger('classifier')
logger.setLevel(logging.DEBUG)
logger.propagate = False
console = logging.StreamHandler()
console.setLevel(logging.INFO)
file = logging.FileHandler("app_" + str(datetime.datetime.now()) + ".log")
<<<<<<< HEAD
#console.setLevel(logging.DEBUG)
logger.addHandler(file)
=======
zaralogger.addHandler(file)
>>>>>>> f6fd77e297be5818b555e271410126bb5a756bdf
logger.addHandler(console)

logger_failed = logging.getLogger("failed")
logger_failed.setLevel(logging.INFO)
logger_failed.propagate = False
file_failed = logging.FileHandler("failed.log", mode="w")
logger_failed.addHandler(file_failed)


logger_bigrams = logging.getLogger("bigrams")
logger_bigrams.setLevel(logging.INFO)
logger_bigrams.propagate = False
file_bigrams = logging.FileHandler("bigrams.log", mode="w")
logger_bigrams.addHandler(file_bigrams)

logger_wrong_words = logging.getLogger("bigrams.words")
logger_wrong_words.setLevel(logging.INFO)
file_wrong_words = logging.FileHandler("wrong_words.log", mode="w")
logger_wrong_words.addHandler(file_wrong_words)


class Document:
    __max_important_samples=5
    __part_of_samples=4
    __stopwords = stopwords.words('english');
        
    def __init__(self, path, klass=None, test_klass=None):
        self.__path = path
        self.__klass = klass
        self.__test_klass = test_klass
        logger_bigrams.info("###############################################################\nFile: %s\n" % self.get_file_name())
        title, only_body = self.read_content();
        bigrams = self._get_bigrams_from_message(only_body)
        bigrams.extend(self._get_bigrams_from_message(title))
        logger_bigrams.info("Bigrams:%s \n" % str(bigrams))
        logger_bigrams.debug("Title:%s \nMsg:%s \n" %(title, only_body))
        self.__bigrams = nltk.Text(set(bigrams))
        
    def read_content(self):
        f=open(self.__path)
        raw=f.read()
        body_results = remove_headers_pattern.search(raw)
        title_results = extract_subject_pattern.search(raw)
        title = title_results.group(2)
        only_body = body_results.group(1)
        return (title, only_body)
        
    def _get_bigrams_from_message(self, message):
        message = message.replace(">", " ") #usuwamy cytowania
        #eng_dict = enchant.Dict("en_US")
        tokens = nltk.word_tokenize(message)
        logger_wrong_words.debug("Tokens: " + str(tokens))
        stemmer = LancasterStemmer()
        stemmed_tokens = set()
        words = []
        for token in tokens:
            new_words = word_pattern.findall(token)
            if new_words:
                #if eng_dict.check(words[0]):
                stem = stemmer.stem(new_words[0])
                stemmed_tokens.add(stem)
                words.append(stem)
                logger_wrong_words.debug("OK: " + stem)
                #else:
                #    logger.info("Mispelled word: %s (token: %s)" % (words[0], token))
                #    logger_wrong_words.info("nd: %s file: %s" % (words[0], self.get_file_name()))
            else:
                logger_wrong_words.info("%s file: %s" % (token, self.get_file_name()))
        logger_bigrams.debug("Words: %s" % str(words))
        return self._filter_stopwords(self.__create_bigrams(words))
    
    def __create_bigrams(self, words):
        bigrams_list = bigrams(words)
        count = max(0, len(words) - 2)
        for i in range(count):
            bigrams_list.append(tuple(words[i:i+3:2]))
        return bigrams_list
    
    def _filter_stopwords(self, bigrams):
        results = []
        for bigram_tuple in bigrams:
            stop_words_count = 0
            for i in bigram_tuple:
                stop_words_count += self.__stopwords.count(i)
                
            if stop_words_count >= len(bigram_tuple):
                logger_bigrams.info("Ignoring bigram %s - contains only stopwords(%d)" % (str(bigram_tuple), stop_words_count))
                pass
            
            isdigit_count = 0
            for i in bigram_tuple:
                isdigit_count += 1 if i.isdigit() else 0
            if isdigit_count >= len(bigram_tuple):
                logger_bigrams.info("Ignoring bigram %s - contains only digits" % (str(bigram_tuple)))
                pass
            
            results.append(bigram_tuple)
        return results    
    
    def get_bigrams_tuple(self):
        return self.__bigrams
    
    def get_bigrams(self):
        bigrams = []
        for bigram_tuple in self.get_bigrams_tuple():
            bigram = " ".join(bigram_tuple)
            bigrams.append(bigram)
        return bigrams            

    def get_klass(self):
        return self.__klass

    def get_test_klass(self):
        return self.__test_klass

    def set_klass(self,klass):
        self.__klass=klass
        
    def get_path(self):
        return str(self.__path)
    
    def get_file_name(self):
        return str(os.path.basename(self.__path))
    
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
        self.__klass_matrix = {}
        for document_klass_name in self.__bigrams.keys():
            for document_test_klass_name in self.__bigrams.keys():
                self.__klass_matrix[(document_klass_name, document_test_klass_name)] = 0        

    def __read_dir(self):
        self.__klasses = set()
        self.__fdist = {}
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            full_path = os.path.join(self.__dirName, single_klass_dir);
            if not os.path.isdir(full_path):
                logger.warning("Ignoring entry (not dir): " + full_path)
                continue
            self.__klasses.add(single_klass_dir)
            self.__fdist[single_klass_dir] = nltk.FreqDist()
            logger.info("Class: %s" % (single_klass_dir))
            listing=os.listdir(full_path)
            logger.info("Total: " + str(len(listing)))
            counter=0
            prevmsg=""
            for doc_path in listing:                
                doc_full_path = full_path + os.sep + doc_path;
                if not os.path.isfile(doc_full_path):
                    logger.warning("\nIgnoring entry (not file): " + doc_full_path)
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
            bigrams = doc.get_bigrams()
            klass_dist.update(bigrams)
        for klass_name, klass_freq_dist in self.__fdist.items():
            logger.debug("Klass: %s\n%s\n\n" % (klass_name, str(klass_freq_dist.items()) ) )
            
    def cut_freq_dist(self):
        self.__bigrams = {}
        for klass_name, freq_dist in self.__fdist.items():
            self.__bigrams[klass_name] = {}
            for bigram, count in freq_dist.items():
                self.__bigrams[klass_name][bigram] = count
            
            
    def print_bigrams(self):
        for klass_name, klass_bigrams in self.__bigrams.items():
            logger.debug("Klass name: " + klass_name + "\nBigrams:")
            logger.debug(str(klass_bigrams))
            
    def print_freq_dist(self):
        for klass_name, freq_dist in self.__bigrams.items():
            logger.info("Klass name: " + klass_name)
            logger.info(str(freq_dist.items()))
            
    def _calc_bigram_value(self, bigram):
        klasses_count = len(self.__bigrams.keys()) + 1
        count_bigram_in_klasses = 0
        for klass_bigrams in self.__bigrams.values():
            count_bigram_in_klasses += 1 if klass_bigrams.has_key(bigram) else 0
        value = klasses_count - count_bigram_in_klasses;
        assert(value >= 0)
        return pow(2, value)
        
    def classify(self,document):
            
        count={}
        for klass_name in self.__bigrams.keys():
            klass_bigrams = self.__bigrams[klass_name]
            count[klass_name]=0             
            for document_bigram in document.get_bigrams():
                if klass_bigrams.has_key(document_bigram):
                    count[klass_name] += self._calc_bigram_value(document_bigram)#klass_bigrams[document_bigrams]
        max_value=0
        max_klass_name=count.keys()[0]
        doc_klass_name=document.get_test_klass()
        for klass_name, value in count.items():
            if value>max_value:
                max_value=value
                max_klass_name=klass_name
        
        document.set_klass(max_klass_name)
        is_correct = doc_klass_name == max_klass_name
        self.__klass_matrix[(max_klass_name, doc_klass_name)] += 1
        
        if not is_correct:
            logger_failed.info("\n#########################################\n")
            logger_failed.info("%s: '%s' as '%s'" % (document.get_file_name(), doc_klass_name, max_klass_name) )
            logger_failed.info("Counts: %s" % str(sorted(count.items(), key= lambda i: i[1], reverse=True)))  
            
            wrong_class_bigrams = self.__bigrams[max_klass_name]
            correct_class_bigrams = self.__bigrams[doc_klass_name]
            line_w_args = []
            line_c_args = []
            for document_bigram in document.get_bigrams():
                if wrong_class_bigrams.has_key(document_bigram):
                    line_w_args.append(document_bigram)
                if correct_class_bigrams.has_key(document_bigram):
                    line_c_args.append(document_bigram)
            logger_failed.info("\nDocument and wrong class bigrams:" + str(line_w_args))
            logger_failed.info("\nDocument and corrent class bigrams:"+ str(line_c_args))
            logger_failed.info("\nDocument title: %s\nContent:\n%s" % document.read_content())
            
        logger.debug("\n######################################### %s" % ("OK" if is_correct else "FAIL") )
        logger.debug("%s: '%s' as '%s'" % (document.get_file_name(), doc_klass_name, max_klass_name) )
        logger.debug("Counts: %s" % str(count))
        return is_correct
    
    def print_klass_matrix(self):
        columns = len(self.__bigrams.keys())
        line = " %s %s" + ("%s" * columns)
        max_klass_name_len = 0
        for klass_name in self.__bigrams.keys():
            max_klass_name_len = max(max_klass_name_len, len(klass_name))
        
        first_line_arg = [" " * (max_klass_name_len + 2)]
        for id in range(97,columns + 97):
            first_line_arg.append(chr(id).rjust(4))
        first_line = " %s" + ("%s" * columns)
        logger.info(first_line % tuple(first_line_arg))
        
        klass_id = 97
        for real_klass_name in self.__bigrams.keys():
            arg = [chr(klass_id), real_klass_name.ljust(max_klass_name_len)]
            klass_id += 1
            for classifier_klass_name in self.__bigrams.keys():
                arg.append(str(self.__klass_matrix[(classifier_klass_name, real_klass_name)]).rjust(4))
            logger.info(line % tuple(arg))        
    
    def print_classifier_parameters(self):
        tp={}
        fp={}
        fn={}
        tn={}
        for classifier_klass_name in self.__bigrams.keys():
            fp[classifier_klass_name]=0
            fn[classifier_klass_name]=0
            tn[classifier_klass_name]=0
            
        for classifier_klass_name in self.__bigrams.keys():
            tp[classifier_klass_name]=self.__klass_matrix[(classifier_klass_name,classifier_klass_name)]           
                        
            for real_klass_name in self.__bigrams.keys():
                if classifier_klass_name!=real_klass_name:
                    fp[classifier_klass_name]+=self.__klass_matrix[(classifier_klass_name,real_klass_name)]                
                    tn[classifier_klass_name]+=self.__klass_matrix[(real_klass_name,real_klass_name)]                    
                    for klass_name in self.__bigrams.keys():
                        if klass_name!=classifier_klass_name:
                            fn[klass_name]+=self.__klass_matrix[(classifier_klass_name,real_klass_name)]
                       
        
             
        for i in self.__bigrams.keys():
            
            precision=float(tp[i])/float(tp[i]+fp[i])
            recall=float(tp[i])/float(tp[i]+fn[i])
            specificity=float(tn[i])/float(tn[i]+fp[i])
            accuracy=float(tp[i]+tn[i])/float(tp[i]+tn[i]+fp[i]+fn[i])
            line="Class - "+i+" precision:"+str(precision)+" recall:"+str(recall)+" specificity:"+str(specificity)+" accuracy:"+str(accuracy)
            logger.info(line);        
                
class TestingSet:
    def __init__(self, dir):
        self.__dirName = dir
        self.__read_dir()
   
    def __read_dir(self):
        self.__documents = []
        for single_klass_dir in os.listdir(self.__dirName):
            full_path = os.path.join(self.__dirName, single_klass_dir);
            if not os.path.isdir(full_path):
                logger.warning("Ignoring entry (not dir): " + full_path)
                continue
            logger.info("Class: "+single_klass_dir)
            listing=os.listdir(full_path)
            logger.info("Total: "+str(len(listing)))
            counter=0
            prevmsg=""
            for doc_path in os.listdir(full_path):
                doc_full_path = os.path.join(full_path, doc_path);
                if not os.path.isfile(doc_full_path):
                    logger.warning("\nIgnoring entry (not file): ", doc_full_path)
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
    
    def print_document_klasses(self):
        for doc in self.__documents:
            logger.info(doc.get_klass()+" "+doc.get_test_klass())


def main(learning_set_dir, testing_set_dir):
    learning_set = LearningSet(learning_set_dir)
    logger.info("Created learning (%d) set" % (len(learning_set)))
    testing_set = TestingSet(testing_set_dir)
    logger.info("Created testing (%d) set" % (len(testing_set)))
    logger.info("Class count: %d" % (len(learning_set.klasses())))

    learning_set.print_bigrams()
            
    correct_class = 0
    all_documents = len(testing_set)
    for doc in testing_set.documents():
        if learning_set.classify(doc):
            correct_class += 1;
    
    logger.info("Correctness: %d / %d - %f %%" % (correct_class, all_documents, (float(100) * correct_class) / all_documents ))
    #testing_set.print_document_klasses()
    learning_set.print_klass_matrix()
    learning_set.print_classifier_parameters()
    logger_wrong_words.info("End")
    
