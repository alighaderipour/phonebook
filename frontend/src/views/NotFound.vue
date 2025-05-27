<template>
  <div class="container">
    <div class="card">
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<script setup>
// Optional logic
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9fafb;
  font-family: 'Inter', system-ui, sans-serif;
}

.card {
  padding: 24px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  font-size: 32px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
}

p {
  font-size: 16px;
  color: #4b5563;
  margin-bottom: 24px;
}

.btn {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: #2563eb;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}
</style>