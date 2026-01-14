from os import getenv
from typing import Any, Dict, List, Optional

import httpx # pyright: ignore
from pydantic import BaseModel, Field, HttpUrl # pyright: ignore

from agno.tools import Toolkit # pyright: ignore
from agno.tools.function import ToolResult # pyright: ignore
from agno.utils.log import logger # pyright: ignore


class JinaReaderToolsConfig(BaseModel):
    """Jina Reader 工具配置类"""
    api_key: Optional[str] = Field(None, description="API key for Jina Reader")
    base_url: HttpUrl = Field("https://r.jina.ai/", description="Base URL for Jina Reader API")  # type: ignore
    search_url: HttpUrl = Field("https://s.jina.ai/", description="Search URL for Jina Reader API")  # type: ignore
    deepsearch_url: HttpUrl = Field("https://deepsearch.jina.ai/v1/chat/completions", description="DeepSearch API URL")  # type: ignore
    max_content_length: int = Field(10000, description="Maximum content length in characters")
    read_timeout: int = Field(60, description="Timeout for read_url requests (seconds)")  # URL 读取超时
    search_timeout: int = Field(30, description="Timeout for search_query requests (seconds)")  # 搜索超时
    deepsearch_timeout: int = Field(120, description="Timeout for DeepSearch API (seconds)")  # 深度搜索超时
    search_query_content: Optional[bool] = Field(False, description="Toggle full URL content in query search result")
    max_retries: int = Field(1, description="Max retries on failure")  # 失败重试次数


