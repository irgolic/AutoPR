FROM duffn/python-poetry:3.9-bullseye

# Install git
RUN echo "deb http://deb.debian.org/debian bullseye-backports main" > /etc/apt/sources.list.d/backports.list && \
    apt-get update && \
    apt-get install -y -t bullseye-backports git

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