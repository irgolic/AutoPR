FROM duffn/python-poetry:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Check if dependencies have changed
COPY poetry.lock pyproject.toml ./

# Change directory to github workspace
WORKDIR /home/github/
RUN poetry install --no-root --only main

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the app
ENTRYPOINT ["/entrypoint.sh"]