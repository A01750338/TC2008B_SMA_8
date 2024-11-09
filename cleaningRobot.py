# Este programa contiene la implementación de un modelo de simulación de un robot limpiador de celdas sucias. 
# Este robot se desplaza en el limite de un grid y limpia las celdas sucias que se encuentre en su camino.
# Autores: 
#       A01749898 - Jennyfer Nahomi Jasso Hernández
#       A01750338 - Min Che Kim
# Fecha de creación: 07/10/2024
# Última modificación: 08/10/2024

import mesa

def computeCleanedPercentage(model):
    """
        Calcula el porcentaje de celdas limpias después del termino de la simulación.

        Params:
            model: El modelo de la simulación.

        Return:
            float: El porcentaje de celdas limpias.
    """
    return (model.areaGrid - model.dirtyNum) * 100 / model.areaGrid

def computeTotalMoves(model):
    """
        Calcula el número total de movimientos realizados por todos los agentes.

        Params:
            model: El modelo de la simulación.

        Return:
            int: El número total de movimientos.
    """
    return sum([agent.moves for agent in model.schedule.agents])

def computeTotalTime(model):
    """
        Calcula el tiempo total transcurrido en la simulación.

        Params:
            model: El modelo de la simulación.

        Return:
            int: El tiempo total transcurrido.
    """
    return model.schedule.time

class CleaningModel(mesa.Model):
    """
    Clase que representa el modelo de la simulación de un robot limpiador.
    """

    def __init__(self, numAgents, gridWidth, gridHeight, maxTime, dirtyPercentage):
        """
        Inicializa el modelo de la simulación.

        Params:
            numAgents (int): Número de agentes limpiadores.
            gridWidth (int): Ancho de la cuadrícula.
            gridHeight (int): Altura de la cuadrícula.
            maxTime (int): Tiempo máximo de la simulación.
            dirtyPercentage (float): Porcentaje de celdas sucias al inicio.
        """
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

    def step(self):
        """
        Ejecuta un paso de la simulación.
        """
        self.time += 1
        self.schedule.step()
        self.datacollector.collect(self)

        # Detiene la simulación si no hay celdas sucias o se alcanza el tiempo máximo
        if self.dirtyNum == 0 or self.time >= self.maxTime:
            self.running = False


class CleaningAgent(mesa.Agent):
    """
    Clase que representa un agente limpiador en la simulación.
    """

    def __init__(self, uniqueId, model):
        """
        Agente limpiador.

        Params:
            uniqueId (int): ID único del agente.
            model (CleaningModel): El modelo de la simulación.
        """
        super().__init__(uniqueId, model)
        self.moves = 0
        self.cleanedCells = 0

    def move(self):
        """
        Mueve el agente a una nueva posición.
        """
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        
        # Filtra las celdas ocupadas por otros agentes
        filterSteps = []
        for step in possibleSteps:
            cellContent = self.model.grid.get_cell_list_contents([step])
            if not any(isinstance(agent, CleaningAgent) for agent in cellContent):
                filterSteps.append(step)
        possibleSteps = filterSteps
        
        # Mueve el agente a una nueva posición
        if possibleSteps:
            newPos = self.random.choice(possibleSteps)
            self.model.grid.move_agent(self, newPos)
            self.moves += 1
    
    def clean(self):
        """
        Limpia la celda en la que se encuentra el agente.
        """
        cellContent = self.model.grid.get_cell_list_contents([self.pos])
        for current in cellContent:
            # Si la celda es sucia, la limpia
            if isinstance(current, DirtyCell):
                self.model.grid.remove_agent(current)
                self.cleanedCells += 1
                self.model.dirtyNum -= 1
    def step(self):
        """
        Ejecuta un paso del agente.
        """
        self.move()
        self.clean()
        
class DirtyCell(mesa.Agent):
    """
    Clase que representa una celda sucia en la simulación.
    """
    
    def __init__(self, unique_id, model):
        """
        Celda sucia.

        Params:
            unique_id (int): ID único de la celda sucia.
            model (CleaningModel): El modelo de la simulación.
        """
        super().__init__(unique_id, model)