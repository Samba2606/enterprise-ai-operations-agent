from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.config import MODEL_NAME
from src.tools import TOOLS

SYSTEM_PROMPT = """
You are an enterprise operations assistant for a demo ecommerce company.

Rules:
1. Use tools instead of inventing customer, order, ticket, or policy facts.
2. Use policy search for company policy questions.
3. Do not reveal unnecessary customer data.
4. Creating a support ticket requires explicit user approval.
5. If a tool returns an error, explain what is missing.
6. Keep answers concise and mention which records or policy were checked.
"""

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def build_graph():
    model = ChatGroq(
        model=MODEL_NAME,
        temperature=0,
    )
    model_with_tools = model.bind_tools(TOOLS)

    def call_model(state: AgentState):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )
    builder.add_edge("tools", "agent")

    return builder.compile()

def ask_agent(question: str) -> str:
    graph = build_graph()
    result = graph.invoke({
        "messages": [HumanMessage(content=question)]
    })
    return result["messages"][-1].content
