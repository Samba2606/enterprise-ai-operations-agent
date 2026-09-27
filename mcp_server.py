from mcp.server import MCPServer

from src.retriever import search_policy
from src.services import (
    create_ticket,
    get_customer,
    get_order,
    get_support_history,
)

mcp = MCPServer(
    "enterprise-ops",
    instructions="Tools for demo ecommerce operations data.",
)

@mcp.tool()
def customer_lookup(customer_id: str) -> dict:
    return get_customer(customer_id)

@mcp.tool()
def order_lookup(order_id: str) -> dict:
    return get_order(order_id)

@mcp.tool()
def support_history(customer_id: str) -> list[dict]:
    return get_support_history(customer_id)

@mcp.tool()
def policy_search(question: str) -> list[dict]:
    return search_policy(question)

@mcp.tool()
def create_support_ticket(
    customer_id: str,
    issue: str,
    approved: bool = False,
) -> dict:
    if not approved:
        return {"requires_approval": True}

    return create_ticket(customer_id, issue)

if __name__ == "__main__":
    mcp.run()
