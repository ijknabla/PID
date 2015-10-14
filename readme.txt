目的：
センサーとアクチュエーターでステージをPID制御すること

内容：
DAQmx(※1)のPythonラッパを利用して、National Instruments製DAQを制御するための
インターフェースとなるクラスや関数。
および、
実際に制御するコード、あるいは得たデータを処理するための構造（これはPID制御に特化した部分）

使用ハードウェア
NI DAQ USB X 6363

環境：
Python3.4

依存パッケージ：
PyDAQmx		DAQmxのPythonラッパ(※2)
numpy		多次元配列ライブラリ、要素の取得や演算が標準のものより簡潔で、スピードも速い
scipy		numpy配列に対して、フーリエ変換、関数フィッティングなどを行う。(numpyが必要)
matplotlib	numpy配列からグラフの画像を生成する(numpyが必要)


(※1) DAQmxとは
NI社製DAQへのAPI。対応環境は
C, C++
.NET Framework (C#, VB)
Labview
igor

たぶんCのAPIをそれぞれの環境にラップして動いていると思われる。異環境間でも、同じ関数名が使われているので、
最も普及しているLabviewのVI図をヒントに調べるとよいと思われる。

(※2) PyDAQmx DAQmxのPythonラッパ
標準的なPythonはCで実装されている(CPython)。
Pythonのディレクトリ内にあるPython.hをインクルードし、そこで定義されたPythonObject型を受け取り、
返すような関数を実装する。これはCPythonからインポートできる。

C言語のライブラリをビルドして、Python側から呼ぶことも可能である。この場合、各関数はC言語の型を要求
するので、呼び出すPythonは値をC互換な型に変換して呼び出し、戻り値をまたPythonの値に変換しなければならない。
このために用いるPythonの標準ライブラリがctypesであり、たとえば、ctypes.c_int32()でcのint型(32bit)の変数を宣言できる。
このctypesのクラスは、組み合わせることでCの型と同等の表現力を持つ（ポインタ、関数のプロトタイプ、構造体...etc）

つまり、C言語をラップした関数に、Pythonのオブジェクトを渡しても十分に働くし、ポインタを用いた参照渡しが必要な
場合でも、ctypesの型にしてbyref()で参照を取り出すことで機能させることができる。

PyDAQmxでは、int32やfloat64などの名前で、ctypesの型を内包させているため、PyDAQmxをインポートするのみで対応が可能。
PyDAQmxのドキュメントを見て分かるとおり、基本的にC言語のDAQmxのドキュメントと一対一の対応がある。