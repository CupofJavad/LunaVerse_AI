FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 4173

# Run preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]

