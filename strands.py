import random
from visualizer import draw_board
import copy

ROWS, COLS = 8, 6
starting_points = [
        [0, 2], [0, 3], [7, 2], [7, 3],
        [2, 0], [3, 0], [4, 0], [5, 0],
        [2, 5], [3, 5], [4, 5], [5, 5]
    ]
border = []
for c in range(COLS):
    border.append([0, c])

# Bottom row
for c in range(COLS):
    border.append([ROWS - 1, c])

# Left col
for r in range(1, ROWS - 1):
    border.append([r, 0])

# Right col
for r in range(1, ROWS - 1):
    border.append([r, COLS - 1])
def generate_empty_board():
    return [[' ' for y in range(COLS)] for x in range(ROWS)]



def manhattan(pos1,pos2):
    x,y = pos1
    x1,y1 = pos2

    return (abs(x-x1) + abs(y-y1))

def generateSpanagram(words, max_attempts=500):
    n = len(words[0])  # Length the path should be
    #starting points to too close to edge lol
    starting_points = [
        [0, 2], [0, 3], [7, 2], [7, 3],
        [2, 0], [3, 0], [4, 0], [5, 0],
        [2, 5], [3, 5], [4, 5], [5, 5]
    ]
    #spam until it works
    attempts = 0


    while attempts < max_attempts:
        #get an empty board
        board = generate_empty_board()

        #direction the spanagram is going to go in
        dir = ""

        #start is a random point thats in the legal points
        start = random.choice(starting_points)
        

        #this just sets the direction and endpoint based on whatever
        if start in [[0, 2], [0, 3]]:
            end = random.choice([[7, 2], [7, 3]])
            dir = "vertical"
        elif start in [[7, 2], [7, 3]]:
            end = random.choice([[0, 2], [0, 3]])
            dir = "vertical"
        elif start in [[2, 0], [3, 0], [4, 0], [5, 0]]:
            end = random.choice([[2, 5], [3, 5], [4, 5], [5, 5]])
            dir = "horizontal"
        elif start in [[2, 5], [3, 5], [4, 5], [5, 5]]:
            end = random.choice([[2, 0], [3, 0], [4, 0], [5, 0]])
            dir = "horizontal"
        else:
            attempts += 1
            continue
        

        #if the word cant go all the way then restart
        if manhattan(start,end) > n:
            attemps += 1
            continue 


        #get the path
        path = find_path_of_length(start, end, n)

        #if there is a path go through and set the letters
        if path:
            board[start[0]][start[1]] = words[0][0].upper()
            board[end[0]][end[1]] = words[0][-1].upper()
            i = 0
            for row, col in path:
                if board[row][col] == ' ':
                    board[row][col] = words[0][i].upper()
                i += 1



            #This gets the count of each side and the legal nodes on each side
            #The count is used for 3 sum as the target


            sidecount = 0
            side1 = []
            side2= []

            #This basically goes up or down from every row or col and waits til it hits a letter otherwise logging every other position
            if dir == "vertical":
                for i in range(len(board)):
                    for j in range(len(board[i])):
                        if board[i][j] != ' ':
                            break
                        else:
                            side1.append([i,j])
                            sidecount +=1
            else:
                for j in range(len(board[0])):
                    for i in range(len(board)):
                        if board[i][j] != ' ':
                            break
                        else:
                            side1.append([i,j])
                            sidecount +=1

            
            if dir == "vertical":
                for i in reversed(range(len(board))):
                        for j in reversed(range(len(board[i]))):
                            if board[i][j] != ' ':
                                break
                            else:
                                side2.append([i,j])
            else:
                for j in reversed(range(len(board[0]))):
                    for i in reversed(range(len(board))):
                        if board[i][j] != ' ':
                            break
                        else:
                            side2.append([i,j])

            return board, path, side1, side2, sidecount



        attempts += 1

    raise Exception("Failed to find a valid spanagram path after many tries.")


#This runs a recursive dfs that finds the path for the spanagram
def find_path_of_length(start, end, length):
    # Inner recursive function to do DFS
    def dfs(path, visited):
        # If path is already too long then dip
        if len(path) > length:
            return None
        # If path is the exact length and ends at the target, then done
        if len(path) == length and path[-1] == tuple(end):
            return path
        # Get valid neighbors from the current position
        neighbors = get_neighbors(path[-1], visited, border)
        random.shuffle(neighbors)  # Shuffle to make it more random

        # Try each neighbor recursively
        for neighbor in neighbors:
            result = dfs(path + [neighbor], visited | {neighbor})
            if result:
                return result  # If we found a valid path, return it

        return None  # If nothing worked, go back

    # Start DFS with the initial position
    return dfs([tuple(start)], {tuple(start)})



#get tge neighbors of a node not diagonal and valid and not in visited
def get_neighbors(position, visited, borders):
    neighbors = []
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in visited and (r,c) not in borders:
            neighbors.append((r, c))
    return neighbors


