"""
向量数据库 Chroma 实现 - 教学版

本文件实现了一个简化版的向量数据库，包含基本的增删改查操作。
同时融入了多种软件设计模式和业务设计思想，作为学习资料。

设计理念：
1. 单一职责原则：每个类和方法只负责一项功能
2. 开闭原则：对扩展开放，对修改关闭
3. 依赖倒置原则：依赖抽象而非具体实现

使用的设计模式：
1. 工厂模式：创建向量数据库实例
2. 策略模式：向量相似度计算策略
3. 观察者模式：数据变更通知
4. 单例模式：全局配置管理
5. 装饰器模式：功能增强

业务设计思路：
- 分层架构：存储层、服务层、API层
- 数据模型：向量、元数据、索引
- 性能优化：内存索引、批量操作
- 可扩展性：插件系统、自定义策略
"""

import numpy as np
from typing import List, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod

class ConfigSingleton:
    """
    全局配置管理类，使用单例模式确保配置的一致性
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """初始化默认配置"""
        self.default_embedding_dim = 128
        self.similarity_threshold = 0.8
        self.max_items = 10000


# 策略模式：向量相似度计算策略
class SimilarityStrategy(ABC):
    """
    相似度计算策略抽象基类
    策略模式允许运行时切换不同的相似度计算方法
    """
    
    @abstractmethod
    def calculate(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """计算两个向量的相似度"""
        pass


class CosineSimilarity(SimilarityStrategy):
    """余弦相似度计算策略"""
    
    def calculate(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        计算余弦相似度
        公式：cos(theta) = (A · B) / (||A|| * ||B||)
        """
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class EuclideanSimilarity(SimilarityStrategy):
    """欧几里得距离相似度计算策略"""
    
    def calculate(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """
        计算欧几里得距离并转换为相似度
        公式：similarity = 1 / (1 + distance)
        """
        distance = np.linalg.norm(vector1 - vector2)
        return 1.0 / (1.0 + distance)


# 观察者模式：数据变更观察者
class VectorDBObserver(ABC):
    """
    向量数据库观察者抽象基类
    观察者模式用于数据变更时的通知机制
    """
    
    @abstractmethod
    def on_data_change(self, event_type: str, data: Dict[str, Any]):
        """数据变更回调方法"""
        pass


class LoggingObserver(VectorDBObserver):
    """日志记录观察者"""
    
    def on_data_change(self, event_type: str, data: Dict[str, Any]):
        """记录数据变更事件"""
        print(f"[LOG] {event_type}: {data}")


# 向量数据模型
class VectorItem:
    """
    向量数据项模型
    包含向量、ID、元数据等信息
    """
    
    def __init__(self, id: str, vector: np.ndarray, metadata: Optional[Dict[str, Any]] = None):
        """
        初始化向量数据项
        
        Args:
            id: 唯一标识符
            vector: 向量数据
            metadata: 元数据（可选）
        """
        self.id = id
        self.vector = vector
        self.metadata = metadata or {}
        self.created_at = "2026-02-09"  # 简化处理，实际应使用时间戳


# 核心向量数据库类
class ChromaVectorDB:
    """
    向量数据库核心类
    实现了基本的增删改查操作
    """
    
    def __init__(self, embedding_dim: int = 128, similarity_strategy: SimilarityStrategy = None):
        """
        初始化向量数据库
        
        Args:
            embedding_dim: 向量维度
            similarity_strategy: 相似度计算策略
        """
        self.embedding_dim = embedding_dim
        self.similarity_strategy = similarity_strategy or CosineSimilarity()
        self._items = {}  # 存储向量项，key为id
        self._observers = []  # 观察者列表
        self._config = ConfigSingleton()
    
    def add_observer(self, observer: VectorDBObserver):
        """
        添加观察者
        
        Args:
            observer: 观察者实例
        """
        self._observers.append(observer)
    
    def _notify_observers(self, event_type: str, data: Dict[str, Any]):
        """
        通知所有观察者
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        for observer in self._observers:
            observer.on_data_change(event_type, data)
    
    def add(self, id: str, vector: np.ndarray, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加向量数据
        
        Args:
            id: 唯一标识符
            vector: 向量数据
            metadata: 元数据（可选）
            
        Returns:
            bool: 添加是否成功
        """
        # 验证向量维度
        if len(vector) != self.embedding_dim:
            raise ValueError(f"Vector dimension must be {self.embedding_dim}")
        
        # 检查是否达到最大容量
        if len(self._items) >= self._config.max_items:
            raise RuntimeError("Database capacity reached")
        
        # 创建向量项
        item = VectorItem(id, vector, metadata)
        self._items[id] = item

        self._notify_observers("add", {"id": id, "metadata": metadata})
        
        return True
    
    def batch_add(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量添加向量数据
        
        Args:
            items: 向量数据列表，每个元素包含id、vector和可选的metadata
            
        Returns:
            Dict[str, Any]: 批量操作结果
        """
        success_count = 0
        failed_items = []
        
        for item in items:
            try:
                self.add(item["id"], item["vector"], item.get("metadata"))
                success_count += 1
            except Exception as e:
                failed_items.append({"id": item.get("id"), "error": str(e)})
        
        return {
            "success_count": success_count,
            "failed_count": len(failed_items),
            "failed_items": failed_items
        }
    
    def get(self, id: str) -> Optional[VectorItem]:
        """
        获取向量数据
        
        Args:
            id: 唯一标识符
            
        Returns:
            Optional[VectorItem]: 向量数据项，如果不存在则返回None
        """
        return self._items.get(id)
    
    def update(self, id: str, vector: Optional[np.ndarray] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        更新向量数据
        
        Args:
            id: 唯一标识符
            vector: 新的向量数据（可选）
            metadata: 新的元数据（可选）
            
        Returns:
            bool: 更新是否成功
        """
        if id not in self._items:
            return False
        
        item = self._items[id]
        
        # 更新向量
        if vector is not None:
            if len(vector) != self.embedding_dim:
                raise ValueError(f"Vector dimension must be {self.embedding_dim}")
            item.vector = vector
        
        # 更新元数据
        if metadata is not None:
            item.metadata = metadata
        
        # 通知观察者
        self._notify_observers("update", {"id": id})
        
        return True
    
    def delete(self, id: str) -> bool:
        """
        删除向量数据
        
        Args:
            id: 唯一标识符
            
        Returns:
            bool: 删除是否成功
        """
        if id not in self._items:
            return False
        
        del self._items[id]
        
        # 通知观察者
        self._notify_observers("delete", {"id": id})
        
        return True
    
    def query(self, query_vector: np.ndarray, top_k: int = 5, filter: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        查询相似向量
        
        Args:
            query_vector: 查询向量
            top_k: 返回前k个最相似的结果
            filter: 过滤函数（可选）
            
        Returns:
            List[Dict[str, Any]]: 相似向量列表，每个元素包含id、similarity和metadata
        """
        # 验证向量维度
        if len(query_vector) != self.embedding_dim:
            raise ValueError(f"Query vector dimension must be {self.embedding_dim}")
        
        # 计算相似度
        results = []
        for id, item in self._items.items():
            # 应用过滤
            if filter and not filter(item.metadata):
                continue
            
            similarity = self.similarity_strategy.calculate(query_vector, item.vector)
            
            # 只添加相似度大于阈值的结果
            if similarity >= self._config.similarity_threshold:
                results.append({
                    "id": id,
                    "similarity": similarity,
                    "metadata": item.metadata
                })
        
        # 按相似度排序并返回前k个
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def count(self) -> int:
        """
        获取数据库中的向量数量
        
        Returns:
            int: 向量数量
        """
        return len(self._items)
    
    def clear(self) -> None:
        """
        清空数据库
        """
        self._items.clear()
        self._notify_observers("clear", {"message": "Database cleared"})


# 工厂模式：向量数据库工厂
class ChromaFactory:
    """
    向量数据库工厂类
    工厂模式用于创建不同配置的向量数据库实例
    """
    
    @staticmethod
    def create_default_db() -> ChromaVectorDB:
        """
        创建默认配置的向量数据库
        
        Returns:
            ChromaVectorDB: 默认配置的向量数据库实例
        """
        return ChromaVectorDB()
    
    @staticmethod
    def create_db_with_dimension(embedding_dim: int) -> ChromaVectorDB:
        """
        创建指定向量维度的向量数据库
        
        Args:
            embedding_dim: 向量维度
            
        Returns:
            ChromaVectorDB: 指定向量维度的向量数据库实例
        """
        return ChromaVectorDB(embedding_dim=embedding_dim)
    
    @staticmethod
    def create_db_with_strategy(strategy: SimilarityStrategy) -> ChromaVectorDB:
        """
        创建指定相似度计算策略的向量数据库
        
        Args:
            strategy: 相似度计算策略
            
        Returns:
            ChromaVectorDB: 指定相似度计算策略的向量数据库实例
        """
        return ChromaVectorDB(similarity_strategy=strategy)


# 装饰器模式：功能增强装饰器
def timing_decorator(func):
    """
    计时装饰器
    装饰器模式用于增强函数功能
    """
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] Time taken: {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper


def validate_input_decorator(func):
    """
    输入验证装饰器
    """
    def wrapper(self, *args, **kwargs):
        # 这里可以添加输入验证逻辑
        print(f"[{func.__name__}] Input validated")
        return func(self, *args, **kwargs)
    
    return wrapper


# 应用装饰器增强 ChromaVectorDB 类
class EnhancedChromaVectorDB(ChromaVectorDB):
    """
    增强版向量数据库
    使用装饰器模式增强功能
    """
    
    @timing_decorator
    def query(self, query_vector: np.ndarray, top_k: int = 5, filter: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        增强版查询方法，添加了计时功能
        """
        return super().query(query_vector, top_k, filter)
    
    @validate_input_decorator
    @timing_decorator
    def add(self, id: str, vector: np.ndarray, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        增强版添加方法，添加了输入验证和计时功能
        """
        return super().add(id, vector, metadata)


# 示例用法
if __name__ == "__main__":
    """
    示例代码，展示向量数据库的基本使用
    """
    # 创建向量数据库实例
    db = ChromaFactory.create_default_db()
    
    # 添加日志观察者
    db.add_observer(LoggingObserver())
    
    # 生成示例向量
    def generate_vector(dim: int) -> np.ndarray:
        return np.random.rand(dim)
    
    # 添加向量数据
    print("=== 添加向量数据 ===")
    db.add("id1", generate_vector(128), {"category": "document", "author": "Alice"})
    db.add("id2", generate_vector(128), {"category": "image", "author": "Bob"})
    db.add("id3", generate_vector(128), {"category": "document", "author": "Charlie"})
    
    # 批量添加向量数据
    print("\n=== 批量添加向量数据 ===")
    batch_items = [
        {"id": "id4", "vector": generate_vector(128), "metadata": {"category": "document", "author": "David"}},
        {"id": "id5", "vector": generate_vector(128), "metadata": {"category": "image", "author": "Eve"}}
    ]
    batch_result = db.batch_add(batch_items)
    print(f"批量添加结果: {batch_result}")
    
    # 查询向量数据
    print("\n=== 查询向量数据 ===")
    query_vector = generate_vector(128)
    results = db.query(query_vector, top_k=3)
    print(f"查询结果: {results}")
    
    # 按元数据过滤查询
    print("\n=== 按元数据过滤查询 ===")
    def document_filter(metadata):
        return metadata.get("category") == "document"
    
    filtered_results = db.query(query_vector, top_k=3, filter=document_filter)
    print(f"过滤查询结果: {filtered_results}")
    
    # 更新向量数据
    print("\n=== 更新向量数据 ===")
    db.update("id1", generate_vector(128), {"category": "document", "author": "Alice", "updated": True})
    
    # 删除向量数据
    print("\n=== 删除向量数据 ===")
    db.delete("id2")
    
    # 获取数据库统计信息
    print("\n=== 数据库统计信息 ===")
    print(f"向量数量: {db.count()}")
    
    # 清空数据库
    print("\n=== 清空数据库 ===")
    db.clear()
    print(f"清空后向量数量: {db.count()}")
    
    # 示例：使用不同的相似度计算策略
    print("\n=== 使用不同的相似度计算策略 ===")
    euclidean_db = ChromaFactory.create_db_with_strategy(EuclideanSimilarity())
    euclidean_db.add("id1", generate_vector(128))
    euclidean_results = euclidean_db.query(query_vector, top_k=1)
    print(f"欧几里得相似度查询结果: {euclidean_results}")
