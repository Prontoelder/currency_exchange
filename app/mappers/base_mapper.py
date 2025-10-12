from abc import ABC


class BaseMapper(ABC):
    pass
    # @staticmethod
    # # @abstractmethod
    # def row_to_entity(row: sqlite3.Row):
    #     pass
    #
    # @staticmethod
    # def dict_to_entity(entity_class, data: dict):
    #     filtered_data = {
    #         key: value
    #         for key, value in data.items()
    #         if key in entity_class.__annotations__
    #     }
    #     return entity_class(**filtered_data)


    # """
    # Абстрактный базовый класс для всех мапперов.
    # Определяет "контракт", которому должны следовать все конкретные мапперы.
    # """
    #
    # @abstractmethod
    # def entity_to_dto(self, entity: Any) -> Any:
    #     """
    #     Преобразует модель базы данных (Entity)
    #     в объект передачи данных (DTO).
    #     """
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def dict_to_dto(self, data: dict) -> Any:
    #     """
    #     Преобразует словарь в объект передачи данных (DTO).
    #     """
    #     raise NotImplementedError
