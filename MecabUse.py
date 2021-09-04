"""
Mecab
"""
import subprocess
import re


def _mecab(text, size="10000000"):
    """
    mecab操作関数
    @param: text テキスト, size 最大文字数
    @return: Mecab型テキスト
    """
    output = subprocess.run(["mecab", "-b", size], input=text+"\n",
                            encoding="utf-8", stdout=subprocess.PIPE)
    return output.stdout


def morphological_analysis(text: str) -> list:
    """
    形態素解析する
    @return: double list e.g.) [["すもも", "名詞", "一般", "*", "*", "*", "*", "すもも", "スモモ", "スモモ"]]
    """
    mData = _mecab(text)
    dataList = [re.split(r"[\t,', ']", idx) for idx in mData.split("\n")]
    dataList = [idx
                for idx in dataList if len(idx) > 1]  # delete EOS or None
    return dataList


def wakati(parse: list) -> str:
    """
    形態素解析リストを分かち書きに変換する
    @param: parse 形態素解析結果リスト
    @return: 分かち書き文字列
    """
    return " ".join(parse)


if __name__ == "__main__":

    with open("neko.txt", "r", encoding="utf-8") as f:
        CONTENTS = f.read().splitlines()
        CONTENTS = [content for content in CONTENTS if not content == ""]
    print(CONTENTS)

    # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
    print("INF: 形態素解析中ですよぉ……")
    surfaces = []
    for content in CONTENTS:
        morphologic_results = morphological_analysis(content)
        for mr in morphologic_results:
            surfaces.append(mr[0])
    print(surfaces)
