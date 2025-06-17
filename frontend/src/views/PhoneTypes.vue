<template>
  <div class="container">
    <h2>Phone Type List</h2>

    <div class="actions">
      <button @click="fetchPhoneTypes" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Loading...' : 'Reload' }}
      </button>
    </div>

    <!-- Add new phone type section -->
    <div class="add-section">
      <input
        v-model="newPhoneTypeName"
        type="text"
        placeholder="Enter new phone type name"
        class="input-field"
      />
      <button @click="addNewPhoneType" class="btn btn-success" :disabled="loading || !newPhoneTypeName.trim()">
        Add New
      </button>
    </div>

    <div v-if="error" class="status status-error">{{ error }}</div>

    <ul v-if="!loading && !error && phoneTypes.length" class="card-list">
      <li
        v-for="pt in phoneTypes"
        :key="pt.phoneTypeId"
        class="card"
      >
        <div class="card-content">
          <h3>{{ pt.phoneTypeId }}</h3>
          <p>{{ pt.phoneTypeName }}</p>
        </div>
        <div class="card-actions">
          <button @click="editPhoneType(pt)" class="btn btn-warning">Edit</button>
          <button @click="deletePhoneType(pt.phoneTypeId)" class="btn btn-danger">Delete</button>
        </div>
      </li>
    </ul>

    <p v-else-if="!loading && !error" class="status">No phone types found.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PhoneType",
  data() {
    return {
      phoneTypes: [],
      loading: false,
      error: "",
      newPhoneTypeName: "",
    };
  },
  created() {
    this.fetchPhoneTypes();
  },
  methods: {
    async fetchPhoneTypes() {
      this.loading = true;
      this.error = "";
      try {
        const response = await axios.get("http://192.168.8.202:5000/api/phonetypes");
        this.phoneTypes = response.data;
      } catch (err) {
        this.error =
          "Failed to load phone types: " + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    async editPhoneType(pt) {
      const newName = window.prompt("New name for PhoneType ID " + pt.phoneTypeId, pt.phoneTypeName);
      if (!newName || newName.trim() === "" || newName === pt.phoneTypeName) {
        return;
      }
      this.loading = true;
      try {
        await axios.put(`http://192.168.8.202:5000/api/phonetypes/${pt.phoneTypeId}`, {
          PhoneTypeName: newName.trim(),
        });
        this.fetchPhoneTypes();
      } catch (err) {
        alert("Failed to update: " + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },

    async deletePhoneType(id) {
      if (!confirm(`Delete PhoneType ID ${id}? This cannot be undone.`)) return;
      this.loading = true;
      try {
        await axios.delete(`http://192.168.8.202:5000/api/phonetypes/${id}`);
        this.fetchPhoneTypes();
      } catch (err) {
        alert("Failed to delete: " + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },

    async addNewPhoneType() {
      const name = this.newPhoneTypeName.trim();
      if (!name) return;

      this.loading = true;
      try {
        await axios.post("http://192.168.8.202:5000/api/phonetypes", {
          PhoneTypeName: name,
        });
        this.newPhoneTypeName = "";
        this.fetchPhoneTypes();
      } catch (err) {
        alert("Failed to add: " + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 32px auto;
  padding: 24px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', system-ui, sans-serif;
}

h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  margin-bottom: 24px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.add-section {
  display: flex;
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

.btn-success {
  background-color: #16a34a;
  color: #ffffff;
}

.btn-warning {
  background-color: #1d4ed8;
  color: #ffffff;
}

.btn-danger {
  background-color: #dc2626;
  color: #ffffff;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-success:hover {
  background-color: #15803d;
}

.btn-warning:hover {
  background-color: #0627a2;
}

.btn-danger:hover {
  background-color: #b91c1c;
}

.btn:disabled {
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
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #f9fafb;
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 6px;
}

.card-content p {
  font-size: 14px;
  color: #4b5563;
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 8px;
}
</style>