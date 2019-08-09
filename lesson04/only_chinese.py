import re
import jieba

f_in = open('zhwiki_simple.txt', 'r', encoding='utf8')
f_out = open('zhwiki_only_simple_and_cut.txt', 'w', encoding='utf8')
line = f_in.readline()

while line:
    if line == '\n':
        line = f_in.readline()
        continue
    pattern = re.compile('[\u4E00-\u9FA5]')
    result = pattern.findall(line)
    line = ''.join(result)
    line = jieba.cut(line)
    new_line = ' '.join(line)
    f_out.writelines(new_line)
    f_out.write('\n')
    line = f_in.readline()

f_in.close()
f_out.close()
