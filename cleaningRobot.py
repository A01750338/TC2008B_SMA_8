import mesa
import seaborn as sns
import numpy as np
import pandas as pd

def computeCleanedPercentage(self):
    return (self.areaGrid - self.dirtyNum) * 100 / self.areaGrid

class CleaningModel(mesa.Model):
    def __init__(self, numAgents, gridWidth, gridHeight, maxTime, dirtyPercentage):
        super().__init__()
        self.numAgents = numAgents
        self.grid = mesa.space.MultiGrid(gridWidth, gridHeight, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.areaGrid = gridWidth * gridHeight
        self.dirtyNum = self.areaGrid * (dirtyPercentage/100)

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

        self.maxTime = maxTime

        # Guardar los datos de la simulación
        self.datacollector = mesa.datacollection.DataCollector(
            modelReporters={"Total time": "totalTime", "Total moves": "moves", "Cleaned cells (percentage)": "computeCleanedPercentage"},
            agentReporters={"Moves": "moves", "Cleaned cells": "cleanedCells"}
        )

    def step(self):
        self.schedule.step()

class CleaningAgent(mesa.Agent):
    def __init__(self, numAgents, uniqueId, model):
        super().__init__(uniqueId, model)
        # Create the agent's variable and set the initial values.
        self.moves = 0
        self.cleanedCells = 0
        #self.numAgents = N
        #self.dirty_percentage

    
    def step(self):
        cellContent = self.model.grid.cellContent(self.pos)
        for elem in cellContent:
            if type(elem) is DirtyCell:
                ...
        
class DirtyCell(mesa.Agent):
    def __init__(self, uniqueId, model):
        
        ...

        
