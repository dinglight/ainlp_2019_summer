import re
import networkx
from scipy.spatial.distance import cosine
from mysentencevector import wordvector_init, sentence_embedding

def text_to_sentences(text):
    '''split the text to sentences
    Args:
        text: a string
    Return:
        sentences: a list of sentences
    '''
    text = re.sub(r'\\n', r' ', text)  # replace \\n to space
    text = re.sub(r'([，。！？])([^”’])', r'\1 \2', text)
    return text.split()

def get_ranked_sentences_by_textrank(sentences, window=3):
    ''' using textrank to ranking the sentences
    Args:
        sentences: a list of string
    Return:
        ranked_sentences: a list of sentences
    '''
    sentence_graph = networkx.Graph()
    for i, sentence in enumerate(sentences):
        sentence_tuples = [(sentences[connect], sentence)
                           for connect in range(i-window, i+window+1)
                           if connect >=0 and connect < len(sentences)]
        sentence_graph.add_edges_from(sentence_tuples)

    ranked_sentences = networkx.pagerank(sentence_graph)
    ranked_sentences = sorted(ranked_sentences.items(), key=lambda x:x[1], reverse=True)
    return ranked_sentences

def get_ranked_sentences_by_sentence_embedding(sentences):
    ''' using sentence_enmbedding cosine distance to ranking the sentences
        let whole text as a sentence vector, choose vector distance nearest sub sentences
    Args:
        sentences: a list of string
    Return:
        ranked_sentences: a list of sentences
    '''
    if isinstance(sentences, list): text = ''.join(sentences)
    text_vector = sentence_embedding(text)

    correlations = {}
    for sentence in sentences:
        sentence_vector = sentence_embedding(sentence)
        correlation = cosine(text_vector, sentence_vector)
        correlations[sentence] = correlation

    ranked_sentences = sorted(correlations.items(), key=lambda x:x[1], reverse=True)
    return ranked_sentences

def extract_sumarization(text, is_sent_vec, constraint=200):
    ''' generate sumarization of the input text

    Args:
       text: a text string
    Return:
       sumarization: a string
    '''
    sentences = text_to_sentences(text)
    if is_sent_vec:
        ranked_sentences = get_ranked_sentences_by_sentence_embedding(sentences)
    else:
        ranked_sentences = get_ranked_sentences_by_textrank(sentences)
    selected_sentences = set()
    current_text = ''

    for sentence, _ in ranked_sentences:
        if len(current_text) > constraint:
            break
        else:
            current_text += sentence
            selected_sentences.add(sentence)

    # print the selected sentence by sequence
    sumarized_sentences = []
    for sentence in sentences:
        if sentence in selected_sentences:
            sumarized_sentences.append(sentence)

    sumarization = ''.join(sumarized_sentences)
    return sumarization

wordvector_init()
