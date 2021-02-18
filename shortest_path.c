#include <stdbool.h>
#include <stdio.h>

#define INFINITY 9999
#define NO_NODES 50
#define START_POS 48
#define END_POS 49
#define NO_ROWS 6
#define NO_COLOUMNS 8


struct coordinate {
    int x;
    int y;
};

int available_path[NO_NODES];

int path_from[NO_NODES];

void dijkstra(int startnode);

bool is_connected(int pos0, int pos1)
{
    if(pos0 > pos1)
    {
        int temp = pos0;
        pos0 = pos1;
        pos1 = temp;
    }
    int x0 = pos0/8;
    int y0 = pos0%8;

    int x1 = pos1/8;
    int y1 = pos1%8;
    if(pos1 == END_POS)
    {
        if(pos0 == 43)
        {
            return available_path[END_POS]%7 == 0;
        }
        else if(pos0 == 44)
        {
            return available_path[END_POS]%3 == 0;
        }
    }
    else if(pos1 == START_POS)
    {
        if(pos0 == 3)
        {
            return available_path[START_POS]%7 == 0;
        }
        else if(pos0 == 4)
        {
            return available_path[START_POS]%3 == 0;
        }
    }
    else if(x1 == x0 + 1)
    {
        return available_path[pos0]%3 == 0;
    }
    else if(y1 == y0 + 1)
    {
        return available_path[pos0]%2 == 0;
    }
    return false;
}


void initialize_paths() 
{
    for(int i =0; i < NO_NODES; i++)
    {
        available_path[i] = 210;
        if(i/8 == 0)
        {
            available_path[i] /= 5;
        }
        if(i/8 == 5)
        {
            available_path[i] /= 2;
        }
        if(i%8 == 0)
        {
            available_path[i] /= 7;
        }
        if(i%8 == 7)
        {
            available_path[i] /= 3;
        }
    }
    available_path[START_POS] /= 2;
    available_path[END_POS] /= 5;
    available_path[3] /= 3;
    available_path[43] /= 3;
    available_path[4] /= 7;
    available_path[44] /= 7;

    dijkstra(END_POS);
}

void blocked(int pos0, int pos1)
{
    if(pos0 > pos1)
    {
        int temp = pos0;
        pos0 = pos1;
        pos1 = temp;
    }
    int x0 = pos0/8;
    int y0 = pos0%8;

    int x1 = pos1/8;
    int y1 = pos1%8;

    if(pos1 == END_POS)
    {
        if(pos0 == 43)
        {
            available_path[END_POS] /= 7;
        }
        else if(pos0 == 44)
        {
            available_path[END_POS] /= 3;
        }
    }
    else if(pos1 == START_POS)
    {
        if(pos0 == 3)
        {
            available_path[START_POS] /= 7;
        }
        else if(pos0 == 4)
        {
            available_path[START_POS] /= 3;
        }
    }

    if(x1 == x0 + 1)
    {
        available_path[pos0] /= 2;
        available_path[pos1] /= 5;
    }
    else if(y1 == y0 + 1)
    {
        available_path[pos0] /= 3;
        available_path[pos1] /= 7;
    }
    dijkstra(END_POS);
}

void connected_nodes(int pos, int arr[])
{
    int direction[] = {2, 3, 5, 7};
    int pos_add[] = {8, 1, -8, -1};

    for(int i = 0; i < 4; i++)
    {
        arr[i] = -1;
    }

    if(pos == START_POS)
    {
        if(available_path[pos]%3 == 0)
        {
            arr[1] = 4;
        }
        if(available_path[pos]%7 == 0)
        {
            arr[3] = 3;
        }
    }
    else if(pos == END_POS)
    {
        if(available_path[pos]%3 == 0)
        {
            arr[1] = 44;
        }
        if(available_path[pos]%7 == 0)
        {
            arr[3] = 43;
        }
    }
    else
    {
        for(int i = 0; i < 4; i++)
        {
            if(available_path[pos] % direction[i] == 0)
            {
                arr[i] = pos + pos_add[i];
            }
        }
    }

    if(pos == 3)
    {
        if(available_path[START_POS]%7 == 0)
        {
            arr[1] = START_POS;
        }
    }
    else if(pos == 4)
    {
        if(available_path[START_POS]%3 == 0)
        {
            arr[3] = START_POS;
        }
    }

    if(pos == 43)
    {
        if(available_path[END_POS]%7 == 0)
        {
            arr[1] = END_POS;
        }
    }
    else if(pos == 44)
    {
        if(available_path[END_POS]%3 == 0)
        {
            arr[3] = END_POS;
        }
    }
}

void dijkstra(int startnode)
{
 
    int distance[NO_NODES], *pred = path_from;
    int count,mindistance,nextnode,i,j;
    int direction[] = {2, 3, 5, 7};
    int connected[4];
    bool visited[NO_NODES];

    for(i = 0; i < NO_NODES; i++)
    {
        
        distance[i] = INFINITY;
        pred[i] = startnode;
        visited[i] = false;

    }

    connected_nodes(startnode, connected);

    for(i = 0; i < 4; i++)
    {
        if(connected[i] != -1)
        {
            distance[connected[i]] = 1;
        }
    }
    
    pred[startnode] = startnode;
    distance[startnode] = 0;
    visited[startnode] = true;
    count = 1;
    
    while(count < NO_NODES - 1)
    {
        mindistance = INFINITY;
        
        for(i = 0; i < NO_NODES; i++)
        {

            if(distance[i] < mindistance && !visited[i])
            {
                mindistance = distance[i];
                nextnode = i;
            }
        }        

        visited[nextnode] = true;
        connected_nodes(nextnode, connected);

        for(i = 0; i < 4; i++)
        {
            if(connected[i] != -1 && !visited[connected[i]])
            {
                if(mindistance + 1 < distance[connected[i]])
                {
                    distance[connected[i]] = mindistance + 1; 
                    pred[connected[i]] = nextnode;
                }
            }
        }
        count++;
    }
}

int shortest_path(int pos)
{
    return path_from[pos];
}

int main()
{   
    initialize_paths();
    blocked(3, 11);
    blocked(4, 12);

    for(int i = NO_ROWS-1; i > -1; i--)
    {
        for(int j = 0; j < NO_COLOUMNS; j++)
        {
            int pos = i*NO_COLOUMNS + j;
            printf("%d[%d] ", pos, path_from[pos]);
        }
        printf("\n");
    }
}