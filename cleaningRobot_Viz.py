# Este archivo contiene la configuración de la visualización de la simulación de un robot limpiador.
# Autores: 
#       A01749898 - Jennyfer Nahomi Jasso Hernández
#       A01750338 - Min Che Kim
# Fecha de creación: 07/10/2024
# Última modificación: 08/10/2024

from cleaningRobot import mesa, CleaningModel, CleaningAgent, DirtyCell

def agent_portrayal(agent):
    """
    Define la repesentación visual de los agentes en la simulación.

    Params:
    agent: El agente a representar

    Return:
    portrayal: Diccionario con la representación visual del agente
    """
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
#Tiempo total de la simulación
totalTimeGraph = mesa.visualization.ChartModule([
    {"Label": "Tiempo total",
    "Color": "Green"}],
    data_collector_name='datacollector'
)

#Porcentaje de celdas limpias
cleanPercentageGraph = mesa.visualization.ChartModule([
    {"Label": "Porcentaje de celdas limpias",
    "Color": "Blue"}],
    data_collector_name='datacollector'
)

# Número total de movimientos de los agentes
totalMovesGraph = mesa.visualization.ChartModule([
    {"Label": "Movimientos totales",
    "Color": "Purple"}],
    data_collector_name='datacollector'
)

gridWidth = 7
gridHeight = 20
baseCanvasSize = 500

# Calcula el tamaño del CanvasGrid para mantener la proporción correcta
if gridWidth >= gridHeight:
    canvasWidth = baseCanvasSize
    canvasHeight = int(baseCanvasSize * (gridHeight / gridWidth))
else:
    canvasHeight = baseCanvasSize
    canvasWidth = int(baseCanvasSize * (gridWidth / gridHeight))

grid = mesa.visualization.CanvasGrid(agent_portrayal, gridWidth, gridHeight, canvasWidth, canvasHeight)

server = mesa.visualization.ModularServer(
    CleaningModel, [grid, totalTimeGraph, cleanPercentageGraph, totalMovesGraph], "M1 Actividad: Wall-E y su plantita", {"numAgents": 12, "gridWidth": gridWidth, "gridHeight": gridHeight, "maxTime": 120, "dirtyPercentage": 30}
)
server.description = "Jennyfer Nahomi Jasso Hernández - A01749898 / Min Che Kim - A01750338"
server.port = 8000
server.launch()