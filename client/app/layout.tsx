import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mental Health Copilot",
  description: "Copilot for mental health professionals",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
