import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { IncidentWorkspace } from './pages/IncidentWorkspace';
import { RelationshipGraph } from './components/RelationshipGraph';
import { LandingPage } from './pages/LandingPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/*" element={
        <Layout>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/incidents/:id" element={<IncidentWorkspace />} />
            <Route path="/incidents/:id/:tab" element={<IncidentWorkspace />} />
            <Route path="/incidents/:id/graph" element={<RelationshipGraph isFullScreen={true} />} />
          </Routes>
        </Layout>
      } />
    </Routes>
  );
}

export default App;
