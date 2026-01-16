import os
import signal
import sys
from agno.agent import Agent 
from agno.models.openai.like import OpenAILike 
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from agno.memory import MemoryManager
from agno.learn.machine import LearningMachine
from agno.culture.manager import CultureManager
from agno.reasoning.step import ReasoningStep
from tools.jina_tool import JinaReaderTools
from dotenv import load_dotenv

load_dotenv()

CC = os.getenv("CC")
BASEURL = os.getenv("BASEURL")
APIKEY = os.getenv("APIKEY")
JINA = os.getenv("JINA")

db = SqliteDb(db_file="tmp/test_workflow.db")

deep_read_agent = Agent(
    name="智能助手",
    model=OpenAILike(
        id=CC,
        base_url=BASEURL,
        api_key=APIKEY,
        temperature=0.2,  # 略微提高温度以增加创造性
    ),
    db = db,
    enable_user_memories=True,  # 启用用户记忆
    enable_agentic_memory=True,  # 启用智能记忆管理
    add_memories_to_context=True,  # 将记忆添加到上下文
    add_history_to_context=True,  
    num_history_runs=10,  # 增加历史记录数量
    cache_session=True,  # 启用会话缓存

    telemetry=False,
    
    # === 工具配置 ===
    tools=[
        JinaReaderTools(
            enable_read_url=True,       # 启用 URL 读取
            enable_search_query=False,  # 关闭搜索功能
            enable_deep_search=False,   # 关闭深度搜索
            api_key=JINA,
            instructions="read_url(url) - 读取 URL 完整正文",
        ),
        # Python 解释器
        MCPTools(
            transport="stdio",
            command=r"python -m mcp_python_interpreter.main --dir C:\\Users\\WUJIEAI\\Desktop\\test-kimi\\play\\workspace --python-path D:\\app\\anaconda\\envs\\lyq\\python.exe",
            env={
                "MCP_ALLOW_SYSTEM_ACCESS": "0",
                "PYTHONPATH": r"C:\\Users\\WUJIEAI\\Desktop\\test-kimi\\play\\mcp\\mcp-python-interpreter",  # 就是当前项目的mcp文件下的mcp-python-interpreter的绝对路径
            },
        ),
        # Puppeteer 浏览器自动化
        # MCPTools(
        #     transport="stdio", 
        #     command="npx -y @modelcontextprotocol/server-puppeteer",
        #     env={
        #         "PUPPETEER_LAUNCH_OPTIONS": "{ \"headless\": true }",
        #     },
        #     # exclude_tools= ['puppeteer_screenshot'],
        # ),
    ],

    # === 上下文增强 ===
    markdown=True,
    add_datetime_to_context=True,
    add_location_to_context=True,
    add_name_to_context=True,  # 添加名称到上下文
    
    # === 输出配置 ===
    stream=True, 
    store_tool_messages=True,  # 存储工具消息以便学习
    store_history_messages=True,  
    store_media=True,
    
    # === 调试配置 ===
    debug_mode=True,  # 启用调试模式
    debug_level=1,  # 详细调试级别
    
    # === 系统描述 ===
    description="""你是一名高级AI助手，具备以下核心能力:
    
    1. **深度推理**：能够进行多步骤、结构化的思考过程
    5. **工具使用**：熟练运用各种工具完成任务
    6. **上下文理解**：全面理解会话历史和当前状态
    
    你的目标是提供准确、深入、个性化的帮助。在回答前，请：
    - 进行充分的推理和思考
    - 必要时使用工具验证信息
    - 提供结构化的、详细的回答
    """,
    
    instructions=[
        "在回答复杂问题前，总是进行多步骤推理",
        "充分利用历史上下文提供个性化回答",
        "在不确定时，使用工具验证信息",
        "提供详细、结构化的回答，包含推理过程",
    ],
    
    # === 期望输出格式 ===
    expected_output="""提供详细、准确、结构化的回答，包含：
    1. 推理过程（如果复杂）
    2. 具体答案
    3. 相关背景信息
    4. 可操作的建议（如适用）
    """,
)

agent_os = AgentOS(
  name="My AgentOS",
  description="My Multi-Agent Runtime",
  agents=[deep_read_agent],
)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(
        app="__main__:app", 
        host="0.0.0.0",
        port=7777,
    )