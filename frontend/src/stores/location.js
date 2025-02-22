// src/stores/location.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useLocationStore = defineStore('university', () => {
  const location = ref(null);
  const totalLocations = ref([]); // 修改 totalUniversity 为数组

  const setLocation = (newLocation) => {
    location.value = newLocation;
  };

  const removeLocation = () => {
    location.value = null;
  };

  const setTotalLocations = (newTotal) => {
    totalLocations.value = newTotal;
  };

  const removeTotalLocations = () => {
    totalUniversity.value = [];
  };

  return {
    location,
    setLocation,
    removeLocation,
    totalLocations,
    setTotalLocations,
    removeTotalLocations
  };
}, {
  persist: true // 持久化存储
});
