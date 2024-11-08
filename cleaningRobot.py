# Este programa contiene la implementación de un modelo de simulación de un robot limpiador de celdas sucias. 
# Este robot se desplaza en el limite de un grid y limpia las celdas sucias que se encuentre en su camino.
# Autores: 
#       A01749898 - Jennyfer Nahomi Jasso Hernández
#       A01750338 - Min Che Kim
# Fecha de creación: 07/10/2024
# Última modificación: 08/10/2024

import mesa

"""
    Calcula el porcentaje de celdas limpias después del termino de la simulación.

    Params:
        model: El modelo de la simulación.

    Return:
        float: El porcentaje de celdas limpias.
"""
def computeCleanedPercentage(model):
    return (model.areaGrid - model.dirtyNum) * 100 / model.areaGrid

"""
    Calcula el número total de movimientos realizados por todos los agentes.

    Params:
        model: El modelo de la simulación.

    Return:
        int: El número total de movimientos.
"""
def computeTotalMoves(model):
    return sum([agent.moves for agent in model.schedule.agents])

"""
    Calcula el tiempo total transcurrido en la simulación.

    Params:
        model: El modelo de la simulación.

    Return:
        int: El tiempo total transcurrido.
"""
def computeTotalTime(model):
    return model.schedule.time

class CleaningModel(mesa.Model):

    """
    Modelo de simulación de limpieza.

    Params:
        numAgents (int): Número de agentes limpiadores.
        gridWidth (int): Ancho de la cuadrícula.
        gridHeight (int): Altura de la cuadrícula.
        maxTime (int): Tiempo máximo de la simulación.
        dirtyPercentage (float): Porcentaje de celdas sucias al inicio.
    """
    def __init__(self, numAgents, gridWidth, gridHeight, maxTime, dirtyPercentage):
        super().__init__()
        self.numAgents = numAgents
        self.grid = mesa.space.MultiGrid(gridWidth, gridHeight, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.areaGrid = gridWidth * gridHeight
        self.dirtyNum = int(self.areaGrid * (dirtyPercentage/100))
        self.maxTime = maxTime
        self.time = 0

        # Crea los agentes
        for i in range(self.numAgents):
            cleanAgent = CleaningAgent(i, self)
            self.schedule.add(cleanAgent)

            # Inicializa los agentes en la celda (1, 1)
            self.grid.place_agent(cleanAgent, (1, 1))

        # Crea las celdas sucias
        for i in range(self.dirtyNum):
            dirtyCell = DirtyCell(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(dirtyCell, (x, y))

        # Guardar los datos de la simulación
        self.datacollector = mesa.datacollection.DataCollector(
            model_reporters={"Tiempo total": computeTotalTime, "Movimientos totales": computeTotalMoves, "Porcentaje de celdas limpias": computeCleanedPercentage},
            agent_reporters={"Movimientos": "moves", "Celdas limpias": "cleanedCells", "Celdas sucias": "dirtyNum"}
        )

    """
    Ejecuta un paso de la simulación.
    """
    def step(self):
        self.time += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Detiene la simulación si no hay celdas sucias o se alcanza el tiempo máximo
        if self.dirtyNum == 0 or self.time >= self.maxTime:
            self.running = False


class CleaningAgent(mesa.Agent):
    """
    Agente limpiador.

    Params:
        uniqueId (int): ID único del agente.
        model (CleaningModel): El modelo de la simulación.
    """
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.moves = 0
        self.cleanedCells = 0

    """
    Mueve el agente a una nueva posición.
    """
    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        newPos = self.random.choice(possibleSteps)
        self.model.grid.move_agent(self, newPos)
        self.moves += 1
    
    """
    Limpia la celda en la que se encuentra el agente.
    """
    def clean(self):
        cellContent = self.model.grid.get_cell_list_contents([self.pos])
        for current in cellContent:
            if isinstance(current, DirtyCell):
                self.model.grid.remove_agent(current)
                self.cleanedCells += 1
                self.model.dirtyNum -= 1

    """
    Ejecuta un paso del agente.
    """
    def step(self):
        self.move()
        self.clean()
        
class DirtyCell(mesa.Agent):
    """
    Celda sucia.

    Params:
        unique_id (int): ID único de la celda sucia.
        model (CleaningModel): El modelo de la simulación.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)