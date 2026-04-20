"use client";

import Link from "next/link";
import { FC } from "react";
import {
  LayoutDashboard,
  Clock,
  Network,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useSidebar } from "./sidebar-context";
import { cn } from "@/lib/utils";
import { ClientOnly } from "../ui/client-only";

export const Sidebar: FC = () => {
  const { isCollapsed, toggleSidebar } = useSidebar();

  return (
    <aside
      className={cn(
        "bg-gray-900 h-screen sticky top-0 flex-shrink-0 transition-all duration-300 ease-in-out border-r border-gray-800",
        isCollapsed ? "w-20" : "w-64"
      )}
    >
      <div className="p-4 flex flex-col h-full">
        <div className={cn(
          "mb-8 flex items-center justify-between",
          isCollapsed ? "flex-col gap-4" : "flex-row"
        )}>
          {!isCollapsed && (
            <div>
              <h1 className="text-xl font-bold text-white">DISCO-ML</h1>
              <p className="text-xs text-gray-400 mt-1">Decision Knowledge Base</p>
            </div>
          )}
          {isCollapsed && (
             <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
               D
             </div>
          )}
        </div>

        <nav className="flex flex-col gap-1 flex-1">
          <SidebarItem
            href="/"
            icon={<LayoutDashboard className="w-5 h-5" />}
            label="Dashboard"
            isCollapsed={isCollapsed}
          />
          <SidebarItem
            href="/timeline"
            icon={<Clock className="w-5 h-5" />}
            label="Timeline View"
            isCollapsed={isCollapsed}
          />
          <SidebarItem
            href="/graph"
            icon={<Network className="w-5 h-5" />}
            label="Graph View"
            isCollapsed={isCollapsed}
          />
        </nav>

        <div className="mt-auto pt-4 border-t border-gray-800">
          <button
            onClick={toggleSidebar}
            className="w-full flex items-center justify-center p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ClientOnly>
              {isCollapsed ? <ChevronRight className="w-5 h-5" /> : (
                <div className="flex items-center gap-3 w-full px-1">
                  <ChevronLeft className="w-5 h-5" />
                  <span className="text-sm">Collapse Sidebar</span>
                </div>
              )}
            </ClientOnly>
          </button>
        </div>
      </div>
    </aside>
  );
};

interface SidebarItemProps {
  href: string;
  icon: React.ReactNode;
  label: string;
  isCollapsed: boolean;
}

const SidebarItem: FC<SidebarItemProps> = ({ href, icon, label, isCollapsed }) => (
  <Link
    href={href}
    className={cn(
      "flex items-center gap-3 px-3 py-2 text-gray-300 hover:bg-gray-800 hover:text-white rounded-lg transition-colors",
      isCollapsed ? "justify-center px-2" : ""
    )}
    title={isCollapsed ? label : ""}
  >
    <ClientOnly fallback={<div className="w-5 h-5" />}>
      {icon}
    </ClientOnly>
    {!isCollapsed && <span className="text-sm font-medium">{label}</span>}
  </Link>
);
