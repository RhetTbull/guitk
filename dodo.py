"""Task list for doit, used to build the project; run with `doit` or `doit list` to see commands"""


def task_update_readme():
    """Update README """
    return {"actions": ["poetry run cog -r README.mdpp", "markdown-pp README.mdpp -o README.md"]}


# def task_test():
#     """Run tests"""
#     return {"actions": ["poetry run pytest"]}


def task_clean_build_files():
    """Clean out old build files"""
    return {
        "actions": ["rm -rf dist/", "rm -rf build/"],
    }


def task_build():
    """Build python project"""
    return {"actions": ["poetry build"]}
