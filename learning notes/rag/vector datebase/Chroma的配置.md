类的构造函数:
`def __init__(self, collection_name: str = "default", persist_directory: str = "./chroma_data"):`
def :定义函数  声明这是一个函数/方法
__init__ :构造函数  Python 类的特殊方法，创建对象时自动调用
self :实例自身  指向类的实例  必须作为第一个参数
这是类的 构造函数 ，作用是：

初始化对象
当你创建 ChromaVectorDB 类的实例时，Python 会自动调用这个方法：

```
# 方式1：使用默认值
db = ChromaVectorDB()
# 等价于：db = ChromaVectorDB
(collection_name="default", 
persist_directory="./chroma_data")

# 方式2：自定义参数
db = ChromaVectorDB(
    collection_name="my_docs",
    persist_directory="./my_data"
)
```
设置默认配置
- collection_name="default" ：默认集合名称为 "default"
- persist_directory="./chroma_data" ：默认数据保存在当前目录的 chroma_data 文件夹
创建客户端
# 内存模式(程序结束后，所有数据都会丢失,速度快适合测试)
`self.client = chromadb.Client(`
    `Settings(`
        `anonymized_telemetry=False`
    `)`
`)`
# 持久化模式(数据不会丢失,适合应用)
`import os`
`os.makedirs(persist_directory, exist_ok=True) 

`self.client = chromadb.PersistentClient(`
    `path=persist_directory,`
    `settings=Settings(`
        `anonymized_telemetry=False`
    `)`
`)`