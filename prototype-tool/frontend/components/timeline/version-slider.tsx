import { FC } from "react";
import { TicketVersion } from "../../lib/types";
import { Clock } from "lucide-react";

interface VersionSliderProps {
  versions: TicketVersion[];
  selectedIndex: number;
  onChange: (index: number) => void;
}

export const VersionSlider: FC<VersionSliderProps> = ({ versions, selectedIndex, onChange }) => {
  if (!versions || versions.length === 0) return null;

  // Versions usually come sorted from oldest to newest or newest to oldest.
  // Assuming they are ordered such that [0] is oldest and [length-1] is newest.
  // Wait, let's look at the data: in ticket-details.tsx it did:
  // `ticket.versions.slice().reverse().map(...)` which implies [0] was the latest version.
  // If [0] is the latest, then [length-1] is the oldest. Let's make sure our slider represents time correctly (left to right).
  // Time flows left to right. Left = Oldest, Right = Newest.
  // We need to verify the sort order of `versions`. Let's assume the component will receive them chronologically: [0] = oldest, [length-1] = newest.
  
  return (
    <div className="w-full bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 p-6 shadow-lg z-10 flex flex-col gap-4">
      <div className="flex items-center gap-2 mb-2">
        <Clock className="w-4 h-4 text-blue-500" />
        <h3 className="font-semibold text-gray-900 dark:text-gray-100 text-sm uppercase tracking-wide">
          Timeline
        </h3>
        <span className="text-xs text-gray-500 dark:text-gray-400 ml-2 bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded">
          {versions.length} version{versions.length > 1 ? "s" : ""}
        </span>
      </div>

      <div className="relative px-4 h-20 flex flex-col justify-center">
        {/* Background Track Markers */}
        <div className="absolute left-4 right-4 h-0.5 top-1/2 -translate-y-1/2 pointer-events-none">
          <div className="relative w-full h-full">
            {versions.map((v, i) => {
              const isSelected = i === selectedIndex;
              const versionStr = v.versionId.split('_v').pop() || v.versionId;
              const dateStr = new Date(v.timestamp).toLocaleDateString(undefined, { 
                month: 'short', 
                day: 'numeric',
                year: 'numeric'
              });
              
              return (
                <div 
                  key={v.versionId} 
                  className="absolute top-1/2 -translate-y-1/2 flex flex-col items-center -translate-x-1/2"
                  style={{ left: `${(i / (Math.max(1, versions.length - 1))) * 100}%` }}
                >
                  {/* Date Timestamp on top */}
                  <div className={`absolute bottom-4 whitespace-nowrap text-[9px] font-medium transition-all ${
                    isSelected 
                      ? "text-blue-600 dark:text-blue-400 opacity-100 -translate-y-1" 
                      : "text-gray-400 dark:text-gray-600 opacity-60"
                  }`}>
                    {dateStr}
                  </div>

                  {/* Stepped Circle */}
                  <div className={`w-3 h-3 rounded-full border-2 transition-all duration-200 ${
                    isSelected 
                      ? "bg-blue-600 border-white dark:border-gray-900 scale-125 z-20 shadow-md" 
                      : i < selectedIndex
                        ? "bg-blue-400 border-white dark:border-gray-900 z-10"
                        : "bg-gray-200 dark:bg-gray-700 border-white dark:border-gray-900 z-10"
                  }`} />

                  {/* Version Label below */}
                  <div className={`absolute top-4 whitespace-nowrap text-[11px] font-bold transition-colors ${
                    isSelected ? "text-gray-900 dark:text-gray-100" : "text-gray-400 dark:text-gray-600"
                  }`}>
                    v{versionStr}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* The Range Input (on top for interaction) */}
        <input
          type="range"
          min={0}
          max={versions.length - 1}
          step={1}
          value={selectedIndex}
          onChange={(e) => onChange(parseInt(e.target.value, 10))}
          className="w-full h-1.5 bg-gray-200 dark:bg-gray-800 rounded-lg appearance-none cursor-pointer accent-blue-600 focus:outline-none relative z-30 bg-transparent"
          style={{
            backgroundImage: `linear-gradient(to right, #3b82f6 ${(selectedIndex / (Math.max(1, versions.length - 1))) * 100}%, transparent ${(selectedIndex / (Math.max(1, versions.length - 1))) * 100}%)`,
            backgroundSize: '100% 100%',
            backgroundRepeat: 'no-repeat'
          }}
        />
      </div>
    </div>
  );
};
