
# 🌌 Cosmos Collections Dept. (DCC) - Space Logistics System

<div align="center">

![Python](https://img.shields.io/badge/python-3.12%2B-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Functional Programming](https://img.shields.io/badge/Paradigm-Functional-orange?style=for-the-badge)

**A high-efficiency space resource management platform built with Python and PyQt5.**
*Developed as project for Advanced Programming at Pontificia Universidad Católica de Chile.*

</div>

---

## 📖 Overview

**Cosmos Collections Dept. (DCC)** is a desktop application designed to manage and visualize complex logistical data for interstellar mining operations.

The project was engineered to solve a specific challenge: **processing massive datasets (Big Data simulation) with limited memory resources.** Unlike traditional approaches that load entire files into RAM, this system utilizes **Python Generators** and **Functional Programming** paradigms to stream data lazily, allowing it to query, filter, and analyze Gigabytes of CSV data in real-time without performance degradation.

### The Scenario
The software simulates a competitive mining environment where the user manages expeditions, ship fleets, and mineral extraction across a generated galaxy, optimizing routes and loads against the rival corporation "Imperio Minero Celestial".

## ⚙️ Key Technical Features

### 1. Memory-Efficient Backend (Functional Pipeline)
* **Generator-Based Architecture:** All data ingestion uses `yield` to process CSV rows one by one.
* **Functional Queries:** Implementation of complex filtering logic using `map`, `filter`, `reduce`, and `lambda` functions instead of traditional loops.
* **Scalability:** Capable of handling `S`, `M`, and `L` (Large) datasets seamlessly.

### 2. Interactive Frontend (PyQt5)
* **Modular GUI Design:** A three-window architecture (Welcome, Query Dashboard, Star Map) built entirely with code (no drag-and-drop designers).
* **Event-Driven Communication:** Decoupled frontend and backend using PyQt5 Signals and Slots to prevent UI freezing during heavy data processing.
* **Custom Visualization:** A dynamic "Star Map" that renders planets based on coordinate systems and relative radii scaling.

### 3. Complex Data Relationships
The system models and cross-references 8 distinct entities:
* `Astronauts`, `Spaceships`, `Crews`
* `Planets`, `Minerals`, `PlanetResources`
* `Missions`, `MissionRequirements`

## 🛠️ Project Architecture

The project follows a strict separation of concerns (MVC pattern adaptation):

```text
/
├── main.py                             # Application Entry Point & Controller
├── parametros.py                       # Configuration constants (Map dimensions, scaling)
├── .gitignore                          # Git configuration
├── backend/                            # Business Logic & Data Processing
│   ├── cargar_datos.py                 # CSV to Generator parsers
│   ├── consultas.py                    # Main query interface
│   ├── logica_ventana_principal.py
│   └── consultas_generadores/          # Modularized query logic
│       ├── consultas_un_gen.py         # Single-source queries
│       ├── consultas_dos_gen.py        # Data joining (2 sources)
│       └── consultas_tres_gen.py       # Complex aggregation (3 sources)
└── frontend/                           # User Interface
    ├── sprites/                        # Assets for planetary visualization
    └── ventanas/                       # PyQt5 Window Definitions
        ├── ventana_inicio.py
        ├── ventana_principal.py
        └── ventana_mapa.py
````

## 🚀 Installation & Usage

### Prerequisites

  * Python 3.12 or higher.
  * `PyQt5` library.

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/dianAnton/Cosmos-Collections-Dept.-DCC-Space-Logistics-System.git
    cd Cosmos-Collections-Dept.-DCC-Space-Logistics-System
    ```

2.  **Install dependencies:**

    ```bash
    pip install PyQt5
    ```

3.  **Data Configuration:**

    > **Note:** Due to copyright and size restrictions, the raw CSV datasets (`data/`) are not included in this repository.

    To run the program, create a folder named `T3` (or adjust the path in the GUI) and populate it with CSV files following the schema defined in `backend/cargar_datos.py`.

4.  **Run the application:**

    ```bash
    python main.py
    ```

## 📸 Visual Preview

*(Placeholder for your Screenshots - Highly Recommended)*

| **Dashboard** | **Star Map Visualization** |
|:---:|:---:|
| *Query interface for filtering ships and missions* | *Coordinate-based rendering of planetary systems* |
|  |  |
