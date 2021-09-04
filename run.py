import MecabUse as mecab
import WordCloudUse

"""
パラメータ設定
"""
INPUT_FILE = 'neko.txt'
OUT_FILE_NAME = "output_wordcloud.png"  # 出力ファイル

OUT_POS_LIST = ["名詞", "形容詞"]  # 出力品詞リスト
# OUT_POS_LIST =["名詞", "動詞", "形容詞", "形容動詞"]
# OUT_POS_LIST=["名詞", "形容詞", "形容動詞"]

# DEBUG = True
DEBUG = False


def debug_out(*kwargs, debug=True):
    if DEBUG:
        print(kwargs)


"""
入力
"""
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    CONTENTS = f.read().splitlines()
    CONTENTS = [content for content in CONTENTS if not content == ""]
debug_out(CONTENTS, debug=DEBUG)


"""
形態素解析
"""
# 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
print("INF: 形態素解析中ですよぉ……")
surfaces = []
for content in CONTENTS:
    morphologic_results = mecab.morphological_analysis(content)
    for mr in morphologic_results:
        if mr[1] in OUT_POS_LIST:
            if mr[-3] not in ["*"]:
                surfaces.append(mr[-3])  # 基本形
debug_out(surfaces, debug=DEBUG)

wakati_text = " ".join(surfaces)
print("INF: 形態素解析終了しましま!")

"""
WORD CLOUDの実行
"""
print("INF: WordCloudをやってみますよっ! ご主人しゃまっ!!")
print("DBG: 出力品詞 -> {}".format(OUT_POS_LIST))

#### パラメータ ####
STOP_WORDS = ["　"]  # ストップワード
MAX_WORDS = 2000  # 出力個数の上限
WIDTH = 1000  # 出力画像の幅
HEIGHT = 1000  # 出力画像の高さ
FONT_FILE = "C:\Windows\Fonts\MSGOTHIC.TTC"  # フォントファイルのパス


wordCloudGenerator = WordCloudUse.WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                                     stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化
wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
wordCloudGenerator.wordcloud_draw(wakati_text)  # 出力
print("INF: すべて終わりました!! お疲れさまでしたぁ~ ご主人しゃまっ!!")
