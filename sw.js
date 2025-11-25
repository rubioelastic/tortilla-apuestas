// Service Worker para TortillApuestas PWA
const CACHE_NAME = 'tortilla-apuestas-v1';
const urlsToCache = [
  '/tortilla-apuestas/',
  '/tortilla-apuestas/index.html',
  '/tortilla-apuestas/ConTortilla.png',
  '/tortilla-apuestas/SinTortilla.png',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalación - cachear recursos estáticos
self.addEventListener('install', (event) => {
  console.log('📦 Service Worker instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('✅ Caché abierto, guardando recursos...');
        return cache.addAll(urlsToCache);
      })
      .catch((error) => {
        console.error('❌ Error cacheando recursos:', error);
      })
  );
  self.skipWaiting();
});

// Activación - limpiar cachés antiguas
self.addEventListener('activate', (event) => {
  console.log('🔄 Service Worker activando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Eliminando caché antigua:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch - estrategia Network First con Cache Fallback
self.addEventListener('fetch', (event) => {
  // Solo cachear peticiones GET
  if (event.request.method !== 'GET') return;

  // No cachear Firebase o APIs externas
  if (
    event.request.url.includes('firebasestorage.googleapis.com') ||
    event.request.url.includes('firestore.googleapis.com') ||
    event.request.url.includes('identitytoolkit.googleapis.com')
  ) {
    return;
  }

  event.respondWith(
    // Intentar red primero
    fetch(event.request)
      .then((response) => {
        // Si la respuesta es válida, clonarla y guardarla en caché
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Si falla la red, usar caché
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            console.log('📂 Sirviendo desde caché:', event.request.url);
            return cachedResponse;
          }
          // Si no hay en caché, devolver página offline personalizada
          if (event.request.destination === 'document') {
            return caches.match('/tortilla-apuestas/index.html');
          }
        });
      })
  );
});

// Escuchar mensajes del cliente
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
