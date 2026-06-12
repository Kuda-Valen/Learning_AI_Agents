from agents import Agent, Runner

technical_support_agent = Agent(
    name="Technical Support Agent",
    instructions=(
        "You provide expert assistance with resolving technical issues, "
        "system outages, or product troubleshooting."
    ),
    tools=[search_knowledge_base],
)

sales_assistant_agent = Agent(
    name="Sales Assistant Agent",
    instructions=(
        "You help enterprise clients browse the product catalog, "
        "recommend suitable solutions, and facilitate purchase transactions."
    ),
    tools=[initiate_purchase_order],
)

order_management_agent = Agent(
    name="Order Management Agent",
    instructions=(
        "You assist clients with inquiries regarding order tracking, "
        "delivery schedules, and processing returns or refunds."
    ),
    tools=[track_order_status, initiate_refund_process],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You act as the first point of contact, assessing customer queries "
        "and directing them promptly to the correct specialized agent."
    ),
    handoffs=[
        technical_support_agent,
        sales_assistant_agent,
        order_management_agent,
    ],
)

result = await Runner.run(
    triage_agent,
    input("Could you please provide an update on the delivery timeline for our recent purchase?")
)