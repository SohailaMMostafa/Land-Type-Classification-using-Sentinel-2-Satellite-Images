export const metadata = {
  title: 'Land Type Classification - Sentinel-2 Satellite Images',
  description: 'Classify land types using AI and Sentinel-2 satellite imagery',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
