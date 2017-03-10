# 论文阅读记录
## 一、论文： Semantic Annotation of Mobility Data using Social Media
### 1.论文核心思想
&emsp &emsp 对用户轨迹数据和周围社交媒体的数据使用核密度估计的方法，筛选出概率最高的几个词语，从而对用户的真实目的做推断。
### 2. 背景

geo-tagged tweets和mobility data日益增多，可以让我们semantically understand <b>why a person travels to a location at particular time?</b>

社交媒体的数据非常杂乱，问题的关键就是要找到正确的模型来处理这个问题。本文使用了三种方法：frequency-based method, Gaussian mixtured model, and kernel density estimation(KDE). 对比三种方法之后，最终选择了KDE。

目前方法的缺点如下：

<li> 只使用了mobility data没有使用其他的data
<li> static annotation, 同一个地点不同时间标注了相同的语义

### 3. 问题

问题输入： 用户轨迹数据 + Geo-tagged tweets from crowd

问题输出： 对用户轨迹的语义标注(Annotation Document)

















