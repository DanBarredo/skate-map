<template>
    <div class="map-wrap">
        <div ref="mapContainer" class="map"></div>

        <div v-if="selectedSpot" class="spot-card">
            <div class="spot-header">
                <h3>🛹 {{ selectedSpot.name }}</h3>

                <button 
                class="fav-toggle-btn" 
                :class="{ 'is-active': isFavourited(selectedSpot) }"
                @click="toggleFavourite(selectedSpot)"
                title="Toggle Favorite"
                >
                {{ isFavourited(selectedSpot) ? '★' : '☆' }}
                </button>
            </div>

            <p><strong>Type:</strong> {{ selectedSpot.type }}</p>
            <button class="directions-btn" @click="showDirectionsToast">🧭 Directions</button>
            <button class="close-btn" @click="selectedSpot = null">Close Details</button>
        </div>

        <div v-if="pendingSpotCoords" class="add-spot-form">
            <h3>Save spot?</h3>
            <p class="coords-display">Lat: {{ pendingSpotCoords.lat.toFixed(4) }}, Lng: {{ pendingSpotCoords.lng.toFixed(4) }}</p>
            
            <label>Name</label>
            <input type="text" placeholder="e.g., Marble 3-Stair" v-model="pendingSpotName" />

            <label>Type</label>
            <select>
                <option value="street">Street Spot</option>
                <option value="skatepark">Skatepark</option>
                <option value="diy">DIY Space</option>
                <option value="street">Flatland</option>
                <option value="street">Hill</option>
            </select>

            <div class="form-actions">
                <button class="save-btn" @click="mockSaveSpot">Save</button>
                <button class="cancel-btn" @click="cancelAddSpot">Cancel</button>
            </div>
        </div>

        <div v-if="toast.visible" class="toast" :class="toast.type">
            {{ toast.message }}
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

// DOM element reference
const mapContainer = ref(null);
const mapInstance = ref(null);
const selectedSpot = ref(null);

// new spot reference
const pendingSpotCoords = ref(null);
const pendingSpotName = ref(null);
let previewMarker = null;

// Toast notification state
const toast = ref({
    visible: false,
    message: '',
    type: 'info'
});

// Function to show toast notification
const showToast = (message, type = 'info', duration = 3000) => {
    toast.value = { visible: true, message, type };
    setTimeout(() => {
        toast.value.visible = false;
    }, duration);
};

// Show toast for directions feature (coming soon)
const showDirectionsToast = () => {
    showToast('In-app navigation coming soon!', 'info');
};

// Mock Database Array (Simulating your future Supabase data)
// TODO: Replace with API call -> fetchSpots() to load from Supabase on mount
const mockSpots = ref([
    {
        id: 1,
        name: "Southbank Skatepark",
        lat: 51.5065,
        lng: -0.116,
        type: "Park",
    },
    {
        id: 2,
        name: "Under-Bridge Ledge",
        lat: 51.5074,
        lng: -0.1278,
        type: "Street Ledge",
    },
    {
        id: 3,
        name: "Bay Sixty 6",
        lat: 51.519,
        lng: -0.211,
        type: "Indoor Park",
    },
]);

const favouriteSpotIds = ref([1]); // Mock user favorites (IDs of spots)

// Haversine formula: Calculate distance between two coordinates in kilometers
const calculateDistance = (lat1, lng1, lat2, lng2) => {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng / 2) * Math.sin(dLng / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
};

// Check if a nearby spot exists within the radius threshold
const NEARBY_RADIUS_KM = 0.1; // 50 meters

const findNearbySpot = (lat, lng) => {
    return mockSpots.value.find(spot => {
        const distance = calculateDistance(lat, lng, spot.lat, spot.lng);
        return distance <= NEARBY_RADIUS_KM;
    });
};

// function to cancel adding new spot - clear pending marker and reset state
const cancelAddSpot = () => {
    pendingSpotCoords.value = null
    if (previewMarker) {
        previewMarker.remove();
        previewMarker = null;
    }
}

