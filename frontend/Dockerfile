FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies (cached layer)
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Build the SvelteKit app
COPY . .
RUN yarn build

# ── Production image ───────────────────────────────────────────────────────────
FROM node:22-alpine

WORKDIR /app

# adapter-node produces a self-contained build/ directory.
# node_modules are needed at runtime for the server entrypoint.
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

EXPOSE 3000

ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["node", "build"]
