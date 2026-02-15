# 向量数据库软件架构 - Mermaid图表

## 1. 时序图：向量查询流程

```mermaid
sequenceDiagram
    autonumber
    participant User as 用户
    participant API as API层
    participant Service as 服务层
    participant Storage as 存储层
    participant Strategy as 相似度策略

    User->>API: 发送查询请求<br/>(query_vector, top_k)
    API->>Service: 调用查询服务
    Service->>Storage: 获取所有向量数据
    Storage-->>Service: 返回向量列表
    
    loop 遍历每个向量
        Service->>Strategy: 计算相似度<br/>(query_vector, stored_vector)
        Strategy-->>Service: 返回相似度分数
    end
    
    Service->>Service: 排序并筛选top_k
    Service-->>API: 返回查询结果
    API-->>User: 返回相似向量列表
```

## 2. 流程图：向量数据库核心功能

```mermaid
flowchart TD
    Start([开始]) --> Init[初始化数据库]
    Init --> Menu{选择操作}
    
    Menu -->|添加| AddInput[输入ID和向量]
    AddInput --> ValidateDim{验证维度}
    ValidateDim -->|通过| Store[存储到字典]
    ValidateDim -->|失败| Error1[返回错误]
    Store --> Notify[通知观察者]
    Notify --> Menu
    
    Menu -->|查询| QueryInput[输入查询向量]
    QueryInput --> CalcSim[计算相似度]
    CalcSim --> Filter[应用过滤器]
    Filter --> Sort[排序结果]
    Sort --> ReturnTop[返回TopK]
    ReturnTop --> Menu
    
    Menu -->|更新| UpdateInput[输入ID和新向量]
    UpdateInput --> CheckExist{ID存在?}
    CheckExist -->|是| UpdateStore[更新数据]
    CheckExist -->|否| Error2[返回错误]
    UpdateStore --> Notify2[通知观察者]
    Notify2 --> Menu
    
    Menu -->|删除| DeleteInput[输入ID]
    DeleteInput --> CheckExist2{ID存在?}
    CheckExist2 -->|是| Remove[删除数据]
    CheckExist2 -->|否| Error3[返回错误]
    Remove --> Notify3[通知观察者]
    Notify3 --> Menu
    
    Menu -->|退出| End([结束])
    
    Error1 --> Menu
    Error2 --> Menu
    Error3 --> Menu
```

## 3. 甘特图：向量数据库开发计划

```mermaid
gantt
    title 向量数据库开发计划
    dateFormat  YYYY-MM-DD
    section 基础架构
    需求分析           :done, a1, 2026-02-01, 2d
    技术选型           :done, a2, after a1, 1d
    架构设计           :done, a3, after a2, 2d
    
    section 核心功能
    数据模型设计       :done, b1, after a3, 2d
    增删改查实现       :done, b2, after b1, 5d
    相似度计算         :done, b3, after b1, 3d
    批量操作           :active, b4, after b2, 2d
    
    section 设计模式
    单例模式实现       :done, c1, after a3, 1d
    工厂模式实现       :done, c2, after c1, 1d
    策略模式实现       :done, c3, after c1, 2d
    观察者模式实现     :done, c4, after c3, 1d
    
    section 优化扩展
    性能优化           :d1, after b4, 3d
    单元测试           :d2, after b4, 3d
    文档编写           :d3, after d2, 2d
    代码审查           :d4, after d3, 1d
```

## 图表说明

### 时序图说明
- 展示了用户查询向量的完整流程
- 包含4个参与者：用户、API层、服务层、存储层、相似度策略
- 展示了数据流向和交互顺序

### 流程图说明
- 展示了向量数据库的4个核心功能：增、删、改、查
- 包含验证、错误处理、观察者通知等流程
- 使用不同颜色区分不同操作路径

### 甘特图说明
- 展示了向量数据库的开发计划
- 分为4个阶段：基础架构、核心功能、设计模式、优化扩展
- 标注了已完成和进行中的任务
