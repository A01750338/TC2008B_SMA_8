import mesa
import seaborn as sns
import numpy as np
import pandas as pd

def computeCleanedPercentage(model):
    return (model.areaGrid - model.dirtyNum) * 100 / model.areaGrid

def computeTotalMoves(model):
    return sum([agent.moves for agent in model.schedule.agents])

def computeTotalTime(model):
    return model.schedule.time

class CleaningModel(mesa.Model):
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

    def step(self):
        self.time += 1
        self.schedule.step()
        self.datacollector.collect(self)
        if self.dirtyNum == 0 or self.time >= self.maxTime:
            self.running = False


class CleaningAgent(mesa.Agent):
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.moves = 0
        self.cleanedCells = 0

    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        newPos = self.random.choice(possibleSteps)
        self.model.grid.move_agent(self, newPos)
        self.moves += 1
    
    def clean(self):
        cellContent = self.model.grid.get_cell_list_contents([self.pos])
        for current in cellContent:
            if isinstance(current, DirtyCell):
                self.model.grid.remove_agent(current)
                self.cleanedCells += 1
                self.model.dirtyNum -= 1

    def step(self):
        self.move()
        self.clean()
        
class DirtyCell(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)