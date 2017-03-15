# GoWhere
Semantic Annotation of Mobility Data using Social Media

##dataset
在[http://www.ark.cs.cmu.edu/GeoText](http://www.ark.cs.cmu.edu/GeoText)该网站上获取了我的数据集。之后将数据集作处理，筛选出纬度在[38,42]，经度[-76,-72]范围内的数据，即提取了New York附近的数据集。
将数据字段重命名如下：

| 字段名 	    | 含义  			|
| ------------ 	| -------------	|
| userId 		| 用户ID 		|
| time		 	| 发布tweet的时间	|
| location		| 位置			|
| lati			| 纬度			|
| long			| 经度			|
| tweets		| tweet的内容	|

其中位置字段为经度纬度合并在一起的字段，因原数据集所带，在此并没有去除掉。

由于location存在编码问题，于是手动删除了这一列，从而方便后面的数据处理。