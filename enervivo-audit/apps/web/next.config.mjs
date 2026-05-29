/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Note : output:"standalone" abandonné — instable avec pnpm monorepo (symlinks
  // cassés ou node_modules absents du standalone). Runtime utilise `next start`
  // avec un node_modules complet (cf apps/web/Dockerfile).
  transpilePackages: ["@enervivo/shared-types"],
  // Server Actions derrière nginx : autorise localhost:11118 (origine cliente)
  // et localhost (header X-Forwarded-Host par défaut). Configurable via env.
  experimental: {
    typedRoutes: false,
    serverActions: {
      allowedOrigins: ["localhost:11118", "localhost"],
    },
  },
  // ESLint v9 incompatible avec next lint legacy options — on désactive au build.
  // Le lint reste utilisable manuellement via `pnpm lint` une fois corrigé.
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Nginx (localhost:11118) gère le routing /api → api:8000 et / → web:3000.
  async rewrites() {
    return [];
  },
};

export default nextConfig;
