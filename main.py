import os
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
db_mem = SqliteDb(db_file="tmp/memory.db")

# 创建智能助手实例
deep_read_agent = Agent(
    name="智能助手",
    model=OpenAILike(
        id=CC,
        base_url=BASEURL,
        api_key=APIKEY,
        temperature=0.2,  # 略微提高温度以增加创造性
    ),
    db = db,
    # === 核心智能增强配置 ===
    
    # 1. 推理能力 - 启用逐步思考
    reasoning=True,
    reasoning_min_steps=2,
    reasoning_max_steps=15,
    
    # 2. 记忆管理 - 启用长期记忆
    memory_manager=MemoryManager(
                        model=OpenAILike(
                            id=CC, 
                            base_url=BASEURL, 
                            api_key=APIKEY
                        ),
                        db=db_mem,
                    ),
    enable_user_memories=True,  # 启用用户记忆
    enable_agentic_memory=True,  # 启用智能记忆管理
    add_memories_to_context=True,  # 将记忆添加到上下文
    
    # 3. 学习机制 - 启用持续学习
    # learning=True,  # 启用学习机器
    # add_learnings_to_context=True,  # 将学习结果添加到上下文
    
    # 4. 文化知识 - 启用共享知识
    # culture_manager=CultureManager(model=OpenAILike(id=CC, base_url=BASEURL, api_key=APIKEY)),
    # enable_agentic_culture=True,  # 启用智能文化管理
    # update_cultural_knowledge=True,  # 更新文化知识
    # add_culture_to_context=True,  # 将文化知识添加到上下文
    
    # 5. 会话管理 - 增强会话理解
    # enable_session_summaries=True,  # 启用会话摘要
    # add_session_summary_to_context=True,  # 将会话摘要添加到上下文
    add_history_to_context=True,  
    num_history_runs=5,  # 增加历史记录数量
    max_tool_calls_from_history=None,  # 限制历史中的工具调用
    
    # 6. 状态管理 - 启用智能状态
    add_session_state_to_context=True,  # 启用会话状态
    enable_agentic_state=True,  # 启用智能状态管理
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
            command=r"python -m mcp_python_interpreter.main --dir C:\\Users\\填写自己的目录\\Desktop\\test-kimi\\play\\workspace --python-path D:\\app\\anaconda\\envs\\myconda\\python.exe",
            env={
                "MCP_ALLOW_SYSTEM_ACCESS": "0",
                "PYTHONPATH": r"C:\\Users\\填写自己的目录\\Desktop\\test-kimi\\play\\mcp\\mcp-python-interpreter"
            }
        ),
        # Puppeteer 浏览器自动化
        # MCPTools(
        #     transport="stdio", 
        #     command="npx -y @modelcontextprotocol/server-puppeteer",
        #     env={"PUPPETEER_LAUNCH_OPTIONS": "{ \"headless\": true }"},
        #     # exclude_tools= ['puppeteer_screenshot'],
        # ),
    ],
    # tool_call_limit=15,  # 增加工具调用限制
    
    # === 上下文增强 ===
    markdown=True,
    add_datetime_to_context=True,
    add_location_to_context=True,
    add_name_to_context=True,  # 添加名称到上下文
    
    # === 输出配置 ===
    stream=True, 
    store_tool_messages=False,  # 存储工具消息以便学习
    store_history_messages=True,  
    store_media=True,
    
    # === 调试配置 ===
    debug_mode=False,  # 启用调试模式
    debug_level=1,  # 详细调试级别
    
    # === 系统描述 ===
    description="""你是一名高级AI助手，具备以下核心能力:
    
    1. **深度推理**：能够进行多步骤、结构化的思考过程
    2. **长期记忆**：记住用户偏好、历史交互和重要信息
    3. **持续学习**：从每次交互中学习并改进
    4. **文化知识**：维护共享的知识体系和最佳实践
    5. **工具使用**：熟练运用各种工具完成任务
    6. **上下文理解**：全面理解会话历史和当前状态
    
    你的目标是提供准确、深入、个性化的帮助。在回答前，请：
    - 进行充分的推理和思考
    - 查阅相关记忆和知识
    - 必要时使用工具验证信息
    - 提供结构化的、详细的回答
    """,
    
    # === 额外指令 ===
    instructions=[
        "在回答复杂问题前，总是进行多步骤推理",
        "主动使用记忆工具记录重要信息",
        "当发现新的模式或最佳实践时，更新文化知识",
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
    
    # === 重试机制 ===
    retries=1,  # 增加重试次数
    delay_between_retries=1,
    exponential_backoff=True,
    
    # === 结构化输出支持 ===
    structured_outputs=True,  # 启用结构化输出
    parse_response=True,
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