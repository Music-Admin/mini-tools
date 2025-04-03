import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './AppLayout';
import { lazy, Suspense } from 'react';

// Lazy load route components
const ToolsDashboard = lazy(() => import('./ToolsDashboard'));
const RoyaltyCompressor = lazy(() => import('./RoyaltyCompressor'));
const CopyrightTermination = lazy(() => import('./CopyrightTermination'));

export default function App() {
  return (
    <Router>
      <AppLayout>
        <Suspense fallback={<div className="p-4 text-center">Loading...</div>}>
          <Routes>
            <Route path="/tools" element={<ToolsDashboard />} />
            <Route path="/tools/royalty-compressor" element={<RoyaltyCompressor />} />
            {/* <Route path="/copyright-termination" element={<CopyrightTermination />} /> */}
          </Routes>
        </Suspense>
      </AppLayout>
    </Router>
  );
}
