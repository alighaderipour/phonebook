<template>
  <div class="container">
    <h2>Section List</h2>
    <div class="actions">
      <button @click="fetchSections" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Loading...' : 'Reload' }}
      </button>
      <button @click="showAddForm = !showAddForm" class="btn btn-success">
        {{ showAddForm ? 'Cancel' : 'Add Section' }}
      </button>
    </div>

    <!-- Add Section Form -->
    <div class="add-form" v-if="showAddForm">
      <input
        v-model="newSection.SectionName"
        placeholder="New Section Name"
        class="input-field"
      />
      <textarea
        v-model="newSection.Description"
        placeholder="Description (optional)"
        class="input-field textarea"
      ></textarea>
      <button @click="addSection" :disabled="adding" class="btn btn-success">
        {{ adding ? 'Adding...' : 'Add Section' }}
      </button>
    </div>

    <div v-if="loading" class="status">Loading...</div>
    <div v-if="error" class="status status-error">{{ error }}</div>

    <ul v-if="sections.length && !loading && !error" class="card-list">
      <li
        v-for="sec in sections"
        :key="sec.SectionID"
        class="card"
      >
        <!-- DISPLAY MODE -->
        <div v-if="editingId !== sec.SectionID" class="card-content">
          <h3>{{ sec.SectionName }}</h3>
          <p>{{ sec.Description }}</p>
        </div>

        <!-- EDIT MODE -->
        <div v-else class="card-content">
          <input
            v-model="form.SectionName"
            placeholder="Section Name"
            class="input-field"
          />
          <textarea
            v-model="form.Description"
            placeholder="Description"
            class="input-field textarea"
          ></textarea>
        </div>

        <!-- ACTIONS -->
        <div class="card-actions">
          <button
            v-if="editingId !== sec.SectionID"
            @click="startEdit(sec)"
            class="btn btn-warning"
          >Edit</button>
          <button
            v-else
            @click="saveEdit(sec.SectionID)"
            class="btn btn-success"
            :disabled="saving"
          >Save</button>
          <button
            v-if="editingId === sec.SectionID"
            @click="cancelEdit"
            class="btn btn-secondary"
            :disabled="saving"
          >Cancel</button>
          <button
            v-if="editingId !== sec.SectionID"
            @click="deleteSection(sec.SectionID)"
            class="btn btn-danger"
            :disabled="loading"
          >Delete</button>
        </div>
      </li>
    </ul>

    <p v-else-if="!loading && !error" class="status">No section found</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      sections: [],
      loading: false,
      saving: false,
      error: "",
      editingId: null,
      form: {
        SectionName: "",
        Description: ""
      },
      showAddForm: false,
      newSection: {
        SectionName: "",
        Description: ""
      },
      adding: false,
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      this.loading = true;
      this.error = "";
      this.editingId = null;
      try {
        const { data } = await axios.get("http://192.168.8.202:5000/api/sections");
        this.sections = data;
      } catch (err) {
        this.error =
          "Failed to load sections: " + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },

    startEdit(sec) {
      this.editingId = sec.SectionID;
      this.form.SectionName = sec.SectionName;
      this.form.Description = sec.Description || "";
    },

    cancelEdit() {
      this.editingId = null;
      this.form.SectionName = "";
      this.form.Description = "";
    },

    async saveEdit(id) {
      if (!this.form.SectionName.trim()) {
        alert("SectionName cannot be empty.");
        return;
      }
      this.saving = true;
      try {
        await axios.put(`http://192.168.8.202:5000/api/sections/${id}`, {
          SectionName: this.form.SectionName.trim(),
          Description: this.form.Description.trim()
        });
        await this.fetchSections();
      } catch (err) {
        alert("Failed to update: " + (err.response?.data?.error || err.message));
      } finally {
        this.saving = false;
      }
    },

    async deleteSection(id) {
      if (!confirm(`Delete Section ID ${id}?`)) return;
      this.loading = true;
      try {
        await axios.delete(`http://192.168.8.202:5000/api/sections/${id}`);
        await this.fetchSections();
      } catch (err) {
        alert("Failed to delete: " + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },
    async addSection() {
      if (!this.newSection.SectionName.trim()) {
        alert("Section Name is required.");
        return;
      }
      this.adding = true;
      try {
        await axios.post("http://192.168.8.202:5000/api/sections", {
          SectionName: this.newSection.SectionName.trim(),
          Description: this.newSection.Description.trim()
        });
        this.newSection.SectionName = "";
        this.newSection.Description = "";
        await this.fetchSections();
      } catch (err) {
        alert("Failed to add: " + (err.response?.data?.error || err.message));
      } finally {
        this.adding = false;
      }
    }
  }
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

.add-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  margin-bottom: 24px;
}

.input-field {
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

.textarea {
  resize: vertical;
  min-height: 80px;
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
  background-color: #106fb6;
  color: #ffffff;
}

.btn-danger {
  background-color: #dc2626;
  color: #ffffff;
}

.btn-secondary {
  background-color: #6b7280;
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

.btn-secondary:hover {
  background-color: #4b5563;
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
  align-items: flex-start;
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
  flex-direction: column;
  gap: 8px;
  margin-left: 12px;
}
</style>