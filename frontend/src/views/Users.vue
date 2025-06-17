<template>
  <div class="container">
    <h2>User Management</h2>

    <!-- Action Buttons -->
    <div class="actions">
      <button @click="fetchUsers" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Loading...' : 'Reload' }}
      </button>
      <button @click="toggleAddForm" class="btn btn-success" :disabled="editingId || showAddForm">
        Add User
      </button>
    </div>

    <!-- Add New User Form -->
    <div class="add-form" v-if="showAddForm">
      <h3>Add New User</h3>
      <input v-model="form.FirstName" placeholder="First Name" class="input-field" />
      <input v-model="form.LastName" placeholder="Last Name" class="input-field" />
      <input v-model="form.Mobile" placeholder="Mobile" class="input-field" />
      <select v-model="form.SectionID" class="input-field">
        <option disabled value="">-- select section --</option>
        <option v-for="sec in sectionsList" :key="sec.SectionID" :value="sec.SectionID">
          {{ sec.SectionName }}
        </option>
      </select>
      <select v-model="form.JobID" class="input-field">
        <option disabled value="">-- select job --</option>
        <option v-for="job in jobsList" :key="job.JobID" :value="job.JobID">
          {{ job.JobTitle }}
        </option>
      </select>
      <label><input type="checkbox" v-model="form.is_admin" /> Admin</label>
      <label><input type="checkbox" v-model="form.IsActive" /> Active</label>
      <button @click="addUser" class="btn btn-success" :disabled="saving">Submit</button>
      <button @click="toggleAddForm" class="btn btn-secondary">Cancel</button>
    </div>

    <!-- Users Table -->
    <table class="table">
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Mobile</th>
          <th>Section</th>
          <th>Job</th>
          <th>Admin</th>
          <th>Active</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usr in users" :key="usr.UserID">
          <template v-if="editingId === usr.UserID">
            <td><input v-model="form.FirstName" class="input-field" /></td>
            <td><input v-model="form.LastName" class="input-field" /></td>
            <td><input v-model="form.Mobile" class="input-field" /></td>
            <td>
              <select v-model="form.SectionID" class="input-field">
                <option disabled value="">--</option>
                <option v-for="sec in sectionsList" :key="sec.SectionID" :value="sec.SectionID">
                  {{ sec.SectionName }}
                </option>
              </select>
            </td>
            <td>
              <select v-model="form.JobID" class="input-field">
                <option disabled value="">--</option>
                <option v-for="job in jobsList" :key="job.JobID" :value="job.JobID">
                  {{ job.JobTitle }}
                </option>
              </select>
            </td>
            <td><input type="checkbox" v-model="form.is_admin" /></td>
            <td><input type="checkbox" v-model="form.IsActive" /></td>
            <td>
              <button @click="saveEdit(usr.UserID)" class="btn btn-success" :disabled="saving">Save</button>
              <button @click="cancelEdit" class="btn btn-secondary">Cancel</button>
            </td>
          </template>
          <template v-else>
            <td>{{ usr.FirstName }}</td>
            <td>{{ usr.LastName }}</td>
            <td>{{ usr.Mobile }}</td>
            <td>{{ usr.SectionName }}</td>
            <td>{{ usr.JobTitle }}</td>
            <td>{{ usr.is_admin ? 'Yes' : 'No' }}</td>
            <td>{{ usr.IsActive ? 'Yes' : 'No' }}</td>
            <td>
              <button @click="startEdit(usr)" class="btn btn-warning" :disabled="showAddForm">Edit</button>
              <button @click="deleteUser(usr.UserID)" class="btn btn-danger" :disabled="showAddForm">Delete</button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Users',
  data() {
    return {
      users: [],
      sectionsList: [],
      jobsList: [],
      form: {
        FirstName: '',
        LastName: '',
        Mobile: '',
        SectionID: '',
        JobID: '',
        is_admin: false,
        IsActive: true
      },
      editingId: null,
      showAddForm: false,
      loading: false,
      saving: false
    };
  },
  async created() {
    await Promise.all([this.fetchSectionsList(), this.fetchJobsList()]);
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        const { data } = await axios.get('http://192.168.8.202:5000/api/users');
        this.users = data;
      } finally {
        this.loading = false;
      }
    },
    async fetchSectionsList() {
      const { data } = await axios.get('http://192.168.8.202:5000/api/sections');
      this.sectionsList = data;
    },
    async fetchJobsList() {
      const { data } = await axios.get('http://192.168.8.202:5000/api/jobs');
      this.jobsList = data;
    },
    async addUser() {
      if (!this.form.FirstName || !this.form.LastName || !this.form.Mobile || !this.form.SectionID || !this.form.JobID) {
        alert('All fields are required');
        return;
      }
      this.saving = true;
      try {
        await axios.post('http://192.168.8.202:5000/api/users', this.form);
        this.resetForm();
        this.showAddForm = false;
        this.fetchUsers();
      } catch (err) {
        alert(err.response?.data?.error || 'Add failed');
      } finally {
        this.saving = false;
      }
    },
    toggleAddForm() {
      this.showAddForm = !this.showAddForm;
      this.resetForm();
    },
    startEdit(user) {
      this.editingId = user.UserID;
      this.form = { ...user };
    },
    cancelEdit() {
      this.editingId = null;
      this.resetForm();
    },
    async saveEdit(id) {
      this.saving = true;
      try {
        await axios.put(`http://192.168.8.202:5000/api/users/${id}`, this.form);
        this.cancelEdit();
        this.fetchUsers();
      } catch (err) {
        alert(err.response?.data?.error || 'Update failed');
      } finally {
        this.saving = false;
      }
    },
    async deleteUser(id) {
      if (!confirm('Delete user?')) return;
      await axios.delete(`http://192.168.8.202:5000/api/users/${id}`);
      this.fetchUsers();
    },
    resetForm() {
      this.form = {
        FirstName: '',
        LastName: '',
        Mobile: '',
        SectionID: '',
        JobID: '',
        is_admin: false,
        IsActive: true
      };
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

h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
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

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 24px;
}

.table th,
.table td {
  border: 1px solid #e5e7eb;
  padding: 12px;
  text-align: left;
  font-size: 14px;
}

.table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #1f2937;
}

.table td {
  background-color: #f9fafb;
}

.table tr:hover td {
  background-color: #f0f8ff;
}
</style>