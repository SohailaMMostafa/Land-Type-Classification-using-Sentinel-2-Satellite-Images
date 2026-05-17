/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable Vercel Python Functions support
  experimental: {
    serverComponentsExternalPackages: ['torch', 'torchvision', 'numpy', 'rasterio', 'joblib', 'pillow'],
  },
}

module.exports = nextConfig
