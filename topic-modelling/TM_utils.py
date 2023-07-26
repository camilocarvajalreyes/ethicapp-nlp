import numpy as np

def get_lda_embeddings(lda_model,tokenizer,dictionary,df_test,column):
    """Add description"""
    tokenized_test = [tokenizer(document) for document in df_test[column]]
    doc_term_matrix = [dictionary.doc2bow(bow) for bow in tokenized_test]
    topic_probs = lda_model.get_document_topics(doc_term_matrix,minimum_probability=0)
    return np.array([[p[1] for p in probs] for probs in topic_probs])


def get_table_top_topics(model,sim_topics,similarity,max_w=5):
    # returns a table with max_w words representing the top topics given a topic list with similarity
    topic_num = len(sim_topics)
    data = [[] for _ in range(topic_num)]
    for i, t in enumerate(sim_topics):
        data[i].append(t)
        data[i].append(similarity[i])
        data[i] += [tup[0] for tup in model.get_topic(t)[:max_w]]

    headers = ['Tópico','Probabilidad'] + ['Palabra {}'.format(i+1) for i in range(max_w)]

    return headers, data
