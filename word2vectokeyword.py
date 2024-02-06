import re
import os
import jieba
import gensim

# 创建停用词列表
stopword_list=[]
with open (r".\StopWords.txt","r",encoding='utf-8') as f:#打开停用词文件
    lines=f.readlines()
for line in lines:
    stopword=line.strip()
    stopword_list.append(stopword)

# 获取文本分词后列表
def cut_words_list(text):
    PureText = ''
    for word in text:
        if word not in stopword_list:
            PureText += word
    WordList = jieba.lcut(PureText)
    return WordList

filePath="E:\伍彬\基金\政府工作报告\地级市工作报告2003-2023txt版本\市级2003-2023\\"
fileNames=os.listdir(filePath)
filterNames=[]
for name in fileNames:
    year=int(''.join(re.findall('[0-9]', name)))
    if year>2014:
        filterNames.append(name)
print(filterNames)
text_list=[]
for name in fileNames:
    # 读入txt文件，按句号分句
    with open(filePath+name, "r", encoding="utf-8") as file:
        text = file.read()
        text = ''.join(re.findall('[\u4e00-\u9fff]+|。', text))
    text_list.extend(text.split("。"))

# 对每一个句子去停用词
text_list2 = [cut_words_list(text) for text in text_list]

# CBOW建模
model = gensim.models.Word2Vec(text_list2, vector_size=100, window=5, min_count=10, sg=0)
# 查看 “科学” 的词向量
print(model.wv.get_vector("智能化"))
# 查看与“科学”最相近的前10个词
print(model.wv.most_similar("智能化", topn=20))
# 查看“科学”与“汪淼”的相似度
print(model.wv.similarity("智能", "智能"))

# # Skip-Gram建模
# model = gensim.models.Word2Vec(text_list2, vector_size=100, window=5, min_count=5, sg=1)
# # 查看 “科学” 的词向量
# print(model.wv.get_vector("智能"))
# # 查看与“科学”最相近的前10个词
# print(model.wv.most_similar("智能", topn=10))
# # 查看“科学”与“汪淼”的相似度
# print(model.wv.similarity("智能", "智能"))