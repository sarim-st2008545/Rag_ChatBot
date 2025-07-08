# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files first for caching
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY frontend/ .

# Build the app
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]