class JinaReaderTools(Toolkit):
    """
    Jina Reader 工具集，专注于网页内容读取和解析。
    
    默认启用功能：
    - read_url: 读取任意 URL 内容，转换为 LLM 友好的 Markdown 格式
    
    可选功能（默认关闭）：
    - search_query: 快速网页搜索（需设置 enable_search_query=True）
    - deep_search: 深度搜索（需设置 enable_deep_search=True）
    """
    
    def __init__(
        self,
        api_key: None,
        base_url: str = "https://r.jina.ai/",
        search_url: str = "https://s.jina.ai/",
        deepsearch_url: str = "https://deepsearch.jina.ai/v1/chat/completions",
        max_content_length: int = 10000,
        read_timeout: int = 15,           # URL 读取超时（秒）
        search_timeout: int = 10,         # 搜索超时（秒）
        deepsearch_timeout: int = 120,    # 深度搜索超时（秒）
        search_query_content: bool = True,
        max_retries: int = 1,             # 失败重试次数
        enable_read_url: bool = True,
        enable_search_query: bool = False,
        enable_deep_search: bool = False,
        all: bool = False,
        **kwargs,
    ):
        self.api_key = api_key or getenv("JINA_API_KEY")
        self.config: JinaReaderToolsConfig = JinaReaderToolsConfig(
            api_key=self.api_key,
            base_url=base_url,
            search_url=search_url,
            deepsearch_url=deepsearch_url,
            max_content_length=max_content_length,
            read_timeout=read_timeout,
            search_timeout=search_timeout,
            deepsearch_timeout=deepsearch_timeout,
            search_query_content=search_query_content,
            max_retries=max_retries,
        )

        # 根据配置启用对应工具
        tools: List[Any] = []
        if all or enable_read_url:
            tools.append(self.read_url)
        if all or enable_search_query:
            tools.append(self.search_query)
        if all or enable_deep_search:
            tools.append(self.deep_search)

        super().__init__(name="jina_reader_tools", tools=tools, **kwargs)

    def read_url(self, url: str) -> ToolResult:
        """
        读取 URL 内容并转换为 LLM 友好的 Markdown 格式。
        
        Args:
            url: 要读取的网页 URL
            
        Returns:
            ToolResult: 包含网页内容的工具返回对象
        """
        api_url = str(self.config.base_url)
        
        # 构建请求头（免费版配置，移除付费功能）
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Timeout": str(self.config.read_timeout),  # 服务端超时
            "X-Retain-Images": "none",         # 移除所有图片
            "X-Return-Format": "markdown",     # 返回 Markdown 格式
            # 移除网页噪音元素（导航、页眉页脚、侧边栏、广告等）
            "X-Remove-Selector": "header,footer,nav,aside,.sidebar,.menu,.navigation,.nav,.ads,.advertisement,.social-share,.share-buttons,.related-posts,.comments,.cookie-banner",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        # 使用 POST 方法（官方推荐）
        body = {"url": url}
        last_error = None
        
        # 简单重试机制
        for attempt in range(self.config.max_retries + 1):
            try:
                response = httpx.post(
                    api_url, 
                    headers=headers,
                    json=body,
                    timeout=self.config.read_timeout
                )
                response.raise_for_status()
                result = response.json()
                
                # 解析响应：提取 data.content 字段
                if "data" in result and "content" in result["data"]:
                    content = result["data"]["content"]
                    title = result["data"].get("title", "")
                    # 添加标题前缀
                    if title:
                        content = f"# {title}\n\n{content}"
                    return ToolResult(content=self._truncate_content(content))
                else:
                    # 兼容旧格式
                    return ToolResult(content=self._truncate_content(str(result)))
                    
            except httpx.TimeoutException:
                last_error = f"请求超时（{self.config.read_timeout}秒）"
                logger.warning(f"read_url 超时，尝试 {attempt + 1}/{self.config.max_retries + 1}")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"read_url 错误: {e}，尝试 {attempt + 1}/{self.config.max_retries + 1}")
        
        error_msg = f"读取 URL 失败: {last_error}"
        logger.error(error_msg)
        return ToolResult(content=error_msg)

    def search_query(self, query: str) -> ToolResult:
        """
        使用 Jina Search API 进行网页搜索。
        
        Args:
            query: 搜索关键词
            
        Returns:
            ToolResult: 包含搜索结果的工具返回对象
        """
        full_url = f"{self.config.search_url}"
        
        # 构建搜索专用 headers（免费版配置）
        headers = {
            "Accept": "application/json",
            "X-No-Images": "true",              # 移除所有图片
            "X-With-Images-Summary": "false",   # 取消图片汇总
            "X-With-Links-Summary": "false",    # 取消结尾链接汇总
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        if not self.config.search_query_content:
            headers["X-Respond-With"] = "no-content"  # 不返回完整内容，加快响应

        body = {"q": query}
        last_error = None
        
        # 简单重试机制
        for attempt in range(self.config.max_retries + 1):
            try:
                response = httpx.post(
                    full_url, 
                    headers=headers, 
                    json=body,
                    timeout=self.config.search_timeout
                )
                response.raise_for_status()
                content = response.json()
                return ToolResult(content=self._truncate_content(str(content)))
                
            except httpx.TimeoutException as e:
                last_error = f"请求超时（{self.config.search_timeout}秒）"
                logger.warning(f"search_query 超时，尝试 {attempt + 1}/{self.config.max_retries + 1}")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"search_query 错误: {e}，尝试 {attempt + 1}/{self.config.max_retries + 1}")
        
        error_msg = f"搜索失败: {last_error}"
        logger.error(error_msg)
        return ToolResult(content=error_msg)

    def deep_search(self, query: str) -> ToolResult:
        """
        使用 Jina DeepSearch API 进行深度搜索。
        
        DeepSearch 会自动执行多轮搜索、阅读网页内容、推理分析，
        直到找到最佳答案。适合复杂研究问题。
        
        注意：响应时间较长（约 30-60 秒），Token 消耗较高。
        
        Args:
            query: 搜索问题，可以是复杂的研究问题
            
        Returns:
            ToolResult: 包含深度搜索结果的工具返回对象
        """
        url = str(self.config.deepsearch_url)
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        # 构建请求体（OpenAI Chat Completions 兼容格式）
        body = {
            "model": "deepsearch",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False  # 简单实现，不使用流式响应
        }
        
        try:
            logger.info(f"DeepSearch 开始搜索: {query}")
            
            # 发送请求，使用较长超时时间
            response = httpx.post(
                url, 
                headers=headers, 
                json=body, 
                timeout=self.config.deepsearch_timeout
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 提取回答内容
            if "choices" in result and len(result["choices"]) > 0:
                answer = result["choices"][0].get("message", {}).get("content", "")
                logger.info(f"DeepSearch 完成，返回 {len(answer)} 字符")
                return ToolResult(content=self._truncate_content(answer))
            else:
                # 响应格式异常，返回原始内容
                return ToolResult(content=f"DeepSearch 响应格式异常: {str(result)[:500]}")
                
        except httpx.TimeoutException:
            error_msg = f"DeepSearch 请求超时（超过 {self.config.deepsearch_timeout} 秒）"
            logger.error(error_msg)
            return ToolResult(content=error_msg)
            
        except Exception as e:
            error_msg = f"DeepSearch 错误: {str(e)}"
            logger.error(error_msg)
            return ToolResult(content=error_msg)

    def _truncate_content(self, content: str) -> str:
        """Truncate content to the maximum allowed length."""
        if len(content) > self.config.max_content_length:
            truncated = content[: self.config.max_content_length]
            return truncated + "... (content truncated)"
        return content


if __name__ == "__main__":
    import time
    import random
    import concurrent.futures
    from datetime import datetime
    
    # ==================== 测试配置 ====================
    # 无 API Key 模式测试
    tools = JinaReaderTools(
        api_key=None,           # 不使用 API Key
        max_content_length=8000,  # 稍大的内容长度，查看更多内容
        read_timeout=15,        # 正常网页需要更长超时
        max_retries=1           # 允许1次重试
    )
    
    print("=" * 70)
    print("Jina URL 爬取测试 - 正常网页测试 (无 API Key 模式)")
    print("=" * 70)
    
    # ==================== 正常网页测试用例 ====================
    # 覆盖各类真实网站场景
    normal_webpage_cases = [
        # ===== 1. 新闻媒体网站 =====
        # ("csdn", "https://blog.csdn.net/xinjichenlibing/article/details/146869538"),
        ("zhihu", "https://www.zhihu.com/column/c_1085975047386050560 ")
    ]
    
    print(f"\n共 {len(normal_webpage_cases)} 个测试用例")
    print("=" * 70)
    
    # ==================== 逐个测试 ====================
    test_results = []
    
    for idx, (case_name, url) in enumerate(normal_webpage_cases, 1):
        print(f"\n[{idx}/{len(normal_webpage_cases)}] 测试: {case_name}")
        print(f"  URL: {url}")
        
        start_time = time.time()
        try:
            result = tools.read_url(url)
            elapsed = time.time() - start_time
            content = str(result.content)
            
            # 判断是否成功
            is_error = "失败" in content or "错误" in content or "Error" in content[:100]
            status = "❌ 失败" if is_error else "✅ 成功"
            
            # 提取内容摘要
            content_clean = content.replace('\n', ' ').replace('\r', '')
            content_preview = content_clean[:]
            
            # 统计内容信息
            content_len = len(content)
            word_count = len(content.split())
            
            print(f"  状态: {status} | 耗时: {elapsed:.2f}s | 字符数: {content_len} | 词数: {word_count}")
            print(f"  预览: {content_preview}...")
            
            test_results.append({
                "name": case_name,
                "url": url,
                "success": not is_error,
                "elapsed": elapsed,
                "content_len": content_len,
                "word_count": word_count
            })
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"  状态: ⚠️ 异常 | 耗时: {elapsed:.2f}s")
            print(f"  错误: {type(e).__name__}: {str(e)[:100]}")
            test_results.append({
                "name": case_name,
                "url": url,
                "success": False,
                "elapsed": elapsed,
                "error": str(e)
            })
        
        # 添加小延迟，避免频率限制
        time.sleep(0.5)
    
    # ==================== 测试统计 ====================
    print("\n" + "=" * 70)
    print("【测试统计报告】")
    print("=" * 70)
    
    # 成功率统计
    success_count = sum(1 for r in test_results if r["success"])
    fail_count = len(test_results) - success_count
    success_rate = success_count / len(test_results) * 100
    
    print(f"\n📊 总体统计:")
    print(f"  - 总测试数: {len(test_results)}")
    print(f"  - 成功: {success_count} ({success_rate:.1f}%)")
    print(f"  - 失败: {fail_count} ({100-success_rate:.1f}%)")
    
    # 响应时间统计
    elapsed_times = [r["elapsed"] for r in test_results]
    avg_time = sum(elapsed_times) / len(elapsed_times)
    max_time = max(elapsed_times)
    min_time = min(elapsed_times)
    
    print(f"\n⏱️ 响应时间:")
    print(f"  - 平均: {avg_time:.2f}s")
    print(f"  - 最快: {min_time:.2f}s")
    print(f"  - 最慢: {max_time:.2f}s")
    
    # 内容统计（仅成功的）
    success_results = [r for r in test_results if r["success"]]
    if success_results:
        avg_content = sum(r["content_len"] for r in success_results) / len(success_results)
        avg_words = sum(r["word_count"] for r in success_results) / len(success_results)
        print(f"\n📝 内容统计 (仅成功):")
        print(f"  - 平均字符数: {avg_content:.0f}")
        print(f"  - 平均词数: {avg_words:.0f}")
    
    # 失败列表
    failed_results = [r for r in test_results if not r["success"]]
    if failed_results:
        print(f"\n❌ 失败列表:")
        for r in failed_results:
            error_info = r.get("error", "返回错误内容")
            print(f"  - {r['name']}: {error_info[:50]}")
    
    # 按类别统计
    print(f"\n📁 按类别统计:")
    categories = {}
    for r in test_results:
        # 从名称提取类别
        cat = r["name"].split("-")[0]
        if cat not in categories:
            categories[cat] = {"total": 0, "success": 0}
        categories[cat]["total"] += 1
        if r["success"]:
            categories[cat]["success"] += 1
    
    for cat, stats in sorted(categories.items()):
        rate = stats["success"] / stats["total"] * 100
        print(f"  - {cat}: {stats['success']}/{stats['total']} ({rate:.0f}%)")
    
    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)