from invoke import task

# run black for code formatting
@task
def format(c):
    c.run("black ./**/*.py")

# run flake8 for linting
@task
def lint(c):
    c.run("flake8 .")
