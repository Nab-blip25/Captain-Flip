# Captain Flip

A local two-player board game built with Python and Pygame. Student project implementing game logic, a graphical interface, player accounts and persistent statistics (wins / losses / grades). The game supports tile drawing, flipping, placement with gravity, turn management and end-of-game scoring.

---

## Quick demo / preview
- This project runs locally in a Pygame window.  
- There is no hosted demo — run it on your machine following the instructions below.

---

## Key features
- Local player accounts with persistent wins / losses / grades.  
- Two-player local gameplay (human vs human).  
- Deck of 72 double-faced tiles with unique recto/verso pairs.  
- Tile flip mechanic and single flip-per-draw rule.  
- Grid with gravity: tiles drop to the lowest free cell in a column.  
- Simple menu: Connect / Register / Play / Stats / Quit.  
- Player data saved to a file (no database required).

---

## Requirements
- Python 3.8+ recommended  
- Pygame  
- (Optional) pygame_gui if used by the GUI code

Install with pip:
```bash
pip install pygame
# optional
pip install pygame_gui
```

---

## Run locally
1. Clone the repository:
```bash
git clone https://github.com/your-username/Captain-Flip.git
cd Captain-Flip
```
2. Install dependencies:
```bash
pip install -r requirements.txt
# or manually: pip install pygame pygame_gui
```
3. Start the game (replace main.py with the actual entrypoint if different):
```bash
python main.py
```
Notes:
- Ensure the data folder or player file (e.g., `players.json`, `Joueurs.txt` or similar) is present or writable; the program tries to create it on first run.

---

## Implementation notes
- Clicking a column computes placement by scanning the column for the lowest free Case; Case objects track occupancy.  
- The deck (pioche) contains 72 unique double-faced tiles built from 9 characters; drawing removes tiles so pairs are unique.  
- The monkey character uses a "mode_singe" flag: it activates only when a neighboring tile can be flipped; otherwise the player gets a default piece reward.  
- Menu screens are implemented by drawing overlays rather than opening new windows.

---

## Known limitations and important notes
- There is no AI opponent implemented; only local human vs human play is available.  
- Several planned UI features are missing (Help screen, animated coin popups, multiple boards).  
- Some input screens may not support an in-screen Back button reliably.  
- The code was written early in our learning process and may be messy or not fully modularized.  
- IMPORTANT: The repository structure may be incomplete or inconsistent. When we developed this project we did not always use Git; some files may have been lost or misplaced since then. You may need to adjust file paths, recreate missing assets, or restore certain modules for the game to run properly. Treat this repo as an archived student project rather than a polished release.

---

## Language of comments
- All code comments and in-code documentation are in French.

---

## Possible improvements / roadmap
- Implement an AI opponent with difficulty levels.  
- Add a Help screen describing character abilities and rules.  
- Improve persistence format (JSON or SQLite) and add account management (delete, rename).  
- Add more boards and support for more than two players.  
- Refactor classes into separate modules and add unit tests.  
- Add animations and a clickable purse UI for coins.

---

## Contributing
This started as a student project. Contributions are welcome for bug fixes, modularization, UI improvements, and AI development. Please open an issue or a pull request with a clear description of changes.