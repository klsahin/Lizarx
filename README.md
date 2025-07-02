# Lizarx Game

A lizard endless runner game where you collect fruit, avoid bombs, and rack up your score! Supports both keyboard and Arduino-based controls.

## Controls

- **Keyboard** (default):
  - Far Left: `A` or `H`
  - Top Left: `W` or `U`
  - Top Right: `S` or `I`
  - Far Right: `D` or `L`

Install dependencies:

```bash
pip install pygame pyserial
```

or install pygame and pyserial seperatly

## Running the Game

```bash
python main.py
```

- To use Arduino, set `arduino = True` at the top of `main.py` and ensure your Arduino is connected and sending serial data.

## Credits

Made by Karla Sahin and Dingning Cao for Jiaji Li and Mingming Li
