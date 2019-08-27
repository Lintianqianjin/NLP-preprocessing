from nltk import word_tokenize,sent_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def themeAnalyze(textIn):
    '''
    对输入段落分句、然后分词（包含词性标注）、去停用词和标点符号
    将所有【单个词语】、【连续的名词】、【连续（单个）形容词修饰连续（单个）名词】三类都作为词进行计数
    根据问题样例，发现高频词text也没有输出，设定只返回长度大于1的最高频的三个词语

    (扩展缩写词，用正则即可，本例不知道要扩展啥缩写词，此步省略)

    :param textIn: [[],[],[]...]的结构；是一个段落的多行
    :return: 长度大于1最高频的三个词语

    本方法时间复杂度较高，有待改进...
    '''

    sentences = []
    for line in textIn:
        sentences.extend(sent_tokenize(line))

    stop_words = set(stopwords.words('english'))
    Punctuation = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','“','”']

    def notStopAndPunctuation(word):
        notStop = word[0] not in stop_words
        # notPunctuation = re.match('^[a-zA-z]+','fixed-length'[0]).group()
        notPunctuation = word[0] not in Punctuation
        # print('fixed'[0])
        # print(notPunctuation)
        # exit()
        return (notStop and notPunctuation)

    def lemmatize_all(sentence):
        wnl = WordNetLemmatizer()
        # print(pos_tag(word_tokenize(sentence)))
        for word, tag in pos_tag(word_tokenize(sentence)):
            word = word.lower()
            if tag.startswith('N'):
                yield wnl.lemmatize(word, pos=wordnet.NOUN), tag
            elif tag.startswith('V'):
                yield wnl.lemmatize(word, pos=wordnet.VERB), tag
            elif tag.startswith('J'):
                yield wnl.lemmatize(word, pos=wordnet.ADJ), tag
            elif tag.startswith('R'):
                yield wnl.lemmatize(word, pos=wordnet.ADV), tag
            else:
                yield word, tag

    sent_words = []
    for sent in sentences:
        originWords = list((lemmatize_all(sent)))
        sent_words.append(list(filter(notStopAndPunctuation,originWords)))

    # print(sent_words)

    # JJ + NN(s) 形容词修饰名词
    # 连续NNP 专有名词
    # 名词修饰名词

    word_dict = dict()
    for sent in sent_words:
        words = []
        posTags = []

        for w in sent:
            words.append(w[0])
            posTags.append(w[1])

        for w in words:
            if w not in word_dict:
                word_dict[w] = 1
            else:
                word_dict[w] += 1

        mainIndex = len(sent)-1

        curCombinedWord = []

        while mainIndex > 0:
            if posTags[mainIndex].startswith('NN'):
                curCombinedWord.insert(0,[words[mainIndex]])
                curIndex = mainIndex - 1
                while True:
                    isConsitantNN = posTags[curIndex].startswith('NN') and posTags[curIndex + 1].startswith('NN')
                    if posTags[curIndex].startswith('JJ') or isConsitantNN:
                        for consitantWord in curCombinedWord:
                            consitantWord.insert(0,words[curIndex])

                            w = ' '.join(consitantWord)
                            if w not in word_dict:
                                word_dict[w] = 1
                            else:
                                word_dict[w] += 1

                        if isConsitantNN:
                            curCombinedWord.append([words[curIndex]])

                        curIndex -= 1
                    else:
                        curCombinedWord.clear()
                        mainIndex = curIndex
                        break

            else:
                mainIndex -= 1

    sortedWords = sorted(word_dict.items(),key=lambda item:item[1],reverse=True)

    # print(sortedWords)
    returnAmount = 0
    willReturn = []
    for item in sortedWords:
        if len(item[0].split(' ')) > 1:
            willReturn.append(item)
            returnAmount+=1
        if returnAmount == 3:
            break
    return willReturn

if __name__ == '__main__':
    text = open('data/textIn','r',encoding='utf-8').readlines()

    result = themeAnalyze(text)
    print(result)