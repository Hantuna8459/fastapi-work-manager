from uuid import UUID

from backend.app.main import user_ws
from backend.app.core.database import SessionLocal
from backend.app.crud.user_category import read_list


class WSManager:
    """
        Chứa ws_manager, là một dict:
            1, key: là id của Category (UUID)
            2, value: là một set, gồm các id của User
                đã tham gia Category có id = key (set(UUID))
    """

    ws_manager: dict[UUID, set[UUID]]

    def __init__(self) -> None:
        self.ws_manager = {}
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

    def notify(self, category_id: UUID, message: str) -> None:
        """
            Gửi notification đến các User join Category qua websocket
        """

        user_ids = self.ws_manager.get(category_id)

        for user_id in user_ids:
            if user_ws.__contains__(user_id):
                user_ws.get(user_id).send_text(message)

        return

    def get_offline_user_ids(self, category_id: UUID) -> list[UUID]:

        offline_user: list[UUID] = []
        user_ids = self.ws_manager.get(category_id)

        for user_id in user_ids:
            if not user_ws.__contains__(user_id):
                offline_user.append(user_id)

        return offline_user

    def add_category_id(self, category_id: UUID) -> None:
        self.ws_manager[category_id] = set()
        return

    def add_user_id(self, category_id: UUID, user_id: UUID) -> None:
        self.ws_manager.get(category_id).add(user_id)
        return

    def remove_user_id(self, category_id: UUID, user_id: UUID) -> None:
        self.ws_manager.get(category_id).remove(user_id)
        return