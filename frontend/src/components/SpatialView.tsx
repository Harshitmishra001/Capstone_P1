import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import type { MapMarker } from '../types';
import L from 'leaflet';
import { Maximize2, Layers } from 'lucide-react';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export const SpatialView: React.FC<{ markers: MapMarker[], pulsedMarkerId?: string }> = ({ markers, pulsedMarkerId }) => {
  return (
    <div className="h-full w-full relative flex flex-col bg-[var(--bg-base)]">
      <div className="h-10 border-b border-[var(--border-hairline)] bg-[var(--bg-surface-2)] px-3 flex items-center justify-between z-10 shrink-0 absolute top-0 left-0 right-0">
        <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider">Spatial Map</span>
        <div className="flex space-x-1">
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><Layers className="w-3.5 h-3.5" /></button>
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><Maximize2 className="w-3.5 h-3.5" /></button>
        </div>
      </div>
      <div className="flex-1 relative z-0 pt-10 h-full">
        <MapContainer 
          center={[40.7128, -74.0060]} 
          zoom={17} 
          style={{ height: "100%", width: "100%", background: "var(--bg-base)" }}
          zoomControl={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          {markers.map(m => (
            <React.Fragment key={m.id}>
              {m.id === pulsedMarkerId && (
                <Circle center={[m.lat, m.lng]} radius={30} pathOptions={{ color: 'var(--accent)', fillColor: 'var(--accent)', fillOpacity: 0.2 }} />
              )}
              <Marker position={[m.lat, m.lng]}>
                <Popup>
                  <div className="font-ui text-sm">
                    <strong>{m.label}</strong><br/>
                    <span className="text-gray-500 font-mono text-xs mt-1 block">Source: {m.witness}</span>
                  </div>
                </Popup>
              </Marker>
            </React.Fragment>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};
