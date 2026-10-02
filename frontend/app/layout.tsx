import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Delivery Support Resolution Agent",
  description: "Multi-agent AI workflow for order and delivery support decisions.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
