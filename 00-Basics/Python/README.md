# CS50 Python Course – Progress Tracker 🐍

This directory holds **all code, tests, and notes** from Harvard’s  
[CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python).

| Folder                  | CS50 Week | Key topics                              | Status | Tests |
|-------------------------|-----------|-----------------------------------------|--------|-------|
| 00-intro                | Week 0    | variables, input / output               | ⏳     | –     |
| 01-conditionals         | Week 1    | `if / elif / else`, data-types          | ⏳     | –     |
| 02-loops-collections    | Week 2    | `for / while`, lists, dicts             | ⏳     | –     |
| 03-functions            | Week 3    | functions, module import                | ⏳     | –     |
| 04-testing-libraries    | Week 4    | `pytest`, third-party libraries         | ⏳     | –     |
| 05-file-io              | Week 5    | files, CSV, JSON                        | ⏳     | –     |
| 06-oop                  | Week 6    | classes, objects                        | ⏳     | –     |
| final-project           | Final     | personal CLI / mini-API                 | ⏳     | –     |

Legend ⏳ in progress | ✅ done | 🟥 revisit

---

## Environment setup

```bash
# run inside 00-basics/Python
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt   # pytest, black, etc.
```

*.gitignore* already excludes **.venv/**.

Before every commit:

```bash
black .
pytest           # optional – run tests if present
```

---

## Directory layout

```text
00-basics/Python/
├── 00-intro/
│   ├── hello.py
│   ├── mario.py
│   └── README.md
├── 01-conditionals/
│   ├── coke.py
│   ├── deep_thought.py
│   └── README.md
├── 02-loops-collections/
│   └── ...
├── 03-functions/
│   └── ...
├── 04-testing-libraries/
│   └── ...
├── 05-file-io/
│   └── ...
├── 06-oop/
│   └── ...
└── final-project/
    ├── app.py
    ├── requirements.txt
    └── demo.gif
```

Each sub-folder contains  
1. **README.md** – short problem description, run instructions, reflections.  
2. Source code for the problem-set.  
3. `test_*.py` files (when applicable).
