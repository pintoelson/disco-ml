"use client";

import { FC } from "react";
import { Search, Bell, Settings, Menu } from "lucide-react";
import ThemeToggle from "../theme-toggle";
import { useSidebar } from "./sidebar-context";
import { ClientOnly } from "../ui/client-only";

export const Header: FC = () => {
  const { toggleSidebar } = useSidebar();

  return (
    <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label="Toggle Sidebar"
        >
          <ClientOnly fallback={<div className="w-5 h-5" />}>
            <Menu className="w-5 h-5" />
          </ClientOnly>
        </button>
        <div className="relative w-96 hidden md:block">
          <ClientOnly fallback={<div className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" />}>
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          </ClientOnly>
          <input
            type="text"
            placeholder="Search tickets, decisions, arguments..."
            className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 dark:text-gray-100"
          />
        </div>
      </div>
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <ClientOnly fallback={<div className="w-5 h-5" />}>
            <Bell className="w-5 h-5" />
          </ClientOnly>
        </button>
        <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <ClientOnly fallback={<div className="w-5 h-5" />}>
            <Settings className="w-5 h-5" />
          </ClientOnly>
        </button>
        <div className="w-8 h-8 rounded-full bg-blue-500 dark:bg-blue-600 flex items-center justify-center text-white font-medium ml-2">
          SC
        </div>
      </div>
    </header>
  );
};
