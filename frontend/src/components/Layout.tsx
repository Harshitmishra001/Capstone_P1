import React from 'react';
import { Eye, LayoutDashboard, FileText, Settings, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export const Layout: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const location = useLocation();
  
  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <div className="h-screen flex font-sans overflow-hidden bg-gray-50 text-gray-800">
      <aside className="w-16 md:w-64 bg-slate-900 text-white flex flex-col transition-all duration-300 shadow-xl z-20">
        <div className="h-16 flex items-center justify-center md:justify-start md:px-6 border-b border-slate-800 shrink-0">
          <Eye className="text-blue-400 h-8 w-8 flex-shrink-0" />
          <h1 className="text-xl font-bold tracking-wide ml-3 hidden md:block">Silent Witness</h1>
        </div>
        
        <nav className="flex-1 py-6 flex flex-col space-y-2 px-3">
          <Link to="/" className={`flex items-center px-3 py-3 rounded-lg transition-colors ${isActive('/') ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>
            <LayoutDashboard className="h-5 w-5 flex-shrink-0" />
            <span className="ml-3 font-medium hidden md:block">Dashboard</span>
          </Link>
          <Link to="/incidents" className={`flex items-center px-3 py-3 rounded-lg transition-colors ${isActive('/incidents') ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>
            <FileText className="h-5 w-5 flex-shrink-0" />
            <span className="ml-3 font-medium hidden md:block">Incidents</span>
          </Link>
        </nav>
        
        <div className="p-4 border-t border-slate-800 space-y-2 shrink-0">
          <button className="w-full flex items-center px-3 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
            <Settings className="h-5 w-5 flex-shrink-0" />
            <span className="ml-3 font-medium hidden md:block">Settings</span>
          </button>
          <button className="w-full flex items-center px-3 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
            <LogOut className="h-5 w-5 flex-shrink-0" />
            <span className="ml-3 font-medium hidden md:block">Log Out</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden relative">
        <div className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm z-10 shrink-0">
          <div className="flex items-center">
            <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-semibold border border-blue-200">MVP Prototype</span>
          </div>
          <div className="flex items-center space-x-4">
             <div className="w-8 h-8 rounded-full bg-slate-300 flex items-center justify-center text-sm font-bold text-slate-700">JS</div>
          </div>
        </div>
        <div className="flex-1 overflow-hidden flex flex-col relative">
          {children}
        </div>
      </main>
    </div>
  );
};
