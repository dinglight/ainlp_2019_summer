0. Can you come up out 3 sceneraies which use AI methods?

Ans: 机器翻译, 无人驾驶, 自动问答系统

1. How do we use Github; Why do we use Jupyter and Pycharm;

Ans: 代码存储在github
     使用jupyter 做笔记
     Pycharm是编写python程序的IDE.

2. What's the Probability Model?

Ans:以概率的方式建立的模型

3. Can you came up with some sceneraies at which we could use Probability Model?

Ans:自然语言模型，天气预报模型

4. Why do we use probability and what's the difficult points for programming based on parsing and pattern match?

Ans:模式或规则太多了，不可能定义完备的规则。

5. What's the Language Model;

Ans:利用统计的方法对语言进行数学建模， 通常构建为字符串s的概率分布p(s)

6. Can you came up with some sceneraies at which we could use Language Model?

Ans:中文分词，机器翻译

7. What's the 1-gram language model;

Ans:只统计单个词的概率。
```
P(s) = p(w1)*p(w2)*p(w3)*p(w4)
```

8. What's the disadvantages and advantages of 1-gram language model;

Ans:优点：计算简单，缺点：不能反映语言的上下文信息，构成的句子不准确

9. What's the 2-gram models;

Ans:一个词出现的概率由它前面的一个词决定
```
P(s) = p(w1)*p(w2|w1)*p(w3|w2)*p(w4|w3)
```
