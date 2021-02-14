import os
import pandas as pd
import math
import numpy as np
import nltk

# create English stop words list
stopwords = nltk.corpus.stopwords.words('english')

doc_dir = './dataset/docs'
doc_names = []
# getting content in each document
def get_docs_contents(directory):
    # getting all documents in given directory
    docs = os.listdir(directory)
    # term doc matrix, list of documents against each term
    docs_cont = []
    for doc_name in docs:
        doc_names.append(doc_name)

        #skipping unrelated files
        if doc_name !='.DS_Store':
            # reading document
            doc_file = open(directory+'/'+ doc_name,'r')
            try:
                terms = []
                for term in doc_file.readlines():
                    trm = term.split('\n')[0].lower()
                    terms.append(trm)
                docs_cont.append(terms)
            finally:
                doc_file.close()
    return docs_cont

# getting unique list of words in set from bag of words
def unique_words(bag_of_words):
    unique_words = bag_of_words[0]
    for i in range(1,len(bag_of_words)):
        unique_words = set(unique_words).union(set(bag_of_words[i]))
    return unique_words

# created term document matrix/ dataframe
def term_document_matrix(bag_of_words, word_dict):
    
    for bow_i,worddict_i in zip(bow,worddict):
        for word in bow_i:
                    worddict_i[word]+=1
    return pd.DataFrame(worddict)

# calculating term frequency for each term with respect to corresponding document/bag of words
# most values will be 0
def term_freq(worddict,bow):
    tfdict = {}
    bowcount = len(bow)
    for word,count in worddict.items():
        tfdict[word] = count/float(bowcount)
    return tfdict

# calculates inverse document frequency
def idf(doclist):
    idfdict={}
    n = len(doclist)
    
    idfdict = dict.fromkeys(doclist[0].keys(),0)
    for doc in doclist:
        for word,val in doc.items():
            if val>0:
                idfdict[word]+=1
    for word,val in idfdict.items():
        idfdict[word]=math.log(n/float(val))
    return idfdict

# calculates tf-idf
def tfidf(tfbow,idfs):
    tfidf = {}
    for word,val in tfbow.items():
        tfidf[word]=val*idfs[word]
    return tfidf

    
def print_top_words_of_top_concepts(N, K, mat, S):
    terms = mat.index
    
    concept_words = {}
    concept_magnitude = {}
    for i,component in enumerate(S.T):
        y = zip(terms,component)
        
        magnitude = np.linalg.norm(component)

        concept_magnitude["Concept-"+str(i)] = magnitude

        terms_score=sorted(y,key = lambda x:x[1],reverse=True)[:K]
        
        top_k_words = []
        for term_score in terms_score:
            top_k_words.append(term_score[0])
            
        concept_words["Concept-"+str(i)] = top_k_words
            # sorting concepts based on magnitude
    print("\nTop " + str(K) + " words of top " + str(N) + " concepts: \n")
    top_concepts = dict(sorted(concept_magnitude.items(), key=lambda item: item[1], reverse=True))
    count = 0
    for concept in top_concepts:
        if count == N:
            break
        print(concept + ": ")
        print("Singular Value: " + str(concept_magnitude[concept]))
        print(concept_words[concept])
        count+=1

    
def print_top_docs_of_top_concepts(N, K, mat, D):

    cols = X.columns
    
    concept_docs = {}
    concept_magnitude = {}

    for i,component in enumerate(D):
        y = zip(cols,component)
        
        magnitude = np.linalg.norm(component)
        concept_magnitude["Concept-"+str(i)] = magnitude

        docs_score=sorted(y,key = lambda x:x[1],reverse=True)[:K]
        top_docs = []
        for doc_score in docs_score:
            top_docs.append(doc_names[doc_score[0]])
        concept_docs["Concept-"+str(i)] = top_docs

    print("\nTop " + str(K) + " documents of top " + str(N) + " concepts: \n")
    top_concepts = dict(sorted(concept_magnitude.items(), key=lambda item: item[1], reverse=True))
    count = 0
    for concept in top_concepts:
        if count == N:
            break
        print(concept + ": ")
        print("Singular Value: " + str(concept_magnitude[concept]))
        print(concept_docs[concept])
        count+=1

docs_content = get_docs_contents(doc_dir)
# creating bag of words
bow=[[i for i in docs_content[j] if i not in stopwords] for j in range(len(docs_content))]
wordset = unique_words(bow)
# creating word dictionary with respect to each document
# each row of bag of words contains words of specific document (identified by that row)
worddict = [dict.fromkeys(wordset,0) for i in range(len(bow))]

docterm = term_document_matrix(bow, worddict)

tfbow =[term_freq(i,j) for i,j in zip(worddict,bow)]

idfs = idf(worddict) 

tfidf = [tfidf(i,idfs) for i in tfbow]  

# taking transponse
X = pd.DataFrame(tfidf).T

# performing singular value decomposition
S,V,D=np.linalg.svd(X)

no_of_concepts = 5
no_of_words = 10
no_of_docs = 10

print_top_words_of_top_concepts(no_of_concepts,no_of_words, X, S)
print_top_docs_of_top_concepts(no_of_concepts, no_of_docs, X, D)

        
