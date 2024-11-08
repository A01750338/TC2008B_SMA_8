from cleaningRobot import mesa, CleaningModel, CleaningAgent, DirtyCell
import random
def agent_portrayal(agent):
    if isinstance(agent, DirtyCell):
        portrayal = {
            "Shape": "plant.png",
            "Layer": 0,
            "r": 0.5,
        }
    elif isinstance(agent, CleaningAgent):
        portrayal = {
            "Shape": "wall_e.png",
            "Layer": 1,
            "r": 0.5,
        }
    return portrayal

# Gráficas de la simulación
# Total time: Tiempo total de la simulación
totalTimeGraph = mesa.visualization.ChartModule([
    {"Label": "Tiempo total",
    "Color": "Green"}],
    data_collector_name='datacollector'
)

# Cleaned cells (percentage): Porcentaje de celdas limpias
cleanPercentageGraph = mesa.visualization.ChartModule([
    {"Label": "Porcentaje de celdas limpias",
    "Color": "Blue"}],
    data_collector_name='datacollector'
)

# Total moves: Número total de movimientos de los agentes
totalMovesGraph = mesa.visualization.ChartModule([
    {"Label": "Movimientos totales",
    "Color": "Purple"}],
    data_collector_name='datacollector'
)
width = random.randint(4, 16)
height = random.randint(4, 16)

numAgents = random.randint(1, 10)
percentage = random.randint(5, 95)

grid = mesa.visualization.CanvasGrid(agent_portrayal, width, height, 500, 500)
server = mesa.visualization.ModularServer(
    CleaningModel, [grid, totalTimeGraph, cleanPercentageGraph, totalMovesGraph], "M1 Actividad: Wall-E y su plantita", {"numAgents": numAgents, "gridWidth": width, "gridHeight": height, "maxTime": 120, "dirtyPercentage": percentage}
)
server.description = "Jennyfer Nahomi Jasso Hernández - A01749898 / Min Che Kim - A01750338"
server.port = 8000
server.launch()