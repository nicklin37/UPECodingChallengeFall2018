#NAME: Nicholas Lin
#UPE Fall Induction Coding Challenge 2018

import requests
import json

def main():
    #Get the token
    UID = "uid=204984806"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    r = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session", data=UID, headers=headers)
    token = r.json()["token"]

    url="http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token
    
    for p in range(5):
        #request a maze
        r = requests.get(url)
        
        #extract the boundaries of the maze
        maze_size = r.json()["maze_size"]
        x_bound = maze_size[0]
        y_bound = maze_size[1]
        
        #extract the starting position
        curr_loc = r.json()["current_location"]
        x = curr_loc[0]
        y = curr_loc[1]

        #initialize our maze to keep track of where we are
        maze = []
        for i in range(y_bound):
            row = []
            for j in range(x_bound):
                row.append('.')
            maze.append(row)

        #just to see what maze we're on
        print(r.text)

        solveMaze(maze, x, y, x_bound, y_bound, url,"")

#A recursive, depth-first search solution to the maze
def solveMaze(maze, x, y, x_bound, y_bound, url, reverse):
    #mark the spot we've already looked at
    maze[y][x] = 'p'

    #move up
    if y > 0:
        if maze[y-1][x] == '.':
            u = requests.post(url, data={"action":"UP"})
            ur = u.json()["result"]
            if ur == "SUCCESS":
                if solveMaze(maze, x, y-1, x_bound, y_bound, url, "DOWN"):
                    return True
            if ur == "WALL" or ur == "OUT_OF_BOUNDS":
                maze[y-1][x] = '*'
            if ur == "END":
                return True

    #move right
    if x < x_bound-1:
        if maze[y][x+1] == '.':
            r = requests.post(url, data={"action":"RIGHT"})
            rr = r.json()["result"]
            if rr == "SUCCESS":
                if solveMaze(maze, x+1, y, x_bound, y_bound, url, "LEFT"):
                    return True
            if rr == "WALL" or rr == "OUT_OF_BOUNDS":
                maze[y][x+1] = '*'
            if rr == "END":
                return True

    #move down
    if y < y_bound-1:
        if maze[y+1][x] == '.':
            d = requests.post(url, data={"action":"DOWN"})
            dr = d.json()["result"]
            if dr == "SUCCESS":
                if solveMaze(maze, x, y+1, x_bound, y_bound, url, "UP"):
                    return True
            if dr == "WALL" or dr == "OUT_OF_BOUNDS":
                maze[y+1][x] = '*'
            if dr == "END":
                return True
    
    #move left
    if x > 0:
        if maze[y][x-1] == '.':
            l = requests.post(url, data={"action":"LEFT"})
            lr = l.json()["result"]
            if lr == "SUCCESS":
                if solveMaze(maze, x-1, y, x_bound, y_bound, url, "RIGHT"):
                    return True
            if  lr == "WALL" or lr == "OUT_OF_BOUNDS":
                maze[y][x-1] = '*'
            if lr == "END":
                return True

    #if we're stuck then reverse our previous step
    p = requests.post(url, data={"action":reverse})
    return False

if __name__=='__main__':
    main()






