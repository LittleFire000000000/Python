#!/usr/bin/python3

def reroute(i: int) -> str:
    if i == 0: return "Rock"
    if i == 1: return "Paper"
    if i == 2: return "Scissors"
    return

def beats(x: int, y: int) -> bool:
    if x == 0: # Rock
        if y == 0: return False # draws to Rock
        if y == 1: return False # loses to Paper
        if y == 2: return True  # wins  to Scissors
    if x == 1: # Paper
        if y == 0: return True  # wins  to Rock
        if y == 1: return False # draws to Paper
        if y == 2: return False # loses to Scissors
    if x == 2: # Scissors
        if y == 0: return False # loses to Rock
        if y == 1: return True  # wins  to Paper
        if y == 2: return False # draws to Scissors
    return

def beat(x: int, y: int) -> bool:
    return (x + 2) % 3 == y

print(not any((beat(a, b) ^ beats(a, b)) for a in (0, 1, 2) for b in (0, 1, 2)),

winners: [int] = [0, 0, 0]

for a in (0, 1, 2):
    for b in (0, 1, 2):
        c: bool = beat(a, b)
        print(reroute(a), ('beats' if c else 'loses'), reroute(b))
        if c: winners[a] += 1

print("\nWins",
      f"Rock    {winners[0]}",
      f"Paper   {winners[1]}",
      f"Scissors {winners[2]}",
      sep='\n')
