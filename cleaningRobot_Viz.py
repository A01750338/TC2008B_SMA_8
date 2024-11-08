from cleaningRobot import mesa, CleaningModel, CleaningAgent, DirtyCell

def agent_portrayal(agent):
    if isinstance(agent, DirtyCell):
        portrayal = {
            "Shape": "circle",
            "Color": "red",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5,
        }
    elif isinstance(agent, CleaningAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 1,
            "r": 0.5,
        }
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(
    CleaningModel, [grid], "Cleaning Model", {"numAgents": 10, "gridWidth": 10, "gridHeight": 10, "maxTime": 100, "dirtyPercentage": 20}
)
server.port = 8000
server.launch()