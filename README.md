pytlite
=======

Control Patlite Signal Tower from Python

パトライト社のネットワーク対応型警告灯"**PHN-3FBE1**"をPythonから操作するためのモジュールです．

"**PHN-3FBE1**"及び，"**PHN-3FB**"を操作することができます．

プロトコルは**TCP**，**UDP**共に対応しています．

http://www.patlite.jp/product/phn_3fbe1.html

機能制限等
==========

* 設定変更を行うことはできません

利用例
==========

```python
from pytlite import Patlite

p = Patlite("10.0.0.1",10000,"TCP")

# 現在の点灯状態を表示
p.print_status()

# 赤色点灯
p.red = p.ON

# 緑色点滅
p.green = p.BLINK

# ブザー(短い連続音)
p.buzzer = p.OFF

# 現在の点灯状態を表示
p.print_status()

p.close()
```
