import os

ALLOWED_EXTENSIONS = {
    '.py', '.ts', '.tsx', '.js', '.jsx',
    '.cpp', '.h', '.c',
    '.md', '.txt', '.yaml', '.yml', '.toml',
    '.json', '.env.example', '.sh'
}

SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv',
    'venv', 'env', 'dist', 'build', '.next'
}

MAX_FILE_SIZE_BYTES = 20_000 


def scan_directory(path: str) -> list[dict]:
    """
    Walk a directory and return a list of files with their content.
    Each item: { path, content, extension }
    """
    results = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)

            try:
                size = os.path.getsize(filepath)
                if size > MAX_FILE_SIZE_BYTES:
                    continue

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().strip()

                if not content:
                    continue

                results.append({
                    'path': filepath,
                    'relative_path': os.path.relpath(filepath, path),
                    'content': content,
                    'extension': ext
                })

            except Exception:
                continue

    return results
