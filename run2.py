import copy
import sys
from collections import deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    g = {}
    outs = {}
    outs_count = create_graph(edges, g, outs)
    for keys in g.keys():
        g[keys][0].sort()
        g[keys][1].sort()

    result = []
    que = deque()
    que.append(['a'])
    start_lvl = 'a'
    end_lvl = g['a'][1][-1]
    outs_at_lvl = list()
    my_turn = True
    visited = set()
    ways = list()
    while que:
        point = que.popleft()
        if point[-1] in visited:
            continue
        ways.append(point)
        visited.add(point[-1])

        for out in g[point[-1]][0]:
            outs_at_lvl.append((out, point[-1]))

        for el in g[point[-1]][1]:
            if el in visited:
                continue
            new_way = copy.deepcopy(point)
            new_way.append(el)
            que.append(new_way)

        if point[-1] == end_lvl:
            if outs_at_lvl:
                outs_at_lvl.sort()
                min_out = outs_at_lvl[0][0]
                close_outs = [x for x in outs_at_lvl if min_out in x]
                close_outs.sort()
                if my_turn:
                    ways.sort()
                    for chose_out in close_outs:
                        for el in ways:
                            if el[-1] == chose_out[1]:
                                closed_out = chose_out
                                break
                        else:
                            continue
                        break
                    result.append(closed_out)
                    outs_count -= 1
                    ind = g[closed_out[1]][0].index(closed_out[0])
                    g[closed_out[1]][0].pop(ind)
                    que = deque()
                    que.append([start_lvl])
                    my_turn = False
                else:
                    monstr_move = 'z'
                    ways.sort()
                    for el in ways:
                        for chose_out in close_outs:
                            if el[-1] == chose_out[1]:
                                monstr_move = el[1]
                                break
                        else:
                            continue
                        break
                    que = deque()
                    que.append([monstr_move])
                    start_lvl = monstr_move
                    my_turn = True
                outs_at_lvl = list()
                first = que.popleft()
                visited = set()
                ways = list()
                end_lvl = g[first[0]][1][-1]
                que.append(first)
            else:
                for el in reversed(g[point[-1]][1]):
                    if el not in visited:
                        end_lvl = el
                        break

    return ["-".join(x) for x in result]


def create_graph(edges, g, outs):
    outs_count = 0
    for t in edges:
        if t[0].isupper():
            outs_count += 1
            add_edge(g, (t[1], t[0]))
            if t[0] in outs.keys():
                outs[t[0]].append(t[1])
            else:
                outs[t[0]] = list(t[1])
        else:
            add_edge(g, (t[0], t[1]))
            if t[1].islower():
                add_edge(g, (t[1], t[0]))
            else:
                outs_count += 1
                if t[1] in outs.keys():
                    outs[t[1]].append(t[0])
                else:
                    outs[t[1]] = list(t[0])
    return outs_count


def add_edge(d: dict, edge: tuple[str, str]):
    key, item = edge[0], edge[1]
    if key in d.keys():
        if item.isupper():
            d[key][0].append(item)
        else:
            d[key][1].append(item)
    else:
        if item.isupper():
            d[key] = [[item], []]
        else:
            d[key] = [[], [item]]


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
