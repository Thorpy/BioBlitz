import asyncio
import json

from typing import Callable
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed
import uvicorn
import sys

app = FastAPI()


class Game:
    def __init__(self):
        self.creature_scores = {
            "shark": 10,
            "dolphin": 5,
            "octopus": 3,
            "jellyfish": 2,
            "clam": 1,
        }
        self.teams = {}

    def get_creature_score(self, creature_name):
        return self.creature_scores.get(creature_name.lower(), 0)

    def add_team(self, team_name):
        team_name_lower = team_name.lower()
        self.teams[team_name_lower] = {"score": 0, "creatures": []}
        return team_name_lower.capitalize()

    def submit_creature(self, team_name, creature_name):
        creature_score = self.get_creature_score(creature_name)
        if team_name.lower() in self.teams:
            if creature_name.lower() not in self.teams[team_name.lower()]["creatures"]:
                self.teams[team_name.lower()]["score"] += creature_score
                self.teams[team_name.lower()]["creatures"].append(creature_name.lower())
        else:
            self.add_team(team_name.lower())
            self.teams[team_name.lower()]["score"] += creature_score
            self.teams[team_name.lower()]["creatures"].append(creature_name.lower())

        data = {"action": "update_team_scores", "teams": self.teams}
        message = json.dumps(data)
        return message



    def get_team_scores(self):
        capitalized_teams = {team_name.capitalize(): data for team_name, data in self.teams.items()}
        data = {"action": "update_team_scores", "teams": capitalized_teams}
        message = json.dumps(data)
        return message




class GameWebSocket(WebSocket):
    websockets = []

    def __init__(self, websocket: WebSocket, receive: Callable, send: Callable):
        super().__init__(websocket, receive=receive, send=send)
        self.teams = {}
        self.game = Game()
        self.application_state = WebSocketState.CONNECTED

        # Open the connection immediately
        asyncio.ensure_future(self.on_connect())

    async def on_connect(self):
        # Add the current instance to the list of websockets.
        self.websockets.append(self)

        # Broadcast the team list and scores to the new client.
        await self.broadcast_team_list()
        await self.broadcast_team_scores()

    async def on_receive(self, message: str):
        # Handle a message from the client.
        data = json.loads(message)
        action = data.get("action")

        if action == "create_team":
            team_name = data.get("team_name")
            if team_name is not None:
                self.game.add_team(team_name)
                await self.broadcast_team_list()

        elif action == "submit_creature":
            team_name = data.get("team_name")
            creature_name = data.get("creature_name")
            if team_name is not None and creature_name is not None:
                self.game.submit_creature(team_name, creature_name)
                await self.broadcast_team_scores()

    async def broadcast_team_list(self):
        # Send the team list to all clients.
        team_list = [team_name for team_name in self.game.teams]
        data = {"action": "update_team_list", "team_list": team_list}
        message = json.dumps(data)
        tasks = []
        for websocket in self.websockets:
            if websocket.application_state == WebSocketState.CONNECTED:
                try:
                    tasks.append(websocket.send_text(message))
                except:
                    self.websockets.remove(websocket)
        try:
            await asyncio.gather(*tasks)
        except:
            print("Someone left and tried to break things")


    async def broadcast_team_scores(self):
        # Send the team scores to all clients.
        message = self.game.get_team_scores()
        tasks = []
        for websocket in self.websockets:
            if websocket.application_state == WebSocketState.CONNECTED:
                try:
                    await websocket.send_text(message)
                except:
                    self.websockets.remove(websocket)
        await asyncio.gather(*tasks)



    async def on_disconnect(self, close_code: int):
        if self in self.websockets:
            self.websockets.remove(self)

    async def on_disconnect(self, close_code: int):
        if self in self.websockets:
            self.websockets.remove(self)



@app.websocket("/game")
async def game(websocket: WebSocket):
    await websocket.accept()
    game_websocket = GameWebSocket(
        websocket, receive=websocket.receive, send=websocket.send
    )
    await game_websocket.on_connect()

    try:
        while True:
            data = await websocket.receive_text()
            await game_websocket.on_receive(data)
    except WebSocketDisconnect:
        await game_websocket.on_disconnect(1000)


@app.get("/")
async def get():
    with open("/home/pi/bioblitz-game/index.html") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.4.1", port=8000)
