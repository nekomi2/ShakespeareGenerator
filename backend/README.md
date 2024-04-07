# Installation

```
python -m venv shakespeare
source shakespeare/bin/activate  # On Windows use `shakespeare\Scripts\activate`
pip install fastapi uvicorn transformers
```

# Run the server

```
uvicorn main:app --reload
```
