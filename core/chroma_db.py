"""
使用 Chroma 实现的向量数据库
Chroma 是一个开源的向量数据库，使用非常简单

功能：
1. 增删改查向量数据
2. 相似度查询（自动计算）
3. 自动持久化存储
4. 内置嵌入模型支持
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any

class ChromaVectorDB:
    """
    【原理】
    基于 Chroma 的向量数据库封装类。
    Chroma 会自动处理：
    - 向量存储和索引
    - 相似度计算
    - 数据持久化
    
    【类比】
    就像一个智能图书馆系统：
    - Collection = 书架（分类存放）
    - Document = 书籍内容
    - Embedding = 书籍特征向量
    - Metadata = 书籍信息（作者、出版日期等）
    """
    
    def __init__(self, collection_name: str = "default", persist_directory: str = "./chroma_data"):
        """
        【原理】
        初始化 Chroma 客户端和集合。
        
        【参数说明】
        collection_name: 集合名称（类似数据库的表名）
        persist_directory: 数据持久化目录
        
        【示例】
        >>> db = ChromaVectorDB(collection_name="my_docs")
        """
        # 保存持久化路径
        self._persist_directory = persist_directory
        
        # 创建客户端（持久化模式）
        # 使用 PersistentClient 而不是 Client，确保数据持久化
        import os
        os.makedirs(persist_directory, exist_ok=True)  # 确保目录存在
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False  # 关闭匿名数据收集
            )
        )
        
        # 获取或创建集合
        # 集合是 Chroma 中存储向量的基本单位
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "向量数据集合"}
        )
        
        print(f"✅ 已连接到集合: {collection_name}")
        print(f"💾 数据将保存在: {os.path.abspath(persist_directory)}")
    
    # ==================== 增加操作 ====================
    
    def add(self, ids: List[str], documents: List[str], 
            embeddings: Optional[List[List[float]]] = None,
            metadatas: Optional[List[Dict]] = None) -> bool:
        """
        【原理】
        添加数据到向量数据库。
        
        【参数说明】
        ids: 唯一标识符列表，如 ["doc1", "doc2"]
        documents: 文本内容列表，如 ["Hello world", "Python编程"]
        embeddings: 向量列表（可选，如果不提供，Chroma会自动计算）
        metadatas: 元数据列表（可选），如 [{"author": "Alice"}]
        
        【返回值】
        True表示成功
        
        【示例】
        >>> db.add(
        ...     ids=["doc1", "doc2"],
        ...     documents=["Hello", "World"],
        ...     metadatas=[{"type": "greeting"}, {"type": "noun"}]
        ... )
        """
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,  # 如果为None，Chroma会自动使用嵌入模型
                metadatas=metadatas
            )
            print(f"✅ 成功添加 {len(ids)} 条数据")
            return True
        except Exception as e:
            print(f"❌ 添加失败: {e}")
            return False
    
    def add_single(self, id: str, document: str, 
                   embedding: Optional[List[float]] = None,
                   metadata: Optional[Dict] = None) -> bool:
        """
        【原理】
        添加单条数据（便捷方法）。
        
        【示例】
        >>> db.add_single("doc1", "Hello World", metadata={"type": "text"})
        """
        return self.add(
            ids=[id],
            documents=[document],
            embeddings=[embedding] if embedding else None,
            metadatas=[metadata] if metadata else None
        )
    
    # ==================== 查询操作 ====================
    
    def get(self, ids: Optional[List[str]] = None, 
            where: Optional[Dict] = None) -> Dict[str, Any]:
        """
        【原理】
        根据ID或条件获取数据。
        
        【参数说明】
        ids: 要查询的ID列表
        where: 元数据过滤条件，如 {"type": "article"}
        
        【返回值】
        包含 ids, documents, embeddings, metadatas 的字典
        
        【示例】
        >>> result = db.get(ids=["doc1"])
        >>> print(result["documents"])
        """
        try:
            result = self.collection.get(
                ids=ids,
                where=where
            )
            return result
        except Exception as e:
            print(f"❌ 查询失败: {e}")
            return {}
    
    def search(self, query_text: Optional[str] = None,
               query_embedding: Optional[List[float]] = None,
               n_results: int = 3,
               where: Optional[Dict] = None) -> Dict[str, Any]:
        """
        【原理】
        相似度搜索：找到与查询最相似的数据。
        
        【参数说明】
        query_text: 查询文本（Chroma会自动转换为向量）
        query_embedding: 查询向量（如果提供了文本，则不需要）
        n_results: 返回最相似的n个结果
        where: 元数据过滤条件
        
        【返回值】
        包含 ids, documents, embeddings, metadatas, distances 的字典
        
        【示例】
        >>> results = db.search(query_text="Hello", n_results=2)
        >>> for doc, distance in zip(results["documents"][0], results["distances"][0]):
        ...     print(f"{doc}: {distance}")
        """
        try:
            if query_text:
                # 使用文本查询（Chroma自动嵌入）
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results,
                    where=where
                )
            elif query_embedding:
                # 使用向量查询
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                    where=where
                )
            else:
                print("❌ 请提供 query_text 或 query_embedding")
                return {}
            
            return results
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return {}
    
    # ==================== 更新操作 ====================
    
    def update(self, id: str, document: Optional[str] = None,
               embedding: Optional[List[float]] = None,
               metadata: Optional[Dict] = None) -> bool:
        """
        【原理】
        更新指定ID的数据。
        
        【参数说明】
        id: 要更新的标识符
        document: 新的文本内容
        embedding: 新的向量
        metadata: 新的元数据
        
        【示例】
        >>> db.update("doc1", document="New content", metadata={"updated": True})
        """
        try:
            # 构建更新参数
            update_data = {"ids": [id]}
            if document:
                update_data["documents"] = [document]
            if embedding:
                update_data["embeddings"] = [embedding]
            if metadata:
                update_data["metadatas"] = [metadata]
            
            self.collection.update(**update_data)
            print(f"✅ 成功更新 '{id}'")
            return True
        except Exception as e:
            print(f"❌ 更新失败: {e}")
            return False
    
    # ==================== 删除操作 ====================
    
    def delete(self, ids: Optional[List[str]] = None,
               where: Optional[Dict] = None) -> bool:
        """
        【原理】
        删除指定ID或符合条件的数据。
        
        【参数说明】
        ids: 要删除的ID列表
        where: 元数据过滤条件
        
        【示例】
        >>> db.delete(ids=["doc1"])
        >>> db.delete(where={"type": "temp"})  # 删除所有type为temp的数据
        """
        try:
            self.collection.delete(ids=ids, where=where)
            print(f"✅ 成功删除数据")
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False
    
    # ==================== 统计操作 ====================
    
    def count(self) -> int:
        """
        【原理】
        获取集合中的数据总数。
        
        【返回值】
        数据条数
        """
        return self.collection.count()
    
    def peek(self, limit: int = 5) -> Dict[str, Any]:
        """
        【原理】
        查看集合中的前n条数据（不删除）。
        
        【参数说明】
        limit: 查看的数量
        
        【返回值】
        包含数据的字典
        """
        return self.collection.peek(limit=limit)
    
    # ==================== 集合管理 ====================
    
    def clear(self) -> bool:
        """
        【原理】
        清空集合中的所有数据。
        """
        try:
            # 获取所有ID
            all_data = self.collection.get()
            if all_data["ids"]:
                self.collection.delete(ids=all_data["ids"])
            print("✅ 集合已清空")
            return True
        except Exception as e:
            print(f"❌ 清空失败: {e}")
            return False


# ==================== 使用示例 ====================

if __name__ == "__main__":
    """
    完整的 Chroma 向量数据库使用示例
    """
    
    print("=" * 60)
    print("Chroma 向量数据库使用示例")
    print("=" * 60)
    
    # 1. 创建数据库
    print("\n【步骤1】创建数据库")
    db = ChromaVectorDB(
        collection_name="demo_collection",
        persist_directory="./data/chroma_data"
    )
    
    # 2. 添加数据（使用 Chroma 的自动嵌入功能）
    print("\n【步骤2】添加数据")
    db.add(
        ids=["doc1", "doc2", "doc3", "doc4"],
        documents=[
            "苹果是一种红色的水果",
            "香蕉是黄色的水果",
            "樱桃也是红色的水果",
            "胡萝卜是橙色的蔬菜"
        ],
        metadatas=[
            {"category": "fruit", "color": "red"},
            {"category": "fruit", "color": "yellow"},
            {"category": "fruit", "color": "red"},
            {"category": "vegetable", "color": "orange"}
        ]
    )
    
    print(f"数据库中有 {db.count()} 条数据")
    
    # 3. 根据ID查询
    print("\n【步骤3】根据ID查询")
    result = db.get(ids=["doc1"])
    if result.get("documents"):
        print(f"doc1 内容: {result['documents'][0]}")
        print(f"doc1 元数据: {result['metadatas'][0]}")
    
    # 4. 根据元数据过滤查询
    print("\n【步骤4】根据元数据过滤查询")
    result = db.get(where={"color": "red"})
    print(f"红色水果数量: {len(result.get('ids', []))}")
    for id, doc in zip(result.get("ids", []), result.get("documents", [])):
        print(f"  - {id}: {doc}")
    
    # 5. 相似度搜索（文本查询）
    print("\n【步骤5】相似度搜索 - 文本查询")
    print("搜索与'红色的水果'最相似的：")
    results = db.search(query_text="红色的水果", n_results=3)
    if results.get("documents"):
        for i, (doc, distance) in enumerate(zip(results["documents"][0], results["distances"][0])):
            print(f"  {i+1}. {doc} (距离: {distance:.4f})")
    
    # 6. 相似度搜索（带过滤条件）
    print("\n【步骤6】相似度搜索 - 只搜索水果")
    results = db.search(
        query_text="水果",
        n_results=2,
        where={"category": "fruit"}
    )
    if results.get("documents"):
        for doc in results["documents"][0]:
            print(f"  - {doc}")
    
    # 7. 更新数据
    print("\n【步骤7】更新数据")
    db.update(
        id="doc1",
        document="苹果是一种红色的水果，很甜",
        metadata={"category": "fruit", "color": "red", "taste": "sweet"}
    )
    
    # 验证更新
    result = db.get(ids=["doc1"])
    print(f"更新后: {result['documents'][0]}")
    print(f"新元数据: {result['metadatas'][0]}")
    
    # 8. 删除数据
    print("\n【步骤8】删除数据")
    db.delete(ids=["doc4"])
    print(f"删除后还有 {db.count()} 条数据")
    
    # 9. 查看剩余数据
    print("\n【步骤9】查看剩余数据")
    remaining = db.get()
    for id, doc in zip(remaining.get("ids", []), remaining.get("documents", [])):
        print(f"  - {id}: {doc}")
    
    # 10. 数据已自动持久化
    print("\n【步骤10】数据已自动持久化")
    print("数据保存在 ./data/chroma_data 目录中")
    
    print("\n" + "=" * 60)
    print("示例结束！")
    print("=" * 60)
