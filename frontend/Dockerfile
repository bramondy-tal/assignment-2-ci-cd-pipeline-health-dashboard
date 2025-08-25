# Use a compatible Node.js version for Vite
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Copy the built application files
COPY dist /app/dist

# Expose the port and run the preview server
EXPOSE 5173
# Use npm run dev to start the development server
CMD ["npm", "run", "dev"]
