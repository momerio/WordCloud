import MeCab
from wordcloud import WordCloud


def read_file():
    ##### ファイル読み取り #####
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        CONTENT = f.read()
    return CONTENT


def mecab_wakati(text):
    # 形態素解析を行う
    tagger = MeCab.Tagger("-Owakati")  # 分かち書き
    parse = tagger.parse(text)
    return parse


class WordCloudGenerator:
    """
    WordCloud
    """
    out_file_name = ""

    def __init__(self, font_path, background_color, width, height, collocations,
                 stopwords, max_words, regexp):
        """
        出力パラメータ初期化
        """
        self.font_path = font_path
        self.background_color = background_color
        self.width = width
        self.height = height
        self.collocations = collocations
        self.stopwords = stopwords
        self.max_words = max_words
        self.regexp = regexp

    def wordcloud_draw(self, parse):
        # wordcloud
        wordcloud = WordCloud(font_path=self.font_path, background_color=self.background_color, width=self.width, height=self.height,
                              collocations=self.collocations, stopwords=self.stopwords, max_words=self.max_words, regexp=self.regexp)

        wordcloud.generate(parse)
        wordcloud.to_file(self.out_file_name)


if __name__ == "__main__":
    # 入力テキストファイル
    FILE_NAME = "neko.txt"
    OUT_FILE_NAME = "output_wordcloud.png"

    #### パラメータ ####
    STOP_WORDS = ["　"]  # ストップワード
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 500  # 出力画像の幅
    HEIGHT = 500  # 出力画像の高さ
    FONT_FILE = "C:\Windows\Fonts\MSGOTHIC.TTC"  # フォントファイルのパス

    CONTENT = read_file()  # ファイル読み取り
    wakati = mecab_wakati(CONTENT)  # 形態素解析

    wordCloudGenerator = WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                            stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati)  # 出力
