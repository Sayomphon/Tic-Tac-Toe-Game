# Tic‑Tac‑Toe Game 🟦🟧  
_A FastAPI + Vanilla‑JS implementation with an AI opponent and persistent score tracking_

---

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Quick Start](#quick-start)  
4. [Detailed Setup (Dev Environment)](#detailed-setup-dev-environment)  
5. [Project Layout](#project-layout)  
6. [Gameplay & Scoring Rules](#gameplay--scoring-rules)  
7. [API Reference](#api-reference)  
8. [AI Bot Strategy](#ai-bot-strategy)  
9. [Extending / Deploying](#extending--deploying)  
10. [License](#license)

---

## Overview
This repository contains a full‑stack **Tic‑Tac‑Toe (OX)** web application:

* **Backend:** Python 3, FastAPI, SQLite  
* **Frontend:** HTML + CSS (responsive) and Vanilla JavaScript  
* **AI Bot:** Minimax algorithm with three difficulty levels (easy, medium, hard)  
* **Persistence:** Scores are stored in a local SQLite DB (or an in‑memory fallback when DB is disabled)  

The project was created as a technical assignment that required:

* A playable _player vs AI_ Tic‑Tac‑Toe game  
* An AI that responds “reasonably” (not random on hard mode)  
* A scoring system with **bonus points** for a 3‑win streak  
* A web interface to **view / reset** all player scores  

---

## Features
| Category            | Details |
|---------------------|---------|
| **Game Modes**      | Player (X) vs. AI Bot (O) |
| **Difficulty**      | `Easy` (random), `Medium` (50 % random, 50 % Minimax), `Hard` (pure Minimax) |
| **Scoring**         | +1 win, −1 loss, +0 tie, **+1 extra** after _3 consecutive wins_ |
| **Tech Stack**      | FastAPI, Uvicorn (ASGI), SQLite (ORM‑free), Vanilla JS, CSS‑only theming |
| **Live Reload**     | `uvicorn --reload` watches source files |
| **Zero JS Build**   | No Node, Webpack or npm required; works in any modern browser |
| **Dev Friendly**    | Runs out‑of‑the‑box in VS Code with a Python virtual‑env |

---

## Quick Start
> **Prerequisites**  
> * Git  
> * Python 3.8+ (tested with 3.11)  
> * _Optional:_ Visual Studio Code for an IDE‑like experience  

```bash
# 1 . Clone
git clone https://github.com/<your‑user>/tic-tac-toe-game.git
cd tic-tac-toe-game

# 2 . Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3 . Install backend dependencies
pip install -r requirements.txt

# 4 . Run the server (auto‑reload enabled)
uvicorn app:app --reload

# 5 . Play!
# Open your browser at http://127.0.0.1:8000