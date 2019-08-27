import re

from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTAnno,LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser


def union_dict(*dicts):
    '''

    :param dicts:
    :return:
    '''
    _keys = set(sum([list(obj.keys()) for obj in dicts], []))
    # print(_keys)
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key, 0) for obj in dicts])
    return _total


def getLTlineText(LTline):
    '''

    :param LTline: LTTextLine object
    :return:
    '''
    line = ''
    length = len(LTline._objs)
    for index, char in enumerate(LTline._objs):
        if isinstance(char,LTAnno) and index < length-1 and (LTline._objs[index-1].height - LTline._objs[index+1].height) > 5:
            continue
        else:
            line += char.get_text()

    return re.sub('auto ','auto',line)


def isAuthors(textInBox):
    tags = pos_tag(word_tokenize(textInBox))
    NNP_CD_Count = 0
    num_words = 0
    for tag in tags:
        if tag[1].isalpha():
            num_words+=1
        if tag[1] == 'NNP' or tag[1] == 'CD':
            NNP_CD_Count+=1
    if NNP_CD_Count/num_words>0.75:
        return True
    else:return False


with open("utils/words.txt") as word_file:
    words = set(word.strip().lower() for word in word_file)

def isEnglishWord(word):
    return word.lower() in words

# def isEnglishWord(word):
#     '''
#     :param word:
#     :return:
#     '''
#     return wordnet.synsets(word)