#Use three sum algo to find all posible matches to where the combined word length is = to sidecount 
#Using three sum 
def validsides(sidecount,words):
    #make a deep copy to pop
    wordscopy = copy.deepcopy(words)
    wordscopy.pop(0)
    res = []
    #sort by length of string
    wordscopy.sort(key=len)


    #use 3sum to get one side with three words (might change later not the best way to do it)
    #credit: https://leetcode.com/problems/3sum/solutions/7392/python-easy-to-understand-solution-o-n-n-time/
    for i in range(len(wordscopy)-2):
        if i > sidecount and len(wordscopy[i]) == len(wordscopy[i-1]):
            continue
        l, r = i+1, len(wordscopy)-1
        while l < r:
            s = len(wordscopy[i]) + len(wordscopy[l]) + len(wordscopy[r])
            if s < sidecount:
                l +=1 
            elif s > sidecount:
                r -= 1
            else:
                res.append([wordscopy[i], wordscopy[l], wordscopy[r]])
                while l < r and len(wordscopy[l]) == len(wordscopy[l+1]):
                    l += 1
                while l < r and len(wordscopy[r]) == len(wordscopy[r-1]):
                    r -= 1
                l += 1; r -= 1
    return res

#get valid neighbors that are not diagonal to pos difference with this and get_neighbors is this doesnt take in visited or borders
def get_valid_nondiag_neighbors(position,board):
    neighbors = []
    row,col = position
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    for dy, dx in directions:
        y,x = row +dy, col + dx
        if 0 <= y < ROWS and 0 <= x < COLS and board[y][x] == ' ':
            neighbors.append([y,x])
    return neighbors

#generate the top or left side. This side will have three words
def generate_side1(board, side1, words):
    from collections import deque
    import random

    all_paths = []

    availableSet = {tuple(cell) for cell in side1}

    for i, word in enumerate(words):
        word_length = len(word)

        if i == 0 and board[0][0] == ' ' and (0, 0) in availableSet:
            startCell = [0, 0]
        else:
            possibleStarts = [list(cell) for cell in availableSet if board[cell[0]][cell[1]] == ' ']
            if not possibleStarts:
                return []  
            startCell = random.choice(possibleStarts)

        queue = deque()
        queue.append(([startCell], {tuple(startCell)}))
        foundPath = None

        # Perform BFS until path of correct length
        while queue:
            currentPath, visitedCells = queue.popleft()

            if len(currentPath) == word_length:
                foundPath = currentPath
                break

            # Get the last cell in the current path.
            lastCell = currentPath[-1]

            # Look through each valid neighbor 
            for neighbor in get_valid_nondiag_neighbors(lastCell, board):
                neighborTuple = tuple(neighbor)
                if (neighborTuple not in visitedCells and neighborTuple in availableSet and board[neighbor[0]][neighbor[1]] == ' '):
                    newPath = currentPath + [neighbor]
                    newVisited = visitedCells | {neighborTuple}
                    queue.append((newPath, newVisited))

        # If no valid path was found for this word, return an empty list.
        if foundPath is None:
            return []

        # Place the word's letters along the found path.
        for idx, (r, c) in enumerate(foundPath):
            board[r][c] = word[idx].upper()

        # Append found path
        all_paths.append(foundPath)

        # Remove the positions used by this word from the avalible
        for cell in foundPath:
            availableSet.discard(tuple(cell))

    return all_paths

#generate the bottom or left side, this will have len(words) - 3 words
def generate_side2(board, side2, words):
    from collections import deque
    import random

    all_paths = []

    availableSet = {tuple(cell) for cell in side2}

    for i, word in enumerate(words):
        word_length = len(word)

        if i == 0 and board[0][0] == ' ' and (0, 0) in availableSet:
            startCell = [0, 0]
        else:
            possibleStarts = [list(cell) for cell in availableSet if board[cell[0]][cell[1]] == ' ']
            if not possibleStarts:
                return []  
            startCell = random.choice(possibleStarts)

        queue = deque()
        queue.append(([startCell], {tuple(startCell)}))
        foundPath = None

        # Perform BFS until path of correct length
        while queue:
            currentPath, visitedCells = queue.popleft()

            if len(currentPath) == word_length:
                foundPath = currentPath
                break

            lastCell = currentPath[-1]

            for neighbor in get_valid_nondiag_neighbors(lastCell, board):
                neighborTuple = tuple(neighbor)
                if (neighborTuple not in visitedCells and 
                    neighborTuple in availableSet and 
                    board[neighbor[0]][neighbor[1]] == ' '):
                    newPath = currentPath + [neighbor]
                    newVisited = visitedCells | {neighborTuple}
                    queue.append((newPath, newVisited))
        # If no valid path was found for this word, return an empty list.
        if foundPath is None:
            return []

        for idx, (r, c) in enumerate(foundPath):
            board[r][c] = word[idx].upper()

        all_paths.append(foundPath)
        # Remove the positions used by this word from the avalible
        for cell in foundPath:
            availableSet.discard(tuple(cell))

    return all_paths



def main(words):
    res = []
    while True:
        board, path, side1, side2, sidecount = generateSpanagram(words)
        res = validsides(sidecount,words)
        print(res)
        s1 = []
        s2 = []
        words1 =[]
        words2 = []
        if res:
            words1 = random.choice(res)
            words2=[]
            s1 = generate_side1(board,side1,words1)
            for item in words:
                if item not in words1 and item != words[0]:
                    words2.append(item)
            s2 = generate_side2(board,side2,words2)

        if len(s2) == len(words2) and s1 != [] and s2 != []:
            print(s1,s2)
            draw_board(board)
            break

        
    print("Path found:", path)



main(["springtime", "showers", "robins", "puddles", "blossoms", "buds", "pollen"])
