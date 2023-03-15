FROM duffn/python-poetry:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the app
ENTRYPOINT ["/entrypoint.sh"]