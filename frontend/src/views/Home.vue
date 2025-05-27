<template>
  <div class="container">
    <img src="../images/logo.jpg" class="logo">
    <h2>جستجوی کارکنان و پزشکان</h2>
    <div class="search-bar">
      <input
  v-model="query"
  @input="debouncedSearch"
  type="text"
  placeholder="جستجوی نام، شغل، شماره تلفن یا بخش..."
  class="input-field"
/>
      <button @click="performSearch" class="btn btn-primary">جستجو</button>
    </div>

    <!-- Status messages -->
    <div v-if="loading" class="status">در حال جستجو...</div>
    <div v-if="error" class="status status-error">{{ error }}</div>
    <div
      v-if="!loading && !error && results.length === 0 && tried"
      class="status"
    >
      نتیجه‌ای یافت نشد.
    </div>

    <!-- Results list -->
    <div v-if="results.length" class="card-list">
      <div v-for="user in results" :key="user.UserID" class="card">
        <h3 class="card-title">{{ user.FirstName }} {{ user.LastName }}</h3>
        <div class="card-field">
          <i class="fas fa-building card-icon"></i>
          <span><strong>بخش:</strong> {{ user.SectionName || "—" }}</span>
        </div>
        <div class="card-field">
          <i class="fas fa-briefcase card-icon"></i>
          <span><strong>عنوان شغلی:</strong> {{ user.JobTitle || "—" }}</span>
        </div>
        <div class="card-field">
          <i class="fas fa-mobile-alt card-icon"></i>
          <span><strong>موبایل:</strong> {{ user.Mobile || "—" }}</span>
        </div>
        <div class="card-field">
          <i class="fas fa-phone card-icon"></i>
          <strong>شماره‌های تلفن:</strong>
          <ul v-if="user.PhoneNumbers.length">
            <li
              v-for="(phone, idx) in user.PhoneNumbers"
              :key="idx"
            >
              {{ phone.PhoneNumber }}
              <em>({{ phone.PhoneTypeName || "ناشناخته" }})</em>
            </li>
          </ul>
          <p v-else class="no-data">هیچ شماره تلفنی وجود ندارد</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchDirectory",
  data() {
    return {
      query: "",
    results: [],
    loading: false,
    error: "",
    tried: false,
    debounceTimer: null, // NEW
    };
  },
  methods: {
  async performSearch() {
    this.tried = true;
    if (!this.query.trim()) {
      this.error = "لطفاً یک عبارت جستجو وارد کنید.";
      this.results = [];
      return;
    }

    this.loading = true;
    this.error = "";
    this.results = [];

    try {
      const response = await axios.get("http://192.168.8.202:5000/search", {
        params: { q: this.query.trim() },
      });
      this.results = response.data;
    } catch (err) {
      this.error = err.response?.data?.error || "جستجو ناموفق بود.";
    } finally {
      this.loading = false;
    }
  },

  debouncedSearch() {
    this.tried = true;
    clearTimeout(this.debounceTimer);
    if (this.query.trim().length < 2) {
      this.results = [];
      return;
    }
    this.debounceTimer = setTimeout(() => {
      this.performSearch();
    }, 300);
  },
},
};
</script>

<style scoped>
@import url('@/assets/fonts/vazirmatn/css/vazirmatn.css');
@import url('@/assets/fonts/fontawesome/css/all.min.css');

.container {
  max-width: 800px;
  margin: 32px auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Vazirmatn', 'Inter', system-ui, sans-serif;
  direction: rtl;
  text-align: center; /* Center content for logo alignment */
}

.logo {
  width: 100px;
  height: auto;
  display: block;
  margin: 0 auto 16px; /* Center horizontally, add space below */
}

h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  text-align: right;
  margin-bottom: 24px;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.search-bar {
  display: flex;
  flex-direction: row-reverse;
  gap: 12px;
  margin-bottom: 24px;
}

.input-field {
  flex: 1;
  padding: 10px 12px;
  font-size: 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.2s, box-shadow 0.2s;
  text-align: right;
}

.input-field:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.btn-primary {
  background-color: #2563eb;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.status {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
}

.status-error {
  color: #dc2626;
  font-weight: 500;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  padding: 20px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  animation: fadeIn 0.5s ease-out;
}

.card:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px;
  text-align: right;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.card-field {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #4b5563;
  margin: 8px 0;
  text-align: right;
}

.card-field strong {
  color: #1f2937;
  font-weight: 600;
}

.card-icon {
  color: #2563eb;
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.card ul {
  padding-right: 30px;
  padding-left: 0;
  margin: 8px 0 0;
}

.card li {
  font-size: 14px;
  color: #4b5563;
  text-align: right;
  margin: 4px 0;
}

.no-data {
  font-size: 14px;
  font-style: italic;
  color: #6b7280;
  margin: 8px 0 0;
  text-align: right;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>