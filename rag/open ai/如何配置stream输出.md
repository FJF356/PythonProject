1. 启用stream输出
```
streaming=True,
```
2. 基本语法：
for 变量 in 可迭代对象:
    循环体
示例：
```
 # 遍历列表
for item in [1, 2, 3]:
    print(item)
 # 遍历字符串
for char in "hello":
    print(char)
 # 遍历生成器（流式输出）
for chunk in llm.stream(question):
    print(chunk.content)
```