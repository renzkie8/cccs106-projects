# ContactBookApp app
## Project Structure

contact_book_app/
├── src/
│ ├── init.py # Makes src a Python package
│ ├── main.py # Entry point: UI and event handling
│ ├── app_logic.py # Core logic: add, edit, delete, search contacts
│ └── database.py # SQLite database initialization and queries
├── requirements.txt # Project dependencies
└── README.md # Project documentation

Notes

Keep all .py files inside the src/ folder.

Use python -m src.main to run locally — this ensures Python treats src as a package.

The sqlite3 module is included with Python.

Any additional packages your app uses should be listed in requirements.txt.

## Run the app

### uv

Run as a desktop app:

```
uv run flet run main.py
```
```
python main.py ## Run the app with python
```
Run as a web app: 

```
uv run flet run  main.py --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```
or
```
flet build apk --module-name src.main
```

To build an APK, you need:

Flet installed (pip install flet)

Android SDK installed and ANDROID_HOME environment variable set

Developer Mode enabled on Windows

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).