// mock function save spot
// TODO: replace with API call -> saveNewSpot(pendingSpotCoords.value, formData)
const mockSaveSpot = () => {
    const newSpot = {
        id: Date.now(),
        name: pendingSpotName.value,
        lat: pendingSpotCoords.value.lat,
        lng: pendingSpotCoords.value.lng,
        type: "Street",
    }

    mockSpots.value.push(newSpot);

    const el = document.createElement('div')
    el.className = "custom-marker";
    el.innerHTML = "📍";
    el.style.fontSize = '24px';
    el.style.cursor = "pointer";
    el.addEventListener('click', () => {
        selectedSpot.value = newSpot;
    });

    new maplibregl.Marker({ element: el })
    .setLngLat([newSpot.lng, newSpot.lat])
    .addTo(mapInstance.value);

    cancelAddSpot();
}

// helper function - check if current spot is in favourites list
const isFavourited = (spot) => {
    if (!spot) return false;
    return favouriteSpotIds.value.includes(spot.id);
};

const toggleFavourite = (spot) => {
    if (!spot) return;
    if (isFavourited(spot)) {
        favouriteSpotIds.value = favouriteSpotIds.value.filter(id => id !== spot.id);
        console.log(`Removed spot ${spot.name} from favourites`);
    } else {
        favouriteSpotIds.value.push(spot.id);
        console.log(`Added spot ${spot.name} to favourites`);
    }
}

onMounted(() => {
    // Initialize the MapLibre Map
    mapInstance.value = new maplibregl.Map({
        container: mapContainer.value,
        style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', // CartoDB positron style
        center: [-0.1278, 51.5074], // [lng, lat] Defaulting to London area
        zoom: 12,
    });

    // Add standard navigation controls (zoom/rotate buttons)
    mapInstance.value.addControl(
        new maplibregl.NavigationControl(),
        "top-right",
    );
    // Add Geolocation control to track and center on the user's phone GPS
    mapInstance.value.addControl(
    new maplibregl.GeolocateControl({
        positionOptions: {
        enableHighAccuracy: true
        },
        trackUserLocation: true,
        showUserLocation: true
    }),
    'top-right'
    );

    // Loop through mock spots and drop HTML markers on the canvas
    mockSpots.value.forEach((spot) => {
        // Create a custom HTML element for the marker wrapper
        const el = document.createElement("div");
        el.className = "custom-marker";
        el.innerHTML = "📍";
        el.style.fontSize = "24px";
        el.style.cursor = "pointer";

        // Listen to clicks on the marker to update Vue state
        el.addEventListener("click", () => {
            selectedSpot.value = spot;
        });

        // Instantiate and anchor the marker to the map instance
        new maplibregl.Marker({ element: el })
            .setLngLat([spot.lng, spot.lat])
            .addTo(mapInstance.value);
    });

    // Capture long presses / clicks on the empty map to register new coordinates
    mapInstance.value.on("click", (e) => {
        console.log(
            `Map clicked at: Lng: ${e.lngLat.lng}, Lat: ${e.lngLat.lat}`,
        );

        const { lng, lat } = e.lngLat;
        
        // Check for nearby existing spot
        const nearbySpot = findNearbySpot(lat, lng);
        
        if (nearbySpot) {
            // Nearby spot found - show it instead of add form
            selectedSpot.value = nearbySpot;
            console.log(`Found nearby spot: ${nearbySpot.name} (${(calculateDistance(lat, lng, nearbySpot.lat, nearbySpot.lng) * 1000).toFixed(0)}m away)`);
            
            // Clear any pending form or preview marker
            pendingSpotCoords.value = null;
            if (previewMarker) {
                previewMarker.remove();
                previewMarker = null;
            }
        } else {
            // No nearby spot - proceed with add form
            pendingSpotCoords.value = { lng, lat };

            if (previewMarker) previewMarker.remove();
        
            previewMarker = new maplibregl.Marker({ color: '#f4757'})
            .setLngLat([lng, lat])
            .addTo(mapInstance.value);
        }
    });
});

