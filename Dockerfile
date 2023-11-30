# Stage 1: Build the application
FROM ruby:3.2.2 AS builder

WORKDIR /app

# Copy the Gemfile and Gemfile.lock to the container
COPY Gemfile Gemfile.lock ./

# Install dependencies using Bundler
RUN gem install bundler
RUN bundle install --binstubs

# Install MySQL and Redis clients
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libhiredis-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . .

# Stage 2: Final image with MySQL and Redis support
FROM ruby:3.2.2

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/bundle/ /usr/local/bundle/
COPY --from=builder /app /app

# Expose the port that your Rails app will run on
EXPOSE 3000

# Start the Rails application
CMD ["bin/rails", "server", "-b", "0.0.0.0"]
