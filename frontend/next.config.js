/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  // Let the backend return its JSON result before the browser’s 75s budget.
  experimental: { proxyTimeout: 65_000 },
  async rewrites() {
    const backendUrl = (process.env.BACKEND_URL || "http://localhost:8000").replace(/\/$/, "");
    return [{ source: "/api/:path*", destination: `${backendUrl}/api/:path*` }];
  },
};
module.exports = nextConfig;
