# Auxiliary functions for Naive-Bayes interpretation

def get_probs(token,clf,df_base,column_text):
    sample = df_base.sample()
    sample[column_text] = token
    return tuple(clf.predict_proba(sample)[0])


def get_top_k_ngrams(k,vectorizer,prob_left,prob_right,str_left,str_right,verbose=True):
    idx_left = sorted(range(len(prob_left)), key=lambda x: prob_left[x])[-k:][::-1]
    idx_right = sorted(range(len(prob_right)), key=lambda x: prob_right[x])[-k:][::-1]

    dic_left = {vectorizer.get_feature_names_out()[i]:prob_left[i] for i in idx_left}
    dic_right = {vectorizer.get_feature_names_out()[i]:prob_right[i] for i in idx_right}

    if verbose:
        print("Top features '{}':".format(str_left))
        for key, value in dic_left.items():
            print(key, value)
        print("\nTop features '{}':".format(str_right))
        for key, value in dic_right.items():
            print(key, value)
    
    return dic_left, dic_right
