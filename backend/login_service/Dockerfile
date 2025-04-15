FROM node:18-alpine

WORKDIR /app

# Copy only necessary files for dependency installation
COPY package*.json  ./
RUN npm install

# COPY . /login_service/

# Copy the rest of the application code
COPY . .

# Expose the service port
EXPOSE 5001

# Start the application
CMD ["node", "models/userModel.js"]


