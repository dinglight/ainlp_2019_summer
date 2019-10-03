#在西部世界里，一个”人类“的语言可以定义为：
import random
from lm import *

human = """
human = 自己 寻找 活动
自己 = 我 | 俺 | 我们
寻找 = 找找 | 想找点
活动 = 乐子 | 玩的
"""


#一个“接待员”的语言可以定义为

host = """
host = 寒暄 报数 询问 业务相关 结尾
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = null
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？
"""

def create_grammar(grammar_str, split='=', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip(): continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar

def generate(gram, target):
    if target not in gram: return target

    expend = [generate(gram, t) for t in random.choice(gram[target])]
    return ''.join([e for e in expend if e != 'null'])

def generate_n(n, gram, target):
    return [generate(gram, target) for i in range(n)]

def generate_best(n, gram, target):
    sentences = generate_n(n, gram, target)
    #print(sentences)
    pros = [get_probability(s) for s in sentences]
    #print(pros)
    sentence_pro = sorted(zip(sentences, pros), key=lambda x:x[1], reverse=True)

    for s,p in sentence_pro:
        print('sentence:{} with pro: {}'.format(s, p))


if __name__ == '__main__':
    lm_load_2gram()
    generate_best(10, gram=create_grammar(host), target='host')
