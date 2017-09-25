# Pinyin2Hanzi
将一串拼音转换成一串中文汉字，类似一个输入法

原始实现是[搜喵输入法](https://github.com/crownpku/Somiao-Pinyin), 在其基础上进行了改造

# 训练模型
### 构建训练数据
```python
from p2h.build_corpus import build_corpus

build_corpus()
```

##### 原始语料
```
米家的忠实粉丝，这是第五次买米家的手机了，希望这次也是棒棒哒。
先用几天，过后追评。
官方太小气，连个膜也不给。
手机还不错。
```

##### 训练数据
```
mijiadezhongshifensi	米_家__的_忠____实__粉__丝_
zheshidiwucimaimijiadeshoujile	这__是__第_五_次_买__米_家__的_手___机_了_
xiwangzheciyeshibangbangda	希_望___这__次_也_是__棒___棒___哒_
xianyongjitian	先___用___几_天___
guohouzhuiping	过__后__追___评___
guanfangtaixiaoqi	官___方___太__小___气_
liangemoyebugei	连___个_膜_也_不_给__
shoujihaibucuo	手___机_还__不_错__
```

### 训练
```python
from p2h.train import train

train()
```

### 使用
```python
from p2h import eval

eval.main()
```


# 实验结果
```
请输入测试拼音：shoujihaixing
手机还行
请输入测试拼音：jiushiganjuedianchibushihennaiyong
就是感觉电池不是很耐用
请输入测试拼音：pingmubixiangxiangzhongdexiaoledian
屏幕比想象中的小了点
请输入测试拼音：sechahenyanzhong
色e差很严重
请输入测试拼音：youhenyanzhongdesecha
又很严重的色差
请输入测试拼音：diyiciyongganjuehenbucuo
第一次用感觉很不错
请输入测试拼音：laonianrenyongzheyehenheshi
老年人用着也很合适
请输入测试拼音：laonianrenyongzheyetingheshide
老年人用着也挺合适的
请输入测试拼音：tebiebangdengjiangjiadenglehaojiu
特别棒等降价等了好久
请输入测试拼音：zhiliangyoudaiyanzheng
质量有待验证
请输入测试拼音：songdedongxizhenshijilei
送的东西真是鸡累
请输入测试拼音：dianhzhilianghaixing
电h质量还行
请输入测试拼音：dianhuazhilianghaixing
电话质量还行
请输入测试拼音：daohuokuaihenmanyi
到货快很满意
请输入测试拼音：lajidongxijingchangsiji
垃圾东西经常死机
请输入测试拼音：
```