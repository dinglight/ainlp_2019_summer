import os
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser

def build_parse_child_dict(words, postags, arcs):
    """
    为句子中的每个词语维护一个保存句法依存儿子节点的字典
    Args:
        words: 分词列表
        postags: 词性列表
        arcs: 句法依存列表
    """
    child_dict_list = []
    for index in range(len(words)):
        child_dict = dict()
        for arc_index in range(len(arcs)):
            if arcs[arc_index].head == index + 1:
                if arcs[arc_index].relation in child_dict:
                    child_dict[arcs[arc_index].relation].append(arc_index)
                else:
                    child_dict[arcs[arc_index].relation] = []
                    child_dict[arcs[arc_index].relation].append(arc_index)
        #if child_dict.has_key('SBV'):
        #    print words[index],child_dict['SBV']
        child_dict_list.append(child_dict)
    return child_dict_list

def complete_e(words, postags, child_dict_list, word_index):
    """
    完善识别的部分实体
    """
    child_dict = child_dict_list[word_index]
    prefix = ''
    if 'ATT' in child_dict:
        for i in range(len(child_dict['ATT'])):
            prefix += complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

    postfix = ''
    if postags[word_index] == 'v':
        if 'VOB' in child_dict:
            postfix += complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
        if 'SBV' in child_dict:
            prefix = complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

    return prefix + words[word_index] + postfix

def extract_opinion(document):
    LTP_DATA_DIR = r'../../tools/ltp_data_v3.4.0/'  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型

    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型

    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser() # 初始化实例
    parser.load(par_model_path)  # 加载模型

    # cut to sentences
    sentences = SentenceSplitter.split(document)
    table = []
    for sentence in sentences:
        # cut words
        words = segmentor.segment(sentence)  # 分词
        # postages
        postags = postagger.postag(words)  # 词性标注
        # ner
        netags = recognizer.recognize(words, postags)  # 命名实体识别
        # dependency parsing
        arcs = parser.parse(words, postags)  # 句法分析

        child_dict_list = build_parse_child_dict(words, postags, arcs)
        index = 0
        for arc in arcs:
            if arc.relation == 'HED':
                break
            index+=1

        # 谓语是说一类的词
        predicate = words[index]
        child_dict = child_dict_list[index]
        if ('SBV' in child_dict) and ('VOB' in child_dict):
            e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
            r = words[index]
            e2 = ''.join(words[index+1:])
            table.append((e1,r,e2))


    segmentor.release()  # 释放模型
    postagger.release()  # 释放模型
    recognizer.release()  # 释放模型
    parser.release()  # 释放模型

    return table
