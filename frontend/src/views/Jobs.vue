<template>
  <div class="container">
    <h2>Job List</h2>
    <div class="actions">
      <button @click="fetchJobs" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Loading...' : 'Reload' }}
      </button>
      <button @click="showAddForm = !showAddForm" class="btn btn-success">
        {{ showAddForm ? 'Cancel Add' : 'Add New' }}
      </button>
    </div>

    <div v-if="loading" class="status">Loading...</div>
    <div v-if="error" class="status status-error">{{ error }}</div>

    <ul v-if="jobs.length && !loading && !error" class="card-list">
      <li v-for="job in jobs" :key="job.JobID" class="card">
        <!-- DISPLAY MODE -->
        <div v-if="editingId !== job.JobID" class="card-content">
          <h3>{{ job.JobTitle }}</h3>
          <p><strong>Section:</strong> {{ getSectionName(job.SectionID) }}</p>
        </div>

        <!-- EDIT MODE -->
        <div v-else class="card-content">
          <input
            v-model="form.JobTitle"
            placeholder="Job Title"
            class="input-field"
          />
          <select v-model="form.SectionID" class="input-field">
            <option disabled value="">-- select section --</option>
            <option
              v-for="sec in sectionsList"
              :key="sec.SectionID"
              :value="sec.SectionID"
            >
              {{ sec.SectionName }}
            </option>
          </select>
        </div>

        <!-- ACTIONS -->
        <div class="card-actions">
          <button
            v-if="editingId !== job.JobID"
            @click="startEdit(job)"
            class="btn btn-warning"
          >Edit</button>
          <button
            v-else
            @click="saveEdit(job.JobID)"
            class="btn btn-success"
            :disabled="saving"
          >Save</button>
          <button
            v-if="editingId === job.JobID"
            @click="cancelEdit"
            class="btn btn-secondary"
            :disabled="saving"
          >Cancel</button>
          <button
            v-if="editingId !== job.JobID"
            @click="deleteJob(job.JobID)"
            class="btn btn-danger"
            :disabled="loading"
          >Delete</button>
        </div>
      </li>
    </ul>

    <p v-else-if="!loading && !error" class="status">No jobs found</p>

    <!-- Add Form -->
    <div v-if="showAddForm" class="add-form">
      <input v-model="newJob.JobTitle" placeholder="Job Title" class="input-field" />
      <select v-model="newJob.SectionID" class="input-field">
        <option disabled value="">-- select section --</option>
        <option
          v-for="sec in sectionsList"
          :key="sec.SectionID"
          :value="sec.SectionID"
        >
          {{ sec.SectionName }}
        </option>
      </select>
      <button @click="createJob" :disabled="saving" class="btn btn-success">
        {{ saving ? 'Saving...' : 'Submit' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "JobList",
  data() {
    return {
      jobs: [],
      sectionsList: [],
      loading: false,
      saving: false,
      error: "",
      editingId: null,
      form: {
        JobTitle: "",
        SectionID: ""
      },
      showAddForm: false,
      newJob: {
        JobTitle: "",
        SectionID: ""
      }
    };
  },
  async created() {
    await this.fetchSections();
    this.fetchJobs();
  },
  methods: {
    async fetchSections() {
      try {
        const { data } = await axios.get("http://192.168.8.202:5000/api/sections");
        this.sectionsList = data;
      } catch (e) {
        console.error("Failed to load sections", e);
      }
    },
    async fetchJobs() {
      this.loading = true;
      this.error = "";
      this.editingId = null;
      try {
        const { data } = await axios.get("http://192.168.8.202:5000/api/jobs");
        this.jobs = data;
      } catch (err) {
        this.error = "Failed to load jobs: " + (err.response?.data?.error || err.message);
      } finally {
        this.loading = false;
      }
    },
    getSectionName(id) {
      const sec = this.sectionsList.find(s => s.SectionID === id);
      return sec ? sec.SectionName : "—";
    },
    startEdit(job) {
      this.editingId = job.JobID;
      this.form.JobTitle = job.JobTitle;
      this.form.SectionID = job.SectionID + "";
    },
    cancelEdit() {
      this.editingId = null;
      this.form.JobTitle = "";
      this.form.SectionID = "";
    },
    async saveEdit(id) {
      if (!this.form.JobTitle.trim() || !this.form.SectionID) {
        alert("Both Job Title and Section are required.");
        return;
      }
      this.saving = true;
      try {
        await axios.put(`http://192.168.8.202:5000/api/jobs/${id}`, {
          JobTitle: this.form.JobTitle.trim(),
          SectionID: Number(this.form.SectionID),
        });
        await this.fetchJobs();
      } catch (err) {
        alert("Failed to update job: " + (err.response?.data?.error || err.message));
      } finally {
        this.saving = false;
      }
    },
    async deleteJob(id) {
      if (!confirm(`Delete Job ID ${id}? This cannot be undone.`)) return;
      this.loading = true;
      try {
        await axios.delete(`http://192.168.8.202:5000/api/jobs/${id}`);
        await this.fetchJobs();
      } catch (err) {
        alert("Failed to delete job: " + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },
    async createJob() {
      if (!this.newJob.JobTitle.trim() || !this.newJob.SectionID) {
        alert("Both Job Title and Section are required.");
        return;
      }
      this.saving = true;
      try {
        await axios.post("http://192.168.8.202:5000/api/jobs", {
          JobTitle: this.newJob.JobTitle.trim(),
          SectionID: Number(this.newJob.SectionID),
        });
        this.newJob.JobTitle = "";
        this.newJob.SectionID = "";
        this.showAddForm = false;
        await this.fetchJobs();
      } catch (err) {
        alert("Failed to add job: " + (err.response?.data?.error || err.message));
      } finally {
        this.saving = false;
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