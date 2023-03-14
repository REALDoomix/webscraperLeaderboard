import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    rank: int
    name: str
    link: str
    img: str

    @staticmethod
    def from_dict(data: dict):
        record = PlayerModel(**data)
        return record


class Problem(BaseModel):
    detail: str


class Database:
    def __init__(self):
        self._data: list = []

    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = PlayerModel.from_dict(record)
                self._data.append(obj)

    def delete(self, rank: int):
        if 0 < rank >= len(self._data):
            return
        self._data.pop(rank)

    def add(self, player:PlayerModel ):
        self._data.append(player)

    def get(self, rank: int):
        if 0 < rank >= len(self._data):
            return
        return self._data[rank]

    def get_all(self) -> list[PlayerModel]:
        return self._data

    def update(self, rank: int, player:PlayerModel ):
        if 0 < rank >= len(self._data):
            return
        self._data[rank] = player

    def count(self) -> int:
        return len(self._data)


db = Database()
db.load_from_filename('leaderboard.json')

app = FastAPI(title="Leaderboard API", version="0.1", docs_url="/docs")

app.is_shutdown = False


@app.get("/players", response_model=list[PlayerModel], description="Returns list of players")
async def get_players():
    return db.get_all()


@app.get("/players/{rank}", response_model=PlayerModel)
async def get_player(rank: int):
    return db.get(rank-1)


@app.post("/players", response_model=PlayerModel, description="Přidáme film do DB")
async def post_players(player:PlayerModel ):
    db.add(player)
    return player


@app.delete("/players/{rank}", description="Deletes player from DB", responses={
    404: {'model': Problem}
})
async def delete_player(rank: int):
    player = db.get(rank)
    if player is None:
        raise HTTPException(404, "Player does not exist")
    db.delete(rank-1)
    return {'status': 'smazano'}


@app.patch("/players/{rank}", description="Updates player from DB", responses={
    404: {'model': Problem}
})
async def update_leaderboard(rank: int, updated_player:PlayerModel ):
    player = db.get(rank)
    if player is None:
        raise HTTPException(404, "Player does not exist")
    db.update(rank, updated_player)
    return {'old': player, 'new': updated_player}