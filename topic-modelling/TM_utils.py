import numpy as np

def get_lda_embeddings(lda_model,tokenizer,dictionary,df_test,column):
    """Add description"""
    tokenized_test = [tokenizer(document) for document in df_test[column]]
    doc_term_matrix = [dictionary.doc2bow(bow) for bow in tokenized_test]
    topic_probs = lda_model.get_document_topics(doc_term_matrix)
    return np.array([[p[1] for p in probs] for probs in topic_probs])
