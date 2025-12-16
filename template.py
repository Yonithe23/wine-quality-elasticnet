from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

PROJECT_NAME = "datascience"

SOURCE_FILES = [
    f"src/{PROJECT_NAME}/__init__.py",
    f"src/{PROJECT_NAME}/components/__init__.py",
    f"src/{PROJECT_NAME}/utils/__init__.py",
    f"src/{PROJECT_NAME}/utils/common.py",
    f"src/{PROJECT_NAME}/config/__init__.py",
    f"src/{PROJECT_NAME}/config/configuration.py",
    f"src/{PROJECT_NAME}/pipeline/__init__.py",
    f"src/{PROJECT_NAME}/entity/__init__.py",
    f"src/{PROJECT_NAME}/entity/config_entity.py",
    f"src/{PROJECT_NAME}/constants/__init__.py",
    "main.py",
    "app.py",
]

# B) Infrastructure / Packaging
INFRA_FILES = [
    "requirements.txt",   # ✅ fixed comma bug (no more requirements.txtDockerfile)
    "Dockerfile",
    "setup.py",
]

# C) Config files
CONFIG_FILES = [
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
]

# D) Other helpful files
OTHER_FILES = [
    ".github/workflows/.gitkeep",
    "research/research.ipynb",
    "templates/index.html",
]

# Final combined list
ALL_FILES = SOURCE_FILES + INFRA_FILES + CONFIG_FILES + OTHER_FILES


def write_minimal_content(path: Path) -> None:
    """
    Write minimal valid content for critical files.
    Non-critical files are created as empty placeholders.

    This function is only called when the file does NOT already exist
    (so it won't overwrite your work).
    """
    if path.name == "Dockerfile":
        path.write_text(
            "FROM python:3.11-slim\n"
            "WORKDIR /app\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n"
            "COPY . .\n"
            'CMD ["python", "app.py"]\n'
        )

    elif path.name == "requirements.txt":
        path.write_text(
            "# Add project dependencies here\n"
            "# Example:\n"
            "# numpy\n"
            "# pandas\n"
        )

    elif path.name == "setup.py":
        path.write_text(
            "from setuptools import setup, find_packages\n\n"
            "setup(\n"
            f'    name="{PROJECT_NAME}",\n'
            "    version='0.0.1',\n"
            "    packages=find_packages(where='src'),\n"
            "    package_dir={'': 'src'},\n"
            ")\n"
        )

    elif path.suffix == ".py":
        # Optional: tiny placeholder for python files (safe + valid)
        if path.name == "app.py":
            path.write_text(
                "def main():\n"
                "    print('App is running...')\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            )
        else:
            path.touch()

    elif path.suffix == ".yaml":
        # Optional: minimal yaml placeholder (valid yaml)
        path.write_text("# YAML config\n")

    elif path.suffix == ".html":
        path.write_text(
            "<!doctype html>\n"
            "<html>\n"
            "<head><meta charset='utf-8'><title>App</title></head>\n"
            "<body><h1>Hello</h1></body>\n"
            "</html>\n"
        )

    else:
        path.touch()



def create_project_structure(files: list[str]) -> None:
    try:   
        for filepath in files:
            path=Path(filepath)

            # NOTE:
            # path.parent = directory of the file
            # parents=True  → create all missing parent folders
            # exist_ok=True → do NOT fail if folder already exists

            # path.parent.mkdir(parents=True, exist_ok=True)
            parent_dir = path.parent
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory: {parent_dir}")
            else:
                parent_dir.mkdir(parents=True, exist_ok=True)

            # Create file only if it doesn't exist
            if not path.exists():
                write_minimal_content(path)
                logging.info(f"Created file: {path}")
            else:
                logging.info(f"{path.name} already exists")
           
    except OSError as e: 
        logging.error(f"File system error occurred: {e}")
        raise
            

if __name__ == "__main__":
    create_project_structure(ALL_FILES)
    logging.info("✅ Project structure created successfully.")
