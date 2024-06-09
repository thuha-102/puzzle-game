import sys, pygame
import time
import json
from pipePuzzle import *
import time

size = width, height = 1200, 960

pygame.display.set_caption("PIPES PUZZLE")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(size)

BLIND_SOLVE = pygame.font.SysFont('Corbel', 20) .render('Blind Solve' , True , (0, 0, 0))
HEURISTIC_SOLVE = pygame.font.SysFont('Corbel', 20) .render('Heuristic Solve' , True , (0, 0, 0))
FILENAMES = [
    "2x1.json", "2x2.json", "3x3.json", "4x4.json", "5x5.json", "7x7.json", "10x10.json"
]
GRAPHS = [
    pygame.font.SysFont('Corbel', 20) .render('1X2' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('2X2' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('3X3' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('4X4' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('5X5' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('7X7' , True , (0, 0, 0)),
    pygame.font.SysFont('Corbel', 20) .render('10X10' , True , (0, 0, 0))
]

blind_start_time = 0
blind_end_time = 0
blind_max_nodes = 0
blind_loop = 0

heuristic_start_time = 0
heuristic_end_time = 0
heuristic_pre_max_nodes = 0
heuristic_pre_loop = 0
heuristic_max_nodes = 0
heuristic_loop = 0

def pipeImage(type, index, width):
    if type is Tpipe:
        image = pygame.image.load(f"assets/Tpipe{index}.png")
    elif type is Lpipe:
        image = pygame.image.load(f"assets/Lpipe{index}.png")
    elif type is Ipipe:
        image = pygame.image.load(f"assets/Ipipe{index}.png")
    else:
        image = pygame.image.load(f"assets/Epoint{index}.png")

    image = pygame.transform.scale(image, (width, width))
    
    return image

def readGraph(fileName: str):
    mainGraph: list[list[Epoint | Tpipe | Lpipe | Ipipe]] = []
    
    with open(f"input/{fileName}", "r") as file:
        data = json.load(file)
    i = 0
    for _ in data:
        row = []
        j = 0
        for d in _:
            if d["type"] == "E":
                row += [Epoint(i, j, int(d["index"]))]
            elif d["type"] == "L":
                row += [Lpipe(i, j, int(d["index"]))]
            elif d["type"] == "T":
                row += [Tpipe(i, j, int(d["index"]))]
            elif d["type"] == "I":
                row += [Ipipe(i, j, int(d["index"]))]
            j += 1
        i += 1
        mainGraph += [row]
        
    return Graph(mainGraph)

mainGraph = readGraph(FILENAMES[0])

def drawGraph(graph: Graph, BaseX, BaseY):
    baseY = BaseY
    
    for i in range(graph.row):
        baseX = BaseX
        for j in range(graph.col):
            t = type(graph.graph[i][j])
            index = graph.graph[i][j].index
            
            screen.blit(pipeImage(t, index, CELL_WIDTH), (baseX, baseY))
            baseX += CELL_WIDTH
        baseY += CELL_WIDTH

def drawDemoSolve(graph: Graph, transforms: list[Transform], BaseX, BaseY):
    baseY = BaseY
    
    for i in range(graph.row):
        baseX = BaseX
        for j in range(graph.col):
            t = type(graph.graph[i][j])
            index = graph.graph[i][j].index
            
            screen.blit(pipeImage(t, index, CELL_WIDTH), (baseX, baseY))
            baseX += CELL_WIDTH
        baseY += CELL_WIDTH
    
    baseY = BaseY
    baseX = BaseX
    
    for t in transforms:
        row = t.row
        col = t.col
        X = baseX + CELL_WIDTH*col
        Y = baseY + CELL_WIDTH*row
        for _ in range(t.times):
            t = type(graph.graph[row][col])
            
            graph.graph[row][col].leftRotate()
            index = graph.graph[row][col].index
            
            screen.blit(pipeImage(t, index, CELL_WIDTH), (X, Y))
            pygame.display.update()
            pygame.time.delay(300)

def solvedGraph(graph, type: str):
    solvedGraph: Graph = copy.deepcopy(graph)
    if type == 'blind':
        return solvedGraph.blindSolve()
    else:
        return solvedGraph.heuristicSolve()

while True:
    CELL_WIDTH = 100 if mainGraph.row < 10 else 70
    BASE_X_GRAPH = (width - CELL_WIDTH*mainGraph.col)//2
    BASE_Y_GRAPH = (height - CELL_WIDTH*mainGraph.col)//2

    screen.fill((0, 255, 255))
    mouse = pygame.mouse.get_pos()
    
    baseX = 5
    baseY = 5
    for i in range(len(GRAPHS)):
        if i != 0 and i % 5 == 0:
            baseY += 50
            baseX = 5

        _ = GRAPHS[i]
        pygame.draw.rect(screen, (170, 170, 170), [baseX, baseY, 100, 40]) 
        screen.blit(_ , (baseX + 30, baseY + 10))
        baseX += 125
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if width - 300 <= mouse[0] <= width - 100 and 5 <= mouse[1] <= 45:
                blind_start_time = time.time()
                transforms, blind_max_nodes, blind_loop = solvedGraph(mainGraph, "blind")
                blind_end_time = time.time()
                drawDemoSolve(mainGraph, transforms, BASE_X_GRAPH, BASE_Y_GRAPH)
                
            if width - 300 <= mouse[0] <= width - 100 and 50 <= mouse[1] <= 90:
                heuristic_start_time = time.time()
                transforms, heuristic_pre_max_nodes, heuristic_max_nodes, heuristic_pre_loop, heuristic_loop = solvedGraph(mainGraph, "heuristic")
                heuristic_end_time = time.time()
                drawDemoSolve(mainGraph, transforms, BASE_X_GRAPH, BASE_Y_GRAPH)
                
            if 5 <= mouse[0] <= 100 and 5 <= mouse[1] <= 45:
                mainGraph = readGraph(FILENAMES[0])
                
            if 125 <= mouse[0] <= 225 and 5 <= mouse[1] <= 45:
                mainGraph = readGraph(FILENAMES[1])
                
            if 250 <= mouse[0] <= 350 and 5 <= mouse[1] <= 45:
                mainGraph = readGraph(FILENAMES[2])
            
            if 375 <= mouse[0] <= 475 and 5 <= mouse[1] <= 45:
                mainGraph = readGraph(FILENAMES[3])
            
            if 500 <= mouse[0] <= 600 and 5 <= mouse[1] <= 45:
                mainGraph = readGraph(FILENAMES[4])
            
            if 5 <= mouse[0] <= 100 and 55 <= mouse[1] <= 95:
                mainGraph = readGraph(FILENAMES[5])
            
            if 125 <= mouse[0] <= 225 and 55 <= mouse[1] <= 95:
                mainGraph = readGraph(FILENAMES[6])
            
            if 0 <= mouse[0] <= 900 and height - 100 <= mouse[1] <= height - 60:
                heuristic_end_time = heuristic_start_time = heuristic_pre_max_nodes = heuristic_max_nodes = heuristic_pre_loop = heuristic_loop = 0
            
            if 0 <= mouse[0] <= 900 and height - 50 <= mouse[1] <= height - 10:
                blind_end_time = blind_start_time = blind_max_nodes = blind_loop = 0
                
            if (width - CELL_WIDTH*mainGraph.col)/2 <= mouse[0] <= (width - CELL_WIDTH*mainGraph.col)/2 + CELL_WIDTH*mainGraph.col and (height - CELL_WIDTH*mainGraph.row)/2 <= mouse[1] <= (height - CELL_WIDTH*mainGraph.row)/2 + CELL_WIDTH*mainGraph.row:
                col = min((mouse[0] - BASE_X_GRAPH)//CELL_WIDTH, mainGraph.col - 1)
                row = min((mouse[1] - BASE_Y_GRAPH)//CELL_WIDTH, mainGraph.row - 1)
                
                if event.button == pygame.BUTTON_LEFT:
                    mainGraph.graph[row][col].leftRotate()
                else:
                    mainGraph.graph[row][col].rightRotate()
    
    drawGraph(mainGraph, BASE_X_GRAPH, BASE_Y_GRAPH)
    pygame.draw.rect(screen, (170, 170, 170), [width - 300, 5, 200, 40]) 
    screen.blit(BLIND_SOLVE , (width - 250, 15))
    
    pygame.draw.rect(screen, (170, 170, 170), [width - 300, 50, 200, 40]) 
    screen.blit(HEURISTIC_SOLVE , (width - 250, 60))
    
    HERISTIC_DURATION_TIME = pygame.font.SysFont('Corbel', 30).render(f"Heuristic:      {round(heuristic_end_time - heuristic_start_time, 4)}  s                             {heuristic_pre_max_nodes}, {heuristic_max_nodes}                             {heuristic_pre_loop}, {heuristic_loop}" , True , (0, 0, 0))
    pygame.draw.rect(screen, (170, 170, 170), [0, height - 100, 900, 40]) 
    screen.blit(HERISTIC_DURATION_TIME , (20, height - 90))
    
    BLIND_DURATION_TIME = pygame.font.SysFont('Corbel', 30).render(f"Blind:             {round(blind_end_time - blind_start_time, 4)}  s                             {blind_max_nodes}                             {blind_loop}" , True , (0, 0, 0))
    pygame.draw.rect(screen, (170, 170, 170), [0, height - 50, 900, 40]) 
    screen.blit(BLIND_DURATION_TIME , (20, height - 40))

    pygame.display.update()