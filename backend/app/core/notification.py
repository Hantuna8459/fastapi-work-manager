from uuid import UUID

from backend.app.main import user_ws, ws_manager


async def notify(category_id: UUID, message: str) -> None:
    """
        Gửi notification đến các User join Category qua websocket
    """

    user_ids = ws_manager.ws_manager.get(category_id)

    for user_id in user_ids:
        if user_ws.__contains__(user_id):
            await user_ws.get(user_id).send_text(message)

    return


def get_offline_user_ids(category_id: UUID) -> list[UUID]:
    offline_user: list[UUID] = []
    user_ids = ws_manager.ws_manager.get(category_id)

    for user_id in user_ids:
        if not user_ws.__contains__(user_id):
            offline_user.append(user_id)

    return offline_user