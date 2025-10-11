FROM node:18-slim

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY frontend/ ./

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
