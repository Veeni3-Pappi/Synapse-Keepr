import type { Metadata } from "next";
import { ReactQueryProvider } from "@/components/providers/react-query-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Synapse Keepr",
  description: "Remember Everything. Find Anything.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}
