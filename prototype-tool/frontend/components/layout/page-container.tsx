import { FC, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

export const PageContainer: FC<Props> = ({ children }) => (
  <main className="flex-1 bg-gray-50 min-h-screen">{children}</main>
);
