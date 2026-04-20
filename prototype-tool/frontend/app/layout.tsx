import "./globals.css";
import { Header } from "../components/layout/header";
import { Sidebar } from "../components/layout/sidebar";
import { SidebarProvider } from "../components/layout/sidebar-context";

export const metadata = {
  title: "DISCO-ML",
  description: "Frontend for thesis prototype",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full" suppressHydrationWarning>
      <body className="flex h-full bg-gray-50 dark:bg-gray-900" suppressHydrationWarning>
        <SidebarProvider>
          <Sidebar />
          <div className="flex flex-col flex-1 min-h-0">
            <Header />
            <main className="flex-1 overflow-auto">
              {children}
            </main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  );
}
