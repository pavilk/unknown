import copy
import sys
from collections import deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    g = {}
    outs_dict = {}
    total_outs = create_graph(edges, g, outs_dict)
    for keys in g.keys():
        g[keys][0].sort()
        g[keys][1].sort()

    result = []
    que = deque()
    que.append(['a'])
    ways_to_outs = list()
    start_lvl = 'a'
    end_lvl = g['a'][1][-1]
    outs = list()
    my_turn = True
    visited = set()
    ways = list()
    outs_counter = 0
    while total_outs != 0 and que:
        point = que.popleft()
        if point[-1] in visited:
            continue
        ways.append(point)
        visited.add(point[-1])

        for out in g[point[-1]][0]:
            outs_counter += 1
            outs.append((out, point[-1]))
            new_way_to_out = copy.deepcopy(point)
            new_way_to_out.append(out)
            ways_to_outs.append(new_way_to_out)

        for el in g[point[-1]][1]:
            if el in visited:
                continue
            new_way = copy.deepcopy(point)
            new_way.append(el)
            que.append(new_way)

        if outs_counter == total_outs:
            ways_to_outs.sort(key=lambda x: (x[-1], x[:-1]))
            if my_turn:
                for pick_out in ways_to_outs:
                    monstr_pos = pick_out[0]
                    if g[monstr_pos][0] and pick_out[-1] not in g[monstr_pos][0]:
                        continue
                    closed_out = pick_out
                    break
                total_outs -= 1
                result.append(closed_out[-1:-3:-1])
                ind = g[closed_out[-2]][0].index(closed_out[-1])
                g[closed_out[-2]][0].pop(ind)
                que = deque()
                que.append([closed_out[0]])
                my_turn = False
            else:
                ways_to_outs.sort()
                monstr_move = ways_to_outs[0][1]
                que = deque()
                que.append([monstr_move])
                my_turn = True
            outs = list()
            visited = set()
            ways = list()
            ways_to_outs = list()
            outs_counter = 0

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
    # q = "a-b\nb-c\nc-d\nc-e\nA-d\nA-e\nc-f\nc-g\nf-B\ng-B"
    for line in sys.stdin:
    # for line in q.split("\n"):
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
