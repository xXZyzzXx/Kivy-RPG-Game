import numpy as np

h = 10
w = 10

A = [[col for col in range(w + 1)] for row in range(h)]
map_index = np.array(A)
#print(map_index)

passability = [[1 for j in range(w + 1)] for i in range(h)]
pm = np.array(passability)
#print(pm)

movement_map = [[-1 for k in range(w + 1)] for g in range(h)]
rm = movement_map  #np.array(movement_map)


def generate_move_map(x, y, moves=3):
    pm_width = 10
    pm_height = 10
    if rm[x][y] < moves:
        rm[x][y] = moves
        for _x in range(-1, 1):  # Проходит циклом вокруг центра
            for _y in range(-1, 1):
                print(_x, _y)
                if _x == 0 and _y == 0:
                    nX = _x + x
                    nY = _y + y
                    print(f'nx,ny={nX, nY}, | _y, _x{_y, _x} | method {x, y, moves}')
                    if 0 <= nX < pm_width and 0 <= nY < pm_height:
                        if abs(_x) + abs(_y) == 2:
                            move_weight = 1.5
                        else:
                            move_weight = 1
                        t = moves - move_weight  # * pm[nX, nY]
                        print(f'T={t}')
                        if t >= 0:
                            print(f'generating new coords: {nX, nY, t}')
                            generate_move_map(nX, nY, t)
                _y += 1
            _x += 1

generate_move_map(5, 5)
for f in rm:
   print(f)
'''
void GenMoveMap(int x, int y, double _points)
            {
                if (rm[x, y].Range < _points)
                {
                    rm[x, y].Range = _points;
                    for (int _x = -1; _x <= 1; _x++)
                        for (int _y = -1; _y <= 1; _y++)
                            if (!(_x == 0 && _y == 0))
                            {
                                int nX = _x + x;
                                int nY = _y + y;
                                if (nX >= 0 && nY >= 0 && nX < pm.Width && nY < pm.Hight)
                                {
                                    double t =
                                        _points - ((Math.Abs(_x) + Math.Abs(_y) == 2 ? 1.5 : 1)
                                        * pm[nX, nY].Penalty);
                                    if (t >= 0)
                                        GenMoveMap(nX, nY, t);
                                }
                            }
                }'''
