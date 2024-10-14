# fetch-bookinfo-from-isbn

画像ファイルを読み込んでバーコード(ISBNコード)を検出し、[国立国会図書館サーチ(NDLサーチ)](https://ndlsearch.ndl.go.jp/) APIを使用してタイトル、著者を取得するPythonプログラム

* ISBNコード読み取り: pyzbar
* 書籍情報検索API: [NDLサーチAPI](https://ndlsearch.ndl.go.jp/help/api) ※営利目的の利用の場合、利用申請が必要
* xmlのパース: xml.etree.ElementTree


## usage

```bash
$ python read_ISBN.py <image_path>
タイトル: ~~~~
著者: _____
# for example...
$ python read_ISBN.py ./images/test.jpeg
タイトル: チク・タク・チク・タク・チク・タク・チク・タク・チク・タク・チク・タク・チク・タク・チク・タク・チク・タク・チク・タク
著者: ジョン・スラデック 著
タイトル: ふたたび嗤う淑女
著者: 中山七里 著
タイトル: ぼぎわんが、来る
著者: 澤村伊智 [著]
```

## その他

個人利用であり、データ利用により収益を得ていません。

images/test.jpegは私が撮影したものです。また、本画像には4つの書影が含まれていますが、うち一つ（『神の悪手』）はなぜか読み取れませんでした。