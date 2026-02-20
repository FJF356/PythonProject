可以从 OPENAI_API_KEY 环境变量推断，或者指定为字符串、或返回字符串的同步或异步函数。
    1. example "使用环境变量指定"
        `ash
        export OPENAI_API_KEY=...
        在项目目录下创建.env文件和.gitignore文件`
        `python
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-5-nano")
        `
    2. example "使用字符串指定"
        `python
        from langchain_openai import ChatOpenAI
        model = ChatOpenAI(model="gpt-5-nano", api_key="...")
        `
    3. example "使用同步函数指定"
        `python
        from langchain_openai import ChatOpenAI
        def get_api_key() -> str:
            # 自定义逻辑来获取 API key
            return "..."
        model = ChatOpenAI(model="gpt-5-nano", api_key=get_api_key)
        `
    4. example "使用异步函数指定"
        `python
        from langchain_openai import ChatOpenAI
        async def get_api_key() -> str:
            # 自定义异步逻辑来获取 API key
            return "..."
        model = ChatOpenAI(model="gpt-5-nano", api_key=get_api_key)
        `
## 四种方式的适用场景
    环境变量：
         生产环境部署
         开发环境配置
         CI/CD流水线
         多环境切换
    直接字符串：
        快速原型开发
        本地测试
        临时脚本
        演示代码
    同步函数：
        从密钥管理服务获取
        需要动态轮换密钥
        多租户应用
        自定义密钥获取逻辑
    异步函数：
        异步Web应用
        FastAPI等异步框架
        高并发场景
        需要异步获取密钥