class extractPdfText:

    def __init__(self, path):
        '''

        :param path: pdf file path
        '''

        # Open a PDF file.
        # Create a PDF parser object associated with the file object.
        self.parser = PDFParser(open(path, 'rb'))

        # Create a PDF document object that stores the document structure.
        self.document = PDFDocument(self.parser)

        # Check if the document allows text extraction. If not, abort.
        if not self.document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object that stores shared resources.
        self.rsrcmgr = PDFResourceManager()

        # Set parameters for analysis.
        self.laparams = LAParams(boxes_flow=0.75, char_margin=3.0, word_margin=0.1, line_margin=0.45)

        # Create a PDF page aggregator object.
        self.device = PDFPageAggregator(self.rsrcmgr, laparams=self.laparams)

        # creat a PDF Page Interpreter object
        self.interpreter = PDFPageInterpreter(self.rsrcmgr, self.device)

        # --------------------------------------------------------------

        self.pages = list(PDFPage.create_pages(self.document))
        self.guessDocumentMainFontandSize()
        # self.fontStatDict = dict()
        # --------------------------------------------------------------

    def isLTTextBox(self, element):
        '''

        :param element: an object in a LTPage object
        :return: LTTextBoxs in this LTPage object
        '''
        return isinstance(element, LTTextBox)

    def getCharSizeAndFontDict(self, TextBox):
        '''

        :param TextBox: LTTextBox object
        :return:
        '''
        fontDict = dict()
        for textLine in TextBox._objs:
            # textLine LTTextLine object
            for char in textLine._objs:
                # if LTAnno ignore
                if isinstance(char, LTAnno):
                    continue
                # char LTchar objects
                fontName = char.fontname
                size = round(char.height, ndigits=2)
                # count char style
                if (fontName, size) not in fontDict:
                    fontDict[(fontName, size)] = 1
                else:
                    fontDict[(fontName, size)] += 1

        return fontDict

    def getMainFontSytle(self, fontDict):
        '''

        :param fontDict: # key: (fontName,fontSize) value: amount
        :return:
        '''
        # if sort time complex nlog2n
        maxCount = 0
        mainStyle = None
        for key in fontDict:
            if fontDict[key] > maxCount:
                maxCount = fontDict[key]
                mainStyle = key

        return mainStyle

    def guessDocumentMainFontandSize(self):
        '''

        :return: (guessed) body text font size and font type
        '''

        # one or two pages e.g. poster guess from all text
        # short paper long paper guess from pages without last several pages
        # a way to delete references(has no idea about better and simple method)
        num_pages = len(self.pages)
        if num_pages <= 4:
            guessPages = self.pages
        elif num_pages<= 10:
            guessPages = self.pages[:-2]
        else:
            guessPages = self.pages[:-3]
        # guessPages = self.pages
        # key: (fontName,fontSize) value: amount
        fontDict = dict()

        for page in guessPages:
            pageLayout = self.pageLayout(page)

            for textBox in pageLayout:
                # textBox LTTextBox object
                curFontDict = self.getCharSizeAndFontDict(textBox)
                fontDict = union_dict(fontDict, curFontDict)

        # call getMainFontSytle return main Style (which amount is max)
        DocumentMainFontandSize = self.getMainFontSytle(fontDict)

        self.fontWithText = {font_account[0]: []
                        for font_account in sorted(fontDict.items(), key=lambda item: item[1], reverse=True)[:3]}

        self.documentMainFontandSize = DocumentMainFontandSize

        return DocumentMainFontandSize

    def pageLayout(self, page):
        '''
        :param page: a PDF page object, return by PDFPage.create_pages
        :return: LTTextBoxes in this page
        '''

        self.interpreter.process_page(page)

        # receive the LTPage object for the page.
        layout = self.device.get_result()
        layout = list(filter(self.isLTTextBox, layout))

        return layout

    def extractBodyTextInSinglePage(self, layout):
        '''

        :param layout:
        :return:
        '''
        # curPageFontDict = dict()
        # bodyTextInThisPage = []

        for textBox in layout:
            curTextBoxFontDict = self.getCharSizeAndFontDict(textBox)
            curTextBoxMainFont = self.getMainFontSytle(curTextBoxFontDict)

            if curTextBoxMainFont in self.fontWithText:
                textInBox = self.concatLine([getLTlineText(LTline).strip().replace('  ', ' ')
                                 for LTline in textBox._objs
                                 if (not LTline.get_text().lower().startswith('keywords:'))
                                 and LTline.height - curTextBoxMainFont[1] > -1])
                if not isAuthors(textInBox):
                    self.fontWithText[curTextBoxMainFont].extend([textInBox])

    def checkIsMeaningfulText(self,multiLines):
        '''
        check whether the text is meaningful text such as bodytext, abstract
        :param multiLines:
        :return:
        '''

    def parseAllPages(self):
        '''

        :return:
        '''

        for index, page in enumerate(self.pages):
            layout = self.pageLayout(page)
            self.extractBodyTextInSinglePage(layout)

        for font in self.fontWithText:
            concatTetx = self.concatLine(self.fontWithText[font])
            self.fontWithText[font] = concatTetx

    def concatLine(self, multiLines):
        '''
        multiLines: list
        :param multiLines:
        :return:
        '''
        num_lines = len(multiLines)

        paragraph = ''

        for index, line in enumerate(multiLines):
            if line:
                if index < num_lines - 1:
                    # some line end with space but some do not
                    line = re.sub('ﬂ |ﬂ', 'fl', line.strip())
                    line = re.sub('ﬁ |ﬁ', 'fi', line.strip())
                    # some end with -
                    wordsInLine = line.split(' ')
                    firstWordInNextLine = multiLines[index + 1].strip().split(' ')[0]

                    if wordsInLine[-1].endswith('-'):
                        # concat two word or two parts in one word


                        # if without -, it is a word and first Word In Next Line is a word too
                        # consider - concats two word
                        concatWord = wordsInLine[-1].strip('-') + re.sub(':|\.','',firstWordInNextLine)
                        if isEnglishWord(concatWord):
                            # two parts in one word
                            paragraph += line.strip('-')
                        else:
                            paragraph += line
                    else:

                        if wordsInLine[-1][-1] in ['.', '!', '?']:
                            # aaa = wordsInLine[-4:-1]
                            if wordsInLine[-1][-4:-1] == 'Fig':
                                paragraph += line + ' '
                            else:
                                paragraph += line + '\n'
                        else:

                            if wordsInLine[-1].isupper() and isEnglishWord(firstWordInNextLine) and firstWordInNextLine[0].isupper():
                                paragraph += line + '\n'
                            else:
                                paragraph += line + ' '




                else:
                    paragraph += line.strip() + '\n'

        return paragraph

    def extractAbstract(self):
        firstPage = self.pages[0]
        layout = self.pageLayout(firstPage)


if __name__ == '__main__':

    pdfextractor = extractPdfText('data/pdf1.pdf')

    pdfextractor.parseAllPages()

    for index, key in enumerate(pdfextractor.fontWithText):
        if index == 0:
            print('-----------------------------------------正文开始-----------------------------------------')
            print(pdfextractor.fontWithText[key])
            print('-----------------------------------------正文结束-----------------------------------------')
        elif index == 1:
            print('-----------------------------------------图解等附文开始-----------------------------------------')
            print(pdfextractor.fontWithText[key])
            print('-----------------------------------------图解等附文结束-----------------------------------------')
        elif index ==2:
            print('-----------------------------------------摘要开始-----------------------------------------')
            print(pdfextractor.fontWithText[key])
            print('-----------------------------------------摘要结束-----------------------------------------')
