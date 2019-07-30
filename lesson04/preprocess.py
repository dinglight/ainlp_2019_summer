import os
import re
import jieba
def preprocess_file(in_file, fout):
    with open(in_file, 'r', encoding='utf-8') as fin:
        for line in fin:
            sline = line.strip()
            # remove empty line
            if sline == "":
                continue
            # remove html mark line
            pattern = re.compile('<.*?>')
            if pattern.match(sline):
                continue
            # jieba
            seg_list = jieba.cut(sline)
            seg_res = ' '.join(seg_list)
            fout.write(seg_res)
            fout.write('\n')

def preprocess(in_folder, out_file):
    fout = open(out_file, 'a', encoding='utf-8')
    for root, dirs, files in os.walk(in_folder):
        for file_name in files:
            in_file = os.path.join(root,file_name)
            preprocess_file(in_file, fout)

if __name__ == '__main__':
    preprocess(r'D:\works\NLP\kaikeba\zhwiki', r'D:\works\NLP\kaikeba\corpus_zhwiki.txt')
