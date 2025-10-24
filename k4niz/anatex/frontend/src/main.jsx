import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import ARScene from './components/ARScene.jsx';

function App() {
  // Demo organ data
  const organs = [
    { name: 'Heart', color: 'bg-red-500' },
    { name: 'Brain', color: 'bg-purple-500' },
    { name: 'Liver', color: 'bg-yellow-500' },
    { name: 'Lungs', color: 'bg-blue-400' },
    { name: 'Kidneys', color: 'bg-green-500' },
  ];
  const [selectedOrgan, setSelectedOrgan] = React.useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 flex flex-col">
      <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 text-white p-6 text-3xl font-extrabold text-center shadow-lg tracking-wide">
        🧠 AR Anatomy Explorer
      </header>
      <main className="flex-1 flex flex-col md:flex-row gap-6 p-6">
        <section className="flex-1 flex flex-col items-center justify-center">
          <ARScene />
          <div className="mt-6 grid grid-cols-2 md:grid-cols-3 gap-4">
            {organs.map(organ => (
              <button
                key={organ.name}
                className={`rounded-lg shadow-lg px-4 py-3 text-white font-bold text-lg transition-all duration-200 hover:scale-105 focus:outline-none ${organ.color}`}
                onClick={() => setSelectedOrgan(organ)}
              >
                {organ.name}
              </button>
            ))}
          </div>
        </section>
        <aside className="w-full md:w-1/3 bg-white rounded-2xl shadow-xl p-6 flex flex-col items-center">
          <div className="text-xl font-bold mb-2 text-blue-700">Organ Info & AI Explanation</div>
          {selectedOrgan ? (
            <div className="w-full">
              <div className={`mb-2 p-2 rounded text-white font-semibold ${selectedOrgan.color}`}>{selectedOrgan.name}</div>
              <div className="mb-2 text-gray-700">Anatomy: <span className="font-medium">Demo description for {selectedOrgan.name}.</span></div>
              <div className="bg-blue-50 border-l-4 border-blue-400 p-3 rounded text-blue-900 shadow-sm">
                <span className="font-semibold">AI Explanation:</span> The {selectedOrgan.name} is a vital organ. (Demo response)
              </div>
            </div>
          ) : (
            <div className="text-gray-600">Select an organ to see details and AI explanation.</div>
          )}
        </aside>
      </main>
      <footer className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 text-white text-center py-2 font-medium shadow-inner">
        &copy; 2025 AR Anatomy Explorer
      </footer>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
