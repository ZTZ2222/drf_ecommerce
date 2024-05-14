FROM python:3.10-slim
WORKDIR /project

# Set environment variables for Python and unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry

# Copy only the dependency files for faster builds
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
	&& poetry install --no-root --no-interaction --no-ansi

# Install netcat-traditional instead of netcat
RUN apt-get update && apt-get install -y netcat-traditional

RUN poetry add gunicorn

# Copy the rest of your application code into the container
COPY . .

# Entrypoint
ENTRYPOINT [ "sh", "entrypoint.sh" ]