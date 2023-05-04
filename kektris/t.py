GAME_END_ZONE = {(x, y) for x in range(0, 34) for y in [0, 33]} | {(x, y) for x in [0, 33] for y in range(0, 34)}

print(GAME_END_ZONE)