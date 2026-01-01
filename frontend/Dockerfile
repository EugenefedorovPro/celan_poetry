FROM node:24.12.0-trixie

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# run manually in /frontend folder
# npm create vite@latest . -- --template react-ts

