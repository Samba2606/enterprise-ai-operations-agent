from langchain_core.tools import tool

from src.retriever import search_policy
from src.services import (
    create_ticket,
    get_customer,
    get_order,
    get_support_history,
)

@tool
def customer_lookup(customer_id: str) -> dict:
    """Get a customer using a customer ID such as CUST-001."""
    return get_customer(customer_id)

@tool
def order_lookup(order_id: str) -> dict:
    """Get order details using an order ID such as ORD-1002."""
    return get_order(order_id)

@tool
def support_history(customer_id: str) -> list[dict]:
    """Get previous support tickets for a customer."""
    return get_support_history(customer_id)

@tool
def policy_search(question: str) -> list[dict]:
    """Search company policy for information relevant to a question."""
    return search_policy(question)

@tool
def open_support_ticket(
    customer_id: str,
    issue: str,
    approved: bool = False,
) -> dict:
    """Create a support ticket. Explicit user approval is required."""
    if not approved:
        return {
            "requires_approval": True,
            "message": (
                "Ask the user to approve ticket creation before calling "
                "this tool again with approved=true."
            ),
        }

    return create_ticket(customer_id, issue)

TOOLS = [
    customer_lookup,
    order_lookup,
    support_history,
    policy_search,
    open_support_ticket,
]
