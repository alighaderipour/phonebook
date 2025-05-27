<template>
  <div class="app-container">
    <header class="app-header">
      <h1>{{ appTitle }}</h1>
      <p class="author">توسعه داده شده توسط {{ authorName }}</p>
    </header>

    <main class="app-main">
      <section class="feature-section">
        <h2>ویژگی‌های برنامه</h2>
        <ul class="features-list">
          <li v-for="(feature, index) in features" :key="index">
            {{ feature }}
          </li>
        </ul>
      </section>

    </main>

    <footer class="app-footer">
      <p>© {{ currentYear }} - تمام حقوق محفوظ است</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'MyProfessionalApp',
  data() {
    return {
      appTitle: ' دفترچه تلفن بیمارستان حضرت فاطمه (س) کرمان',
      authorName: 'بیمارستان حضرت فاطمه (س) کرمان', // نام خود را اینجا قرار دهید
      features: [
        'قابلیت جستجو شماره افراد',
        'قابلیت جستجو شماره های پزشکان',
        'قابلیت اضافه کردن بخش، شغل',
        'قابلیت اضافه کردن افراد، نوع شماره تلفن، موبایل',
        'بهینه‌سازی شده برای عملکرد عالی'
      ],
      count: 0,
      currentYear: new Date().getFullYear()
    }
  },

}
</script>

<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  direction: rtl;
  text-align: right;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.app-header h1 {
  color: #2c3e50;
  font-size: 2.2rem;
}

.author {
  color: #7f8c8d;
  font-style: italic;
}

.app-main {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-section {
  margin-bottom: 30px;
}

.feature-section h2 {
  color: #3498db;
  border-bottom: 2px solid #3498db;
  padding-bottom: 5px;
  display: inline-block;
}

.features-list {
  list-style-type: square;
  padding-right: 20px;
}

.features-list li {
  margin-bottom: 8px;
  color: #34495e;
}

.counter-section {
  text-align: center;
  padding: 20px;
  background-color: #ecf0f1;
  border-radius: 8px;
}

.counter-section p {
  font-size: 1.2rem;
  margin-bottom: 15px;
}

.action-button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #27ae60;
}

.action-button.secondary {
  background-color: #e74c3c;
}

.action-button.secondary:hover {
  background-color: #c0392b;
}

.app-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  color: #95a5a6;
  font-size: 0.9rem;
}
</style>