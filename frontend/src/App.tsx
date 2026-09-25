import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { IncidentWorkspace } from './pages/IncidentWorkspace';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/incidents/:id" element={<IncidentWorkspace />} />
        <Route path="/incidents" element={<Dashboard />} />
      </Routes>
    </Layout>
  );
}

export default App;
