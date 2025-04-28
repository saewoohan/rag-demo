FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .
RUN yarn build

# Make start script executable
RUN chmod +x start.sh

CMD ["./start.sh"] 