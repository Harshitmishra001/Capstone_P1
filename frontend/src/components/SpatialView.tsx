import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import type { MapMarker } from '../types';
import L from 'leaflet';
import { Maximize2, Layers } from 'lucide-react';

// Fix for default marker icons in react-leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export const SpatialView: React.FC<{ markers: MapMarker[] }> = ({ markers }) => {
  return (
    <div className="h-full w-full relative flex flex-col bg-white">
      <div className="h-10 border-b border-gray-200 bg-gray-50/80 px-3 flex items-center justify-between z-10 shrink-0">
        <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">Spatial Map</span>
        <div className="flex space-x-2">
          <button className="text-gray-400 hover:text-gray-700 transition p-1 hover:bg-gray-200 rounded"><Layers className="w-4 h-4" /></button>
          <button className="text-gray-400 hover:text-gray-700 transition p-1 hover:bg-gray-200 rounded"><Maximize2 className="w-4 h-4" /></button>
        </div>
      </div>
      <div className="flex-1 relative z-0">
        <MapContainer 
          center={[40.7128, -74.0060]} 
          zoom={17} 
          style={{ height: "100%", width: "100%" }}
          zoomControl={false}
        >
          <TileLayer
            attribution='&copy; OpenStreetMap'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {markers.map(m => (
            <Marker key={m.id} position={[m.lat, m.lng]}>
              <Popup>
                <div className="text-sm">
                  <strong>{m.label}</strong><br/>
                  <span className="text-gray-500">Source: {m.witness}</span>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};
