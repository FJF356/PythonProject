"""
超级简单的向量数据库demo - 面向过程版本
就像写脚本一样，一行一行往下执行
"""

import numpy as np

# ========== 第1步：创建一个"数据库" ==========
# 就是一个空字典，用来存数据
# key是id，value是向量
database = {}

print("=== 1. 创建了一个空数据库 ===")
print(f"数据库里有 {len(database)} 条数据")
print()


# ========== 第2步：添加数据 ==========
# 创建几个向量（随机生成）
vector_1 = np.array([1.0, 2.0, 3.0])  # 向量1
vector_2 = np.array([4.0, 5.0, 6.0])  # 向量2
vector_3 = np.array([1.1, 2.1, 3.1])  # 向量3（和向量1很相似）

# 把向量存到数据库里
database["doc_1"] = vector_1
database["doc_2"] = vector_2
database["doc_3"] = vector_3

print("=== 2. 添加了3条数据 ===")
print(f"doc_1: {database['doc_1']}")
print(f"doc_2: {database['doc_2']}")
print(f"doc_3: {database['doc_3']}")
print()


# ========== 第3步：查询数据（根据id获取） ==========
print("=== 3. 查询数据 ===")
id_to_find = "doc_1"
if id_to_find in database:
    found_vector = database[id_to_find]
    print(f"找到了 {id_to_find}: {found_vector}")
else:
    print(f"没找到 {id_to_find}")
print()


# ========== 第4步：计算相似度 ==========
# 两个向量越"像"，点积越大
def calculate_similarity(v1, v2):
    """计算两个向量的相似度（点积）"""
    return np.dot(v1, v2)

print("=== 4. 计算相似度 ===")
query_vector = np.array([1.0, 2.0, 3.0])  # 查询向量
print(f"查询向量: {query_vector}")
print()

# 和数据库里的每个向量比一比
for id, vector in database.items():
    similarity = calculate_similarity(query_vector, vector)
    print(f"和 {id} 的相似度: {similarity:.2f}")
print()


# ========== 第5步：找最相似的 ==========
print("=== 5. 找最相似的 ===")
best_id = None
best_similarity = -999999

for id, vector in database.items():
    similarity = calculate_similarity(query_vector, vector)
    if similarity > best_similarity:
        best_similarity = similarity
        best_id = id

print(f"最相似的是: {best_id}, 相似度: {best_similarity:.2f}")
print()


# ========== 第6步：更新数据 ==========
print("=== 6. 更新数据 ===")
id_to_update = "doc_1"
new_vector = np.array([10.0, 20.0, 30.0])

if id_to_update in database:
    database[id_to_update] = new_vector
    print(f"更新了 {id_to_update}: {database[id_to_update]}")
else:
    print(f"不存在 {id_to_update}")
print()


# ========== 第7步：删除数据 ==========
print("=== 7. 删除数据 ===")
id_to_delete = "doc_2"

if id_to_delete in database:
    del database[id_to_delete]
    print(f"删除了 {id_to_delete}")
else:
    print(f"不存在 {id_to_delete}")

print(f"现在数据库里有 {len(database)} 条数据")
print()


# ========== 第8步：查看所有数据 ==========
print("=== 8. 查看所有数据 ===")
for id, vector in database.items():
    print(f"{id}: {vector}")
