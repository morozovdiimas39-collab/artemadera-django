import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TeplyShovPage from './pages/TeplyShovPage';
import PokraskaPage from './pages/PokraskaPage';
import ArtemaderaSectionPage from './pages/ArtemaderaSectionPage';
import ServiceLandingPage from './pages/ServiceLandingPage';
import { ARTEMADERA_PAGES } from './content/artemaderaStructure';
import { SERVICE_LANDING_CONTENT } from './content/serviceLandingContent';

import AdminPage from './pages/AdminPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/pokraska" element={<PokraskaPage />} />
        <Route path="/teplyy-shov" element={<TeplyShovPage />} />
        {SERVICE_LANDING_CONTENT.map((p) => (
          <Route key={p.path} path={p.path} element={<ServiceLandingPage />} />
        ))}
        {ARTEMADERA_PAGES
          .filter((p) => !['/pokraska', '/teplyy-shov', ...SERVICE_LANDING_CONTENT.map((s) => s.path)].includes(p.path))
          .map((p) => (
            <Route key={p.path} path={p.path} element={<ArtemaderaSectionPage />} />
          ))}
      </Routes>
    </BrowserRouter>
  );
}
