# Password Manager (Python)

Simple desktop password manager written in Python with a Tkinter GUI. This is a learning project and is NOT production-ready. The app demonstrates:

- Tkinter GUI
- Random password generation
- Clipboard integration with `pyperclip`
- Local encrypted storage using `cryptography` (Fernet + PBKDF2 key derivation)

Security notes
- Passwords are encrypted on disk with a key derived from a master password using PBKDF2-HMAC-SHA256.
- The project is intended for learning. Review and strengthen before any real use.

How to run
1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run:

```powershell
python main.py
```

Testing

Run tests with pytest:

```powershell
pip install pytest
pytest -q
```
