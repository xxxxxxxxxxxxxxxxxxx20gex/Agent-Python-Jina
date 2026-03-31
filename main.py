import os
import signal
import sys
import shutil
from pathlib import Path
from urllib.parse import urlparse
from agno.agent import Agent 
from agno.models.openai.like import OpenAILike 
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
from agno.skills import Skills, LocalSkills
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

SKILLS_DIR = Path(__file__).parent / "workspace" / "skills"

def _normalize_openai_base_url(raw: str | None) -> str | None:
    """Normalize base_url for OpenAI-compatible clients.

    Gateways sometimes provide a full endpoint URL (e.g. .../v1/chat/completions).
    OpenAI-compatible clients will append resource paths themselves, so we keep
    base_url at the API root (typically .../v1) to avoid duplicated paths.
    """
    if not raw:
        return raw

    base = raw.strip().rstrip("/")
    lowered = base.lower()
    for suffix in ("/chat/completions", "/completions", "/models"):
        if lowered.endswith(suffix):
            base = base[: -len(suffix)].rstrip("/")
            lowered = base.lower()

    # Best-effort validation; if it's not a URL, still return trimmed string.
    try:
        parsed = urlparse(base)
        if parsed.scheme and parsed.netloc:
            return base
    except Exception:
        pass
    return base


def _build_mcp_tools() -> list:
    """Create MCP tool list, skipping tools with missing executables."""
    tools = []

    # Prefer the current interpreter to avoid stale hardcoded paths.
    python_exe = sys.executable
    work_dir = r"C:\\Users\\WUJIEAI\\Desktop\\me_workplace\\Agent-Python-Jina\\workspace"
    mcp_project = r"C:\\Users\\WUJIEAI\\Desktop\\me_workplace\\Agent-Python-Jina\\mcp\\mcp-python-interpreter"

    tools.append(
        MCPTools(
            transport="stdio",
            command=(
                f"\"{python_exe}\" -m mcp_python_interpreter.main "
                f"--dir \"{work_dir}\" --python-path \"{python_exe}\""
            ),
            env={
                "MCP_ALLOW_SYSTEM_ACCESS": "0",
                "PYTHONPATH": mcp_project,
            },
        )
    )

    # Puppeteer requires Node.js (npx). Skip if missing.
    if shutil.which("npx"):
        tools.append(
            MCPTools(
                transport="stdio",
                command="npx -y @modelcontextprotocol/server-puppeteer",
                env={
                    "PUPPETEER_LAUNCH_OPTIONS": "{ \"headless\": true }",
                },
            )
        )

    return tools

db = SqliteDb(db_file="tmp/test_workflow.db")

deep_read_agent = Agent(
    name="智能助手",
    model=OpenAILike(
        id=CC,
        base_url=_normalize_openai_base_url(BASEURL),
        api_key=APIKEY,
        temperature=0.2,  # 略微提高温度以增加创造性
    ),
    skills=Skills(loaders=[LocalSkills(str(SKILLS_DIR))]),
    db = db,
    enable_user_memories=True,  # 启用用户记忆
    enable_agentic_memory=True,  # 启用智能记忆管理
    add_memories_to_context=True,  # 将记忆添加到上下文
    add_history_to_context=True,  
    num_history_runs=10,  # 增加历史记录数量
    cache_session=True,  # 启用会话缓存

    telemetry=False,
    
    # === 工具配置 ===
    tools=_build_mcp_tools(),

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