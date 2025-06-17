<template>
  <div class="forbidden-container">
    <h1>403 - Forbidden</h1>
    <p>You do not have permission to access this page.</p>
    <router-link to="/" class="home-link">Go back to Home</router-link>
  </div>
</template>

<script>
export default {
  name: 'Forbidden',
};
</script>

<style scoped>
.forbidden-container {
  text-align: center;
  margin-top: 100px;
}

h1 {
  font-size: 2.5rem;
  color: #e74c3c;
}

p {
  margin-top: 1rem;
  font-size: 1.2rem;
  color: #555;
}

.home-link {
  display: inline-block;
  margin-top: 2rem;
  text-decoration: none;
  background-color: #3498db;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  font-weight: bold;
}

.home-link:hover {
  background-color: #2980b9;
}
</style>
