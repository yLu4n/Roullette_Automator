# A ordem dos números na "Race" (pista) da roleta
RACE_TRACK = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 
    23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 
    35, 3, 26
]

STRATEGY_MAP = {
    1: [{'numero': 1, 'vizinhos': 3}, {'numero': 3, 'vizinhos': 3}, {'numero': 36, 'vizinhos': 3}],
    2: [{'numero': 2, 'vizinhos': 3}, {'numero': 22, 'vizinhos': 3}, {'numero': 5, 'vizinhos': 3}],
    3: [{'numero': 26, 'vizinhos': 3}, {'numero': 33, 'vizinhos': 3}],
    5: [{'numero': 5, 'vizinhos': 3}, {'numero': 22, 'vizinhos': 3}, {'numero': 25, 'vizinhos': 3}],
    7: [{'numero': 7, 'vizinhos': 3}, {'numero': 27, 'vizinhos': 3}, {'numero': 19, 'vizinhos': 3}],
    8: [{'numero': 30, 'vizinhos': 3}],
    9: [{'numero': 9, 'vizinhos': 3}, {'numero': 27, 'vizinhos': 3}, {'numero': 19, 'vizinhos': 3}],
    11: [{'numero': 30, 'vizinhos': 3}],
    12: [{'numero': 12, 'vizinhos': 3}, {'numero': 21, 'vizinhos': 3}, {'numero': 16, 'vizinhos': 3}],
    13: [{'numero': 13, 'vizinhos': 3}, {'numero': 0, 'vizinhos': 3}, {'numero': 33, 'vizinhos': 3}],
    14: [{'numero': 14, 'vizinhos': 3}, {'numero': 34, 'vizinhos': 3}],
    15: [{'numero': 26, 'vizinhos': 3}, {'numero': 33, 'vizinhos': 3}],
    16: [{'numero': 16, 'vizinhos': 3}, {'numero': 21, 'vizinhos': 3}, {'numero': 12, 'vizinhos': 3}],
    17: [{'numero': 17, 'vizinhos': 3}, {'numero': 20, 'vizinhos': 3}],
    19: [{'numero': 19, 'vizinhos': 3}, {'numero': 27, 'vizinhos': 3}, {'numero': 9, 'vizinhos': 3}],
    20: [{'numero': 20, 'vizinhos': 3}, {'numero': 17, 'vizinhos': 3}],
    21: [{'numero': 21, 'vizinhos': 3}, {'numero': 16, 'vizinhos': 3}, {'numero': 12, 'vizinhos': 3}],
    22: [{'numero': 22, 'vizinhos': 3}, {'numero': 25, 'vizinhos': 3}, {'numero': 5, 'vizinhos': 3}],
    25: [{'numero': 25, 'vizinhos': 3}, {'numero': 5, 'vizinhos': 3}, {'numero': 22, 'vizinhos': 3}],
    26: [{'numero': 26, 'vizinhos': 3}, {'numero': 33, 'vizinhos': 3}],
    27: [{'numero': 27, 'vizinhos': 3}, {'numero': 7, 'vizinhos': 3}, {'numero': 19, 'vizinhos': 3}],
    30: [{'numero': 30, 'vizinhos': 3}],
    36: [{'numero': 30, 'vizinhos': 3}],
}