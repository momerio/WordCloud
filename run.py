import sys
import os
import argparse
import MecabUse
import WordCloudUse


"""
パラメータ設定
"""

"""出力する品詞リスト"""
OUT_POS_LIST = ["名詞", "形容詞"]


"""ストップワードファイル"""
STOP_WORDS_FILE = "stop_words.txt"

# DEBUG = True
DEBUG = False

"""ディレクトリ設定"""
INPUT_DIRECTORY_PATH = "input_files"
OUTPUT_DIRECTORY_PATH = "."


###########################################################

def debug_out(*kwargs):
    if DEBUG:
        print(kwargs)


def get_args():
    """
    引数を取得する
    """
    parser = argparse.ArgumentParser(description="WordCloudを生成する")
    parser.add_argument("-f", "--file", help="入力ファイルパス",
                        default=None)
    parser.add_argument("-s", "--stop", help="ストップワードファイル名",
                        default=STOP_WORDS_FILE)
    parser.add_argument("-D", "--dir", help="入力ディレクトリパス指定 デフォルト:{}".format(INPUT_DIRECTORY_PATH),
                        default=INPUT_DIRECTORY_PATH)
    parser.add_argument("-O", "--outdir", help="出力ディレクトリパス指定 デフォルト:{}".format(OUTPUT_DIRECTORY_PATH),
                        default=OUTPUT_DIRECTORY_PATH)
    args = parser.parse_args()
    return args


def get_file_name_from_dir():
    """
    ディレクトリに存在するファイル名をすべて取得する
    """
    file_name = None
    args = get_args()
    if args.dir is None:
        return file_name
    else:
        dir_path = args.dir
        # ディレクトリに存在するファイル名をすべて取得する
        file_name_list = [f for f in os.listdir(
            dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        # .txtを削除する
        file_name_list = [f.replace(".txt", "") for f in file_name_list]
        return file_name_list


def main(input_file):
    """
    入力
    """
    args = get_args()
    input_dir = args.dir
    output_dir = args.outdir

    # 入力ファイルパス
    if args.file:
        input_file_path = input_file+".txt"
    else:
        input_file_path = os.path.join(input_dir, input_file + ".txt")

    with open(input_file_path, "r", encoding="utf-8") as f:
        CONTENTS = f.read().splitlines()
        CONTENTS = [content for content in CONTENTS if not content == ""]
    debug_out(CONTENTS)

    """
    形態素解析
    """
    # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
    print("INF: 入力ふぁいるは{}です!".format(input_file_path))
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
        with open(args.stop, "r", encoding="utf-8") as f:
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

    # 出力ファイルパス設定
    OUTPUT_WORDCLOUD_FILE = "wc_{}".format(input_file)
    OUTPUT_FILE_PATH = os.path.join(output_dir, OUTPUT_WORDCLOUD_FILE + ".png")
    print("INF: WordCloudの出力パスは{}ですね".format(OUTPUT_FILE_PATH))

    wordCloudGenerator.out_file_name = OUTPUT_FILE_PATH  # 出力ファイル名
    wordCloudGenerator.wordcloud_draw(wakati_text)  # 出力

    print("INF: 単語の出現頻度を計測しますよぉ……")
    word_freq = wordCloudGenerator.frequency_count(wakati_text)
    debug_out(word_freq)

    # 単語頻出度の出力ファイルパス設定
    OUTPUT_FREQ_FILE = "fq_{}".format(input_file)
    OUTPUT_FREQ_FILE_PATH = os.path.join(output_dir, OUTPUT_FREQ_FILE + ".txt")
    print("INF: 出現頻度ファイルの出力パスは{}ですね".format(OUTPUT_FREQ_FILE_PATH))
    print("INF: 只今っ 出現頻度ファイルを出力していますっ")
    with open(OUTPUT_FREQ_FILE_PATH, "w", encoding="utf-8") as f:
        for word, freq in word_freq.most_common():
            f.write(word + "," + str(freq) + "\n")


if __name__ == "__main__":
    args = get_args()
    if args.file:
        # fオプション(個別ファイル)が指定されている場合
        # args.fileから.txt を削除したファイル名を取得
        file_name_list = [args.file.replace(".txt", "")]
    else:
        # fオプションが指定されていない場合
        file_name_list = get_file_name_from_dir()  # 入力ディレクトリ内のファイル名
        print(f"INF: 入力ファイルは{file_name_list}です")

    for input_file in file_name_list:
        main(input_file)

    print("INF: すべて終わりました!! お疲れさまでしたぁ～ ご主人しゃまっ!!")
