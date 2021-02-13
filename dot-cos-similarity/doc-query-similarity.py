import os
import math

def getDocFreq(directory):

    # getting all documents in given directory
    docs = os.listdir(directory)
    # variable to store frequency words in each file
    doc_freq = {}
    for doc_name in docs:
        term_freq = {}
        doc_freq[doc_name] = term_freq
        #skipping unrelated files
        if doc_name !='.DS_Store':
            # reading document
            doc_file = open(directory+'/'+ doc_name,'r')
            try:
                for term in doc_file.readlines():
                    trm = term.split('\n')[0]
                    if trm not in term_freq:
                        term_freq[trm] = 1
                    else:
                        term_freq[trm] += 1
            finally:
                doc_file.close()
                
    return doc_freq
    
def dotProdScore(query, doc):
    score = 0
    for term in query:
        if term in doc:
            score += (query[term]*doc[term])

    return score

def cosScore(query, doc):
    score = 0
    dot_prod_score = dotProdScore(query, doc)
    doc_score = 0
    query_score = 0
    for term in doc:
        doc_score += (doc[term]*doc[term])
    
    for term in query:
        query_score += (query[term]*query[term])

    score = dot_prod_score/(math.sqrt(doc_score)*math.sqrt(query_score))
    return score

def getTopKSimDocs(query, doc_freq, k, method):
    docs_similarity = ()
    for doc in doc_freq:
        if doc == ".DS_Store":
            continue

        sim_score = 0
        if method == "dotprod":
            sim_score = dotProdScore(query, doc_freq[doc])
        elif method == "cosine":
            sim_score = cosScore(query, doc_freq[doc])

        # adding docs in tuple along with their similarity score
        docs_similarity += ((doc, sim_score),)

    # sorting by score (descending)
    docs_similarity = tuple(sorted(docs_similarity, key = lambda x: x[1], reverse=True))
    
    return docs_similarity[0:k]


if __name__ == "__main__":
    doc_dir = '../dataset/docs'
    doc_freq = getDocFreq(doc_dir)

    queries_dir = '../dataset/queries'
    query_freq = getDocFreq(queries_dir)

    # running all queries one by one with dot product similarity measure

    print("\nGetting results for Dot Product Similarity Method: \n")

    queries = os.listdir(queries_dir)    
    for query_no in queries:
        if query_no == ".DS_Store":
            continue
      
        k = 10
        top_k_similar_docs = getTopKSimDocs(query_freq[query_no], doc_freq, k, method="dotprod")

        print('Top ' + str(k) + ' similar documents to query ' + query_no + ' are: \n')
            
        for doc, sim_score in top_k_similar_docs:
            print('Doc: ' + doc + ', Dot Product Similarity Score: '+ str(sim_score))
        print("\n")

    print("Getting results for Cosine Similarity Method: \n")

    queries = os.listdir(queries_dir)    
    for query_no in queries:
        if query_no == ".DS_Store":
            continue
        k = 10
        top_k_similar_docs = getTopKSimDocs(query_freq[query_no], doc_freq, k, method="cosine")

        print('Top ' + str(k) + ' similar documents to query ' + query_no + ' are: \n')
            
        for doc, sim_score in top_k_similar_docs:
            print('Doc: ' + doc + ', Cosine Similarity Score: '+ str(sim_score))
        print("\n")


