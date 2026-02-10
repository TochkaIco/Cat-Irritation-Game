# 🐱 Cat Irritation Game
Project Goal: Creating a high-performance, procedurally generated Roguelike using pure Python and PyGame.

---

## 🌟 Key Technical Features
- 🌊 Procedural island generation
Random closed-shape island generation with spline-smoothed coastline using **CubicSpline**, followed by a scanline polygon fill algorithm (NumPy + SciPy)
- 🎥 Smooth camera tracking system
Interpolated camera movement that smoothly follows the player while keeping them centered on screen
- 🧠 DeltaTime-stabilized movement logic
Velocity normalization combined with clamped DeltaTime to maintain consistent movement and physics behavior across varying frame rates.

**This is just the beginning!**

---

## 🚀 How to Run

1. 📦 Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. ▶️ Run the app:

    ```bash
    python CatGame.py
    ```

---

## 📁 Project Structure

```bash
Cat-Irritation-Game/
├── Images/
│   └── Roman-Verde.png
│   └── Angry_Slime.png
│   └── Cat_health_bar.png
│   └── Catgirl 15x38.png
│   └── Flowers/
│       └── Flower1.png
│       └── Flower2.png
│   └── Prefabs/
│       └── BlackMarker.png
│       └── BlueMarker.png
│       └── GreenMarker.png
│       └── RedMarker.png
├── dev_setup/
│   └── dev_setup.py
├── .gitignore
├── CatGame.py                # 🧠main script
├── CatGame_BasicLogics.py
├── MapGenerator.py
├── Classes.py
├── PrefabManager.py
├── README.md
├── requirements.txt
```

---

## 📦 requirements.txt

```bash
pygame==2.6.1
scipy==1.17.0
matplotlib==3.10.8
numpy==2.4.1
```