// Clean up map resources on component unmount to prevent memory leaks
onUnmounted(() => {
    if (mapInstance.value) {
        mapInstance.value.remove();
    }
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

:root {
  box-sizing: border-box;
}

*, *::before, *::after {
  box-sizing: inherit;
}

.map-wrap {
    position: relative;
    width: 100vw;
    height: 100vh;
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    color: #1f2937;
}

.map {
    position: absolute;
    width: 100%;
    height: 100%;
}

/* UI Overlay Card Styling */
.spot-card {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.18);
    z-index: 10;
    width: min(94vw, 360px);
    max-width: 360px;
    color: #1f2937;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.spot-card h3 {
    margin: 0;
    font-size: 1.1rem;
    line-height: 1.25;
    flex: 1;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.spot-card button {
    padding: 10px 12px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    font-weight: 600;
    box-sizing: border-box;
}

.spot-card button:hover {
    background: #1d4ed8;
}

.add-spot-form {
  font-family: inherit;
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.15);
  z-index: 10;
  width: min(94vw, 360px);
  max-height: 85vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-sizing: border-box;
}

/* Layout adjustment to place name and star side-by-side */
.spot-header {
  display: flex;
  align-items: center;
  gap: 10px;
  box-sizing: border-box;
}

.spot-header h3 {
  margin: 0;
  font-size: 1rem;
}

/* Base Star Button Styling */
.fav-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.22);
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  color: #3b82f6;
  transition: transform 0.1s ease, color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
  padding: 0;
  line-height: 1;
  box-sizing: border-box;
}

.fav-toggle-btn:hover {
  transform: scale(1.08);
  background: rgba(59, 130, 246, 0.12);
}

/* Active Gold Star State */
.fav-toggle-btn.is-active {
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
  background: rgba(245, 158, 11, 0.12);
  text-shadow: 0 0 4px rgba(245, 158, 11, 0.3);
}

.close-btn {
  width: 100%;
  padding: 10px 12px;
  background: #0d2854;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  transition: background-color 0.2s ease;
  box-sizing: border-box;
}
.close-btn:hover {
  background: #2563eb;
}

.directions-btn {
  width: 100%;
  padding: 10px 12px;
  background: #06b6d4;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s ease;
  box-sizing: border-box;
}

.directions-btn:hover {
  background: #0891b2;
}

.coords-display {
  font-size: 0.9rem;
  color: #555;
  margin: 0 0 8px 0;
}

input, select {
  padding: 12px 10px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  font: inherit;
  outline: none;
  width: 100%;
  box-sizing: border-box;
}

input:focus,
select:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.14);
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.save-btn {
  flex: 2;
  background: #22c55e;
  color: white;
  border: none;
  padding: 12px 14px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  box-sizing: border-box;
  transition: background-color 0.2s ease;
}

.save-btn:hover {
  background: #16a34a;
}

.cancel-btn {
  flex: 1;
  background: #f1f5f9;
  color: #334155;
  border: none;
  padding: 12px 14px;
  border-radius: 10px;
  cursor: pointer;
  box-sizing: border-box;
  transition: background-color 0.2s ease;
}

.cancel-btn:hover {
  background: #e2e8f0;
}

/* Toast notification */
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 14px 20px;
  border-radius: 12px;
  background: #1f2937;
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  z-index: 20;
  max-width: 90vw;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.toast.info {
  background: #3b82f6;
  color: white;
}

@media (max-width: 500px) {
  .spot-card,
  .add-spot-form {
    width: calc(100vw - 24px);
    left: 50%;
    transform: translateX(-50%);
    padding: 14px;
    border-radius: 12px;
  }

  .spot-card {
    bottom: 12px;
    gap: 10px;
  }

  .add-spot-form {
    top: 12px;
    max-height: calc(100vh - 24px);
    max-height: 90vh;
  }

  .spot-header {
    gap: 8px;
  }

  .spot-header h3 {
    font-size: 0.95rem;
  }

  .fav-toggle-btn {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .spot-card button,
  .close-btn,
  .save-btn,
  .cancel-btn {
    padding: 10px 12px;
  }

  input, select {
    padding: 10px 8px;
    font-size: 16px;
  }
}
</style>
