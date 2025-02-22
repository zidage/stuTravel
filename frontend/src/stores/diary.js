// src/stores/diary.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useDiaryStore = defineStore('diary', () => {
  const diaryId = ref(null);

  // 设置 diaryId 的函数
  const setDiaryId = (newDiaryId) => {
    diaryId.value = newDiaryId;
  };

  // 清除 diaryId 的函数
  const clearDiaryId = () => {
    diaryId.value = null;
  };

  return {
    diaryId,
    setDiaryId,
    clearDiaryId,
  };
}, {
  persist: true // 持久化存储
});
