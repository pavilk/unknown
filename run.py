import sys
from heapq import heappush, heappop

ROOMS_IND = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HALL_STOPS = [0, 1, 3, 5, 7, 9, 10]


def solve(lines: list[str]) -> int:
    saved_states: dict[tuple[tuple[str | None, ...], tuple[tuple[str | None, ...], ...]], int] = {}
    start_rooms = parse(lines)
    depth = len(start_rooms[0])
    hall = [None] * 11
    counter = 0
    start_state = (tuple(hall), tuple(tuple(room) for room in start_rooms))
    heap = []
    heappush(heap, (0, counter, start_state))
    right_state = tuple(tuple([symb] * depth) for symb in 'ABCD')

    while heap:
        cost, _, state = heappop(heap)
        if state in saved_states and saved_states[state] <= cost:
            continue
        saved_states[state] = cost
        if right_state == state[1]:
            return cost
        for new_state, new_cost in new_moves(state):
            counter += 1
            heappush(heap, (cost + new_cost, counter, new_state))
    return 0


def create_new_state(move_type: str, room_num: int, hall_pos_ind: int,
                     hall: tuple[str | None, ...], rooms: tuple[tuple[str, ...], ...]) -> tuple[
        tuple[str | None, ...], tuple[tuple[str, ...], ...]]:
    new_hall = list(hall)
    new_rooms = [list(room) for room in rooms]

    if move_type == "hall_move":
        symb = new_hall[hall_pos_ind]
        new_hall[hall_pos_ind] = None
        depth = deepest_ind(new_rooms[room_num])
        new_rooms[room_num][depth] = symb

    else:  # move_type == "room move"
        room = new_rooms[room_num]
        symb = None
        for i, element in enumerate(room):
            if element is not None:
                symb = element
                room[i] = None
                break
        new_rooms[room_num] = tuple(room)
        new_hall[hall_pos_ind] = symb

    return tuple(new_hall), tuple(tuple(room) for room in new_rooms)


def new_moves(state: tuple[tuple[str | None, ...], tuple[tuple[str, ...], ...]]) -> list[
        tuple[tuple[tuple[str | None, ...], tuple[tuple[str, ...], ...]], int]]:
    moves = []
    hall, rooms = state

    # может ли кто-нибудь вернуться в комнату из хола
    for pos, symb in enumerate(hall):
        if symb is None:
            continue
        room = rooms['ABCD'.index(symb)]
        room_ind = ROOMS_IND[symb]
        if can_go_home(pos, room_ind, hall, room):
            room_num = "ABCD".index(symb)
            depth = deepest_ind(room)
            steps = abs(pos - room_ind) + (depth + 1)
            cost = steps * COSTS[symb]
            new_state = create_new_state("hall_move", room_num, pos, hall, rooms)
            moves.append((new_state, cost))

    # перебираем все возможные выходы из комнат
    for room_num, room in enumerate(rooms):
        for symb_ind, symb in enumerate(room):
            if symb is None:
                continue
            if all(element == 'ABCD'[room_num] for element in room[symb_ind:]):
                continue
            for hall_pos in HALL_STOPS:
                start_ind = ROOMS_IND['ABCD'[room_num]]
                if not can_move_through_hall(start_ind, hall_pos, hall):
                    continue
                steps = symb_ind + 1 + abs(start_ind - hall_pos)
                cost = steps * COSTS[symb]
                new_state = create_new_state("room move", room_num, hall_pos, hall, rooms)
                moves.append((new_state, cost))
            break
    return moves


def can_go_home(start_ind: int, end_ind: int, hall: tuple[str | None, ...], room: tuple[str, ...]) -> bool:
    if not can_move_through_hall(start_ind, end_ind, hall):
        return False
    symb = hall[start_ind]
    return all(element == symb or element is None for element in room)


def deepest_ind(room: list[str] | tuple[str, ...]) -> int:
    for i in range(len(room) - 1, -1, -1):
        if room[i] is None:
            return i
    return -1


def can_move_through_hall(start_ind: int, end_ind: int, hall: tuple[str | None, ...]) -> bool:
    direction = 1 if start_ind < end_ind else -1
    for pos in range(start_ind + direction, end_ind + direction, direction):
        if hall[pos] is not None:
            return False
    return True


def parse(lines: list[str]) -> list[list[str]]:
    a_room, b_room, c_room, d_room = [], [], [], []
    for line in lines[2:-1]:
        a_room.append(line[3])
        b_room.append(line[5])
        c_room.append(line[7])
        d_room.append(line[9])
    return [a_room, b_room, c_room, d_room]


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
