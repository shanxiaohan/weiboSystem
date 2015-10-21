训练模型的过程：
1）model_process.py中的readIn()函数
从weibo_unique表中读取增量数据，存到/home/shanxiaohan/tmsvm/memememememememememe/mysqldata/data文件（'w'方式打开会覆盖原来数据）

2）执行/home/shanxiaohan/tmsvm/memememememememememe/predict.py文件训练模型，输出结果文件到/home/shanxiaohan/tmsvm/memememememememememe/data.result
可以选取index[]中的下标代表哪几列保留到data.result中，这里选取了全部数据，共13列

3）model_process.py中的writeOut()函数从data.result读入文件，写入analyse_result表


微博去重no_repeat.py文件，将weibo表中新增的记录插入weibo_unique表中