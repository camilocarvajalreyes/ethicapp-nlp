import numpy as np
import matplotlib.pyplot as plt

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


def plot_frecuencies(input_list,label):
    frequency_dict = {}
    for element in input_list:
        if element in frequency_dict:
            frequency_dict[element] += 1
        else:
            frequency_dict[element] = 1
    counts = frequency_dict

    # Switching to the OO-interface. You can do all of this with "plt" as well.
    fig, ax = plt.subplots()

    keys = counts.keys()
    values = counts.values()

    plt.bar(keys, values)

    custom_ticks = list(range(-1,max(input_list)))
    plt.xticks(custom_ticks)

    plt.xlabel('Tópicos')
    plt.ylabel('Frecuencia')
    plt.title('Tópicos postura: {}'.format(label))

    plt.show()


def get_top_k_topics(input_list,k=5):

    frequency_dict = {}
    for element in input_list:
        if element in frequency_dict:
            frequency_dict[element] += 1
        else:
            frequency_dict[element] = 1

    # Sort the dictionary items by their values in descending order
    sorted_items = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 keys with the largest values
    top_k_keys = [item[0] for item in sorted_items[:k]]
    top_k_values = [item[1] for item in sorted_items[:k]]

    top_k_values = [elem/len(input_list) for elem in top_k_values]

    return top_k_keys, top_k_values

def random_indices_of_x_appearances(arr, x, k):
    if type(arr) == list:
        arr = np.array(arr)
    indices = np.where(arr == x)[0]
    random_indices = np.random.choice(indices, size=min(k, len(indices)), replace=False)
    return random_indices


def get_k_random_samples_from_topic(df,BT_output,topic:int,k=5):
    # takes a dataframe, a BERTopic output of the same df and returns k random samples of the corresponding topic
    indices = random_indices_of_x_appearances(BT_output[0],topic,k)
    filtered_df = df.iloc[indices]
    return filtered_df, [vec[topic] for vec in BT_output[1][indices]]
