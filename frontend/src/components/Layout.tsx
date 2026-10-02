import React from 'react';
import { Sidebar } from './Sidebar';
import { CommandBar } from './CommandBar';

export const Layout: React.FC<{children: React.ReactNode}> = ({ children }) => {
  return (
    <div className="h-screen flex overflow-hidden">
      <CommandBar />
      <Sidebar />
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {children}
      </main>
    </div>
  );
};
