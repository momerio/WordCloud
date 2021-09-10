# WordCloud


["名詞", "形容詞"]の基本形を出力する(run.pyでパラメータを変更可能)

ストップワードはstop_words.txtに一行一語で登録可能．

## 実行方法
run.pyを実行すれば良い．

なお，形態素解析器のMeCabが必須．

## 生成されるファイル
* `wc_` から始まるファイル → WordCloud可視化ファイル
* `fq_` から始まるファイル → 単語頻出度のファイル

## オプション
* [-D --dir] 入力ファイルを格納するディレクトリ
* [-O --outdir] 出力ファイルを格納するディレクトリ
* [-s --stop] ストップワードのファイルパス

## 実行例
` python .\run.py -D input -O output `


## 出力例
↓neko.txt(吾輩は猫であるの一部)をWordCloudした結果↓
![WordCloud_sample](https://github.com/momerio/WordCloud/blob/22881134f26ccd443510163cd418e1d458ed8f70/sample_image.png "word cloud sample")
