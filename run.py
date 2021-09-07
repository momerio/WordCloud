import MecabUse
import WordCloudUse


"""
パラメータ設定
"""
"""入力テキストファイル"""
INPUT_FILE = "neko.txt"

"""出力テキストファイル"""
OUT_FILE_NAME = "output_wordcloud.png"

"""出力単語頻度ファイル"""
OUT_FREQ_FILE = "out_freq_.txt"

"""出力する品詞リスト"""
OUT_POS_LIST = ["名詞", "形容詞"]

"""ストップワードファイル"""
STOP_WORDS_FILE = "stop_words.txt"

DEBUG = True
DEBUG = False


###########################################################

def debug_out(*kwargs):
    if DEBUG:
        print(kwargs)


def main():
    """
    入力
    """
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        CONTENTS = f.read().splitlines()
        CONTENTS = [content for content in CONTENTS if not content == ""]
    debug_out(CONTENTS)

    """
    形態素解析
    """
    # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
    print("INF: 形態素解析中ですよぉ……")
    surfaces = []
    for content in CONTENTS:
        morphologic_results = MecabUse.morphological_analysis(content)
        for mr in morphologic_results:
            if mr[1] in OUT_POS_LIST:
                if mr[-3] not in ["*"]:
                    surfaces.append(mr[-3])  # 基本形
            # surfaces.append(mr[0])
    debug_out(surfaces)

    wakati_text = " ".join(surfaces)
    print("INF: 形態素解析終了しましま!")

    """
    WORD CLOUDの実行
    """

    #### WordCloudのパラメータ ####
    try:
        print("INF: STOP WORDSファイルを開きますっ! ファイルの名前は{}ですっ".format(STOP_WORDS_FILE))
        with open(STOP_WORDS_FILE, "r", encoding="utf-8") as f:
            STOP_WORDS = set(f.read().splitlines())
    except FileNotFoundError:
        print("WAR: STOP WORDSファイルが見つかりませんでした……")
        STOP_WORDS = set()
    MAX_WORDS = 2000  # 出力個数の上限
    WIDTH = 1000  # 出力画像の幅
    HEIGHT = 1000  # 出力画像の高さ
    FONT_FILE = "C:\Windows\Fonts\MSGOTHIC.TTC"  # フォントファイルのパス

    print("INF: WordCloudをやってみますよっ! ご主人しゃまっ!!")
    wordCloudGenerator = WordCloudUse.WordCloudGenerator(font_path=FONT_FILE, background_color="white", width=WIDTH, height=HEIGHT, collocations=False,
                                                         stopwords=STOP_WORDS, max_words=MAX_WORDS, regexp=r"[\w']+")  # WordCloud初期化

    wordCloudGenerator.out_file_name = OUT_FILE_NAME  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati_text)  # 出力

    print("INF: 単語の出現頻度を計測しますよぉ……")
    word_freq = wordCloudGenerator.frequency_count(wakati_text)
    debug_out(word_freq)

    print("INF: 只今っ 出現頻度ファイルを出力していますっ")
    with open(OUT_FREQ_FILE, "w", encoding="utf-8") as f:
        for word, freq in word_freq.most_common():
            f.write(word + "," + str(freq) + "\n")


if __name__ == "__main__":
    main()
    print("INF: すべて終わりました!! お疲れさまでしたぁ～ ご主人しゃまっ!!")
