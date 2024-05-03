cars = [
    {
        "name": "Strip Weathers",
        "color": "44"
    },
    {
        "name": "Chick Hicks",
        "color": "42"
    },
    {
        "name": "Flash McQueen",
        "color": "41"
    },
    {
        "name": "Cal Weathers",
        "color": "46"
    },
    {
        "name": "Bobby Swift",
        "color": "45"
    },
    {
        "name": "Jackson Storm",
        "color": "40"
    },
    {
        "name": "Paul Conrev",
        "color": "47"
    },
    {
        "name": "Cruz Ramirez",
        "color": "43"
    }
]

s = "".join([f"\x1b[{i+2};{0}H\x1b[{car['color']};1m \x1b[{i+2+len(cars)};{0}H\x1b[{car['color']};1m " for i, car in enumerate(cars)])
print(s, end="", flush=True)