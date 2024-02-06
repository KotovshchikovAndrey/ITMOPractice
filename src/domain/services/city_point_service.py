from kink import inject

from domain.repositories.city_point_repository import ICityPointRepository


@inject
class CityPointService:
    _repository: ICityPointRepository

    def __init__(self, repository: ICityPointRepository) -> None:
        self._repository = repository

    async def test_init(self):
        return await self._repository.test_init()
