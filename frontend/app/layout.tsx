import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Pulse AI Agent - Autonomous AI News Intelligence",
  description: "Autonomous AI intelligence agent that curates, summarizes, and publishes AI/ML news",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} text-white min-h-screen`}>
        <Navbar />
        <main className="min-h-screen pt-24 pb-12">
          {children}
        </main>
      </body>
    </html>
  );
}
