from fastapi import WebSocket
from uuid import UUID

from backend.app.core.database import SessionLocal
from backend.app.crud.user_category import read_list


class WSManager:
    """
        Chứa ws_manager, là một dict:
            1, key: là id của Category (UUID)
            2, value: là một set, gồm các id của User
                đã join Category có id = key (set(UUID))
    """

    # Singleton
    _instance = None

    # Attribute
    user_ws: dict[UUID, WebSocket]
    ws_manager: dict[UUID, set[UUID]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WSManager, cls).__new__(cls)
            cls._instance.user_ws = {}
            cls._instance.ws_manager = {}

        return cls._instance

    def __init__(self) -> None:
        return

    async def add_information(self) -> None:
        manager = self.ws_manager

        async with SessionLocal() as db:
            seq = await read_list(db)
            for user_category in seq:
                category_id = user_category[0]
                user_id = user_category[1]

                if not manager.__contains__(category_id):
                    manager.update({category_id: set()})

                manager.get(category_id).add(user_id)

        self.ws_manager = manager
        return

    def add_ws(self, ws: dict[UUID, WebSocket]) -> None:
        self.user_ws.update(ws)
        return

    def remove_ws(self, user_id: UUID) -> None:
        self.user_ws.pop(user_id)
        return

    async def notify(self, category_id: UUID, message: str) -> None:
        """
            Gửi notification đến các User join Category qua websocket
        """
        ws = self.user_ws
        user_ids = self.ws_manager.get(category_id)

        for user_id in user_ids:
            if ws.__contains__(user_id):
                await ws.get(user_id).send_text(message)

        return

    def get_offline_user_ids(self, category_id: UUID) -> list[UUID]:
        offline_user: list[UUID] = []
        user_ids = self.ws_manager.get(category_id)
        ws = self.user_ws

        for user_id in user_ids:
            if not ws.__contains__(user_id):
                offline_user.append(user_id)

        return offline_user

    # Update dữ liệu của ws_manager
    def add_category_id(self, category_id: UUID) -> None:
        self.ws_manager[category_id] = set()
        return

    def add_user_id(self, category_id: UUID, user_id: UUID) -> None:
        self.ws_manager.get(category_id).add(user_id)
        return

    def remove_user_id(self, category_id: UUID, user_id: UUID) -> None:
        self.ws_manager.get(category_id).remove(user_id)
        return