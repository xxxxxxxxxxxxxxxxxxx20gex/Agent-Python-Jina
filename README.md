# AI Agent with MCP Integration

基于 Agno 框架的多工具 AI Agent，通过 Model Context Protocol (MCP) 集成 Python 代码执行和浏览器自动化能力

---

## Features
- **Python 代码执行**：集成 mcp-python-interpreter，支持在隔离环境中执行 Python 代码
- **浏览器自动化**：集成 Puppeteer MCP 服务器，支持网页导航、截图、交互等操作

---

## Quick Start

### 环境配置

```bash
# 创建 conda 虚拟环境
conda create -n myconda python=3.12
conda activate myconda
```

### 安装

```bash
pip install -r requirements.txt
```

### 配置
- 去jina官网申请一个个人api key，有免费额度
- 需要一个模型的key，可以是openai的，也可以是claude的

1. 复制环境变量模板：
```bash
cp .env_example .env
```

2. 编辑 `.env`，配置模型参数：
```env
CC=claude-4.5-sonnet                    # 模型 ID
BASEURL=https://api.example.com/v1      # API 基础 URL
APIKEY=sk-your-api-key                   # API 密钥
```

3. 配置 MCP 服务器路径（如使用本地 mcp-python-interpreter）：
   - 在 `main.py` 中修改 `PYTHONPATH` 环境变量指向本地项目路径
   - 修改 `--dir` 参数指向工作目录
   - 修改 `--python-path` 参数指向 Python 解释器路径

MCPTools(
    transport="stdio",
    command=r"python -m mcp_python_interpreter.main --dir C:\\Users\\【填写自己的目录】\\workspace --python-path 【填写自己的目录】\\python.exe",
    env={
        "MCP_ALLOW_SYSTEM_ACCESS": "0",
        "PYTHONPATH": r"C:\\Users\\【填写自己的mcp目录】\\mcp-python-interpreter"
    }
)

### 运行

```bash
python main.py
```

服务将在 `http://0.0.0.0:7777` 启动。

---

## MCP 配置说明

### 当前集成的 MCP 服务器

#### mcp-python-interpreter

**功能：** 在隔离环境中执行 Python 代码，支持文件操作、包管理等


## MCP 服务器配置方式
#### 1. 使用本地 MCP 服务器（推荐，启动更快）

```python
MCPTools(
    transport="stdio",
    command=r"python -m mcp_python_interpreter.main --dir <工作目录> --python-path <Python路径>",
    env={
        "MCP_ALLOW_SYSTEM_ACCESS": "0",  # 是否允许系统级文件访问
        "PYTHONPATH": r"<本地项目路径>"   # 指向本地 mcp-python-interpreter 项目
    }
)
```

**配置要点：**
- `transport="stdio"`：使用标准输入输出进行通信
- `command`：启动 MCP 服务器的命令，支持命令行参数
- `env`：传递给 MCP 服务器的环境变量
- `PYTHONPATH`：必须指向本地项目的根目录（包含 `mcp_python_interpreter` 模块的目录）

#### 2. 使用远程/在线 MCP 服务器

```python
MCPTools(
    transport="sse",
    url="https://api.example.com/mcp/server/sse?Authorization=token"
)
```

#### 3. 使用 npx 自动下载运行（Node.js 服务器）

```python
MCPTools(
    transport="stdio",
    command="npx -y @modelcontextprotocol/server-puppeteer",
    env={"PUPPETEER_LAUNCH_OPTIONS": "{ \"headless\": true }"}
)
```

---

## 项目结构

```
项目根目录/
├── main.py                    # 主程序入口，Agent 和 MCP 配置
├── requirements.txt           # Python 依赖
├── .env_example               # 环境变量配置模板
├── .env                       # 实际环境变量配置（需创建）
├── mcp/                       # 本地 MCP 服务器项目
│   └── mcp-python-interpreter/
│       ├── mcp_python_interpreter/
│       │   ├── main.py       # MCP 服务器入口
│       │   └── server.py     # MCP 服务器实现
│       └── pyproject.toml
├── workspace/                 # 代码执行工作目录
│   └── [用户代码文件]
└── tmp/                       # 临时文件
    └── test_workflow.db       # SQLite 数据库
```

---

## 使用说明

### 启动服务

运行 `python main.py` 后，Agent 将：
1. 加载环境变量配置
2. 初始化 MCP 服务器连接
3. 启动 FastAPI 服务在 7777 端口
