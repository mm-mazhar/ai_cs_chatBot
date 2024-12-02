from typing import Any, Optional

from agent_controller import AgentController
from configs import cfg
from fastapi import APIRouter, status
from schemas import OrderTakingResponse

order_taking_router = APIRouter(tags=[cfg.ROUTES.ORDER_TAKING_TAG])

# print(f"cfg.ROUTES.ORDER_TAKING: {cfg.ROUTES.ORDER_TAKING}")


@order_taking_router.post(
    cfg.ROUTES.ORDER_TAKING,
    # response_model=OrderTakingResponse,
    status_code=status.HTTP_200_OK,
)
def order_taking(request: dict) -> dict[str, Any]:
    agent_controller = AgentController()
    response: dict[str, Any] = agent_controller.get_response(request)
    # print(f"response: {response}")
    return response
