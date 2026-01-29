# Use official Node.js image
FROM node:18

# Create app directory
WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy entire project
COPY . .

# Expose app port (change if your app uses different port)
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]

