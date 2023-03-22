FROM duffn/python-poetry:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY pyproject.toml poetry.lock ./
# Poetry is installed with `pip`, so active our virtual environmennt and install projects dependecies there, so they don't conflict with poetry's dependencies.
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

# Install the app
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install

# Run the app
CMD ["/entrypoint.sh"]