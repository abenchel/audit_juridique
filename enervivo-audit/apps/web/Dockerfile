# EnerVivo Audit Web — Next.js 14 (monorepo pnpm)
# BuildKit cache: lock-first strategy
# On n'utilise PAS output:"standalone" (instable avec pnpm workspaces).

FROM node:20-alpine AS base
RUN corepack enable && corepack prepare pnpm@9.12.0 --activate

# --- 🎯 Layer 1: lock files seulement ---
FROM base AS lockfiles
WORKDIR /repo
COPY pnpm-lock.yaml* package.json pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/
COPY packages/shared-types/package.json ./packages/shared-types/
RUN echo "node-linker=hoisted" > /repo/.npmrc

# --- 🎯 Layer 2: install deps ---
FROM base AS deps
WORKDIR /repo
RUN echo "node-linker=hoisted" > /repo/.npmrc
COPY --from=lockfiles /repo .
# Fallback: si pnpm-lock.yaml manquant, on génère et on installe
RUN if [ ! -f pnpm-lock.yaml ]; then pnpm install --no-frozen-lockfile; else pnpm install --frozen-lockfile; fi

# --- 🎯 Layer 3: build ---
FROM base AS builder
WORKDIR /repo
COPY --from=deps /repo/.npmrc ./.npmrc
COPY --from=deps /repo/node_modules ./node_modules
COPY pnpm-workspace.yaml package.json ./
COPY apps/web ./apps/web
COPY packages/shared-types ./packages/shared-types
ENV NEXT_TELEMETRY_DISABLED=1
RUN cd apps/web && pnpm build

# --- 🎯 Layer 4: runtime slim ---
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

# Copy ALL node_modules first (needed for next binary)
COPY --from=builder --chown=nextjs:nodejs /repo/node_modules ./node_modules
# Then copy app-specific files
COPY --from=builder --chown=nextjs:nodejs /repo/apps/web/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /repo/apps/web/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /repo/apps/web/next.config.mjs ./next.config.mjs

USER nextjs
EXPOSE 3000
CMD ["node_modules/.bin/next", "start", "-p", "3000"]
