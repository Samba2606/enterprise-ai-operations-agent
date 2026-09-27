from src.retriever import search_policy
from src.services import get_order, get_support_history

def check(name: str, condition: bool) -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"{status:4} | {name}")
    return condition

results = []

order = get_order("ORD-1002")
results.append(
    check(
        "order lookup returns delayed status",
        order.get("status") == "delayed",
    )
)

history = get_support_history("CUST-002")
results.append(
    check(
        "support history returns demo tickets",
        len(history) >= 2,
    )
)

refund_hits = search_policy(
    "When can a delayed order get a full refund?",
    top_k=2,
)
joined = " ".join(hit["text"].lower() for hit in refund_hits)

results.append(
    check(
        "policy retrieval finds refund section",
        "refund" in joined,
    )
)

results.append(
    check(
        "policy retrieval finds 10-day rule",
        "10 calendar days" in joined,
    )
)

score = sum(results) / len(results)
print(f"\nScore: {score:.0%}")
