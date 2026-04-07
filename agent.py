import os
import logging
from datetime import datetime
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# ==================== LOGGING SETUP ====================
# Tạo thư mục logs nếu chưa có
os.makedirs("logs", exist_ok=True)

# File log theo ngày
log_filename = f"logs/chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Cấu hình logging: ghi cả ra console và file
logger = logging.getLogger("TravelBuddy")
logger.setLevel(logging.INFO)

# Handler ghi ra file
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(file_handler)

# Handler in ra console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(console_handler)

# ==================== 1. ĐỌC SYSTEM PROMPT ====================
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# ==================== 2. KHAI BÁO STATE ====================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# ==================== 3. KHỞI TẠO LLM VÀ TOOLS ====================
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# ==================== 4. AGENT NODE ====================
def agent_node(state: AgentState):
    messages = state["messages"]

    # Chèn System Prompt nếu chưa có
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            logger.info(f"🔧 Gọi tool: {tc['name']}({tc['args']})")
    else:
        # Log nội dung trả lời (cắt ngắn nếu quá dài)
        preview = response.content[:200] + "..." if len(response.content) > 200 else response.content
        logger.info(f"💬 LLM trả lời: {preview}")

    return {"messages": [response]}

# ==================== 5. XÂY DỰNG GRAPH ====================
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# ==================== 6. CHAT LOOP ====================
if __name__ == "__main__":
    print("=" * 60)
    print("  TravelBuddy – Trợ lý Du lịch Thông minh")
    print("  Gõ 'quit' để thoát")
    print("=" * 60)

    logger.info("=== Bắt đầu phiên chat mới ===")

    while True:
        user_input = input("\nBạn: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "q"]:
            logger.info("=== Kết thúc phiên chat ===")
            print("\nTạm biệt! Chúc bạn có chuyến đi vui vẻ! 🌴")
            break

        logger.info(f"👤 User: {user_input}")
        print("\nTravelBuddy đang suy nghĩ...")

        try:
            result = graph.invoke({"messages": [("human", user_input)]})
            final = result["messages"][-1]
            print(f"\nTravelBuddy: {final.content}")
        except Exception as e:
            logger.error(f"❌ Lỗi: {e}")
            print(f"\n⚠️ Có lỗi xảy ra: {e}")