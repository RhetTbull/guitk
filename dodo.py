"""Task list for doit, used to build the project; run with `doit` or `doit list` to see commands"""

DOIT_CONFIG = {
    "default_tasks": ["update_readme", "build_docs", "clean_build_files", "build"]
}


def task_update_readme():
    """Update README"""
    return {
        "actions": [
            "poetry run cog -r README.mdpp",
            "markdown-pp README.mdpp -o README.md",
        ]
    }


def task_build_docs():
    """Build documentation"""
    return {
        "actions": [
            "poetry run cog -r docs/tutorial.mdpp",
            "markdown-pp docs/tutorial.mdpp -o docs/tutorial.md",
            "poetry run mkdocs build",
        ]
    }


def task_test():
    """Run tests"""
    return {"actions": ["poetry run pytest"]}


def task_clean_build_files():
    """Clean out old build files"""
    return {
        "actions": ["rm -rf dist/", "rm -rf build/"],
    }


def task_build():
    """Build python project"""
    return {"actions": ["poetry build"]}
