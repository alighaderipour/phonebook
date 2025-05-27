<template>
  <div class="container">
    <h2>Phone Number List</h2>

    <div class="actions">
      <button @click="fetchPhonenumbers" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Loading...' : 'Reload' }}
      </button>
      <button @click="openAddModal" class="btn btn-success">Add New</button>
    </div>

    <div v-if="error" class="status status-error">{{ error }}</div>

    <ul v-if="!loading && !error && phonenumbers.length" class="card-list">
      <li
        v-for="phonenumber in phonenumbers"
        :key="phonenumber.PhoneID"
        class="card"
      >
        <div class="card-content">
          <p><strong>Job ID:</strong> {{ phonenumber.JobID }}</p>
          <p><strong>Job Title:</strong> {{ phonenumber.JobTitle }}</p>
          <p><strong>Section:</strong> {{ phonenumber.SectionName }}</p>
          <p><strong>Phone:</strong> {{ phonenumber.PhoneNumber }}</p>
          <p><strong>Mobile:</strong> {{ phonenumber.Mobile || '—' }}</p>
          <p><strong>Type:</strong> {{ phonenumber.PhoneTypeName || 'Unknown' }}</p>
        </div>
        <EditDeleteButtons
          @edit="openEditModal(phonenumber)"
          @delete="handleDelete(phonenumber.PhoneID)"
        />
      </li>
    </ul>

    <p v-else-if="!loading && !error" class="status">No phone numbers found.</p>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>Edit Phone Number</h3>
        <form @submit.prevent="saveEdit" class="form">
          <label for="job">Job Title:</label>
          <select id="job" v-model="editForm.JobID" required class="input-field">
            <option v-for="job in jobs" :key="job.JobID" :value="job.JobID">
              {{ job.JobTitle }}
            </option>
          </select>

          <label for="section">Section:</label>
          <select id="section" v-model="editForm.SectionID" required class="input-field">
            <option v-for="section in sections" :key="section.SectionID" :value="section.SectionID">
              {{ section.SectionName }}
            </option>
          </select>

          <label for="phoneType">Phone Type:</label>
          <select id="phoneType" v-model="editForm.PhoneTypeID" class="input-field">
            <option v-for="type in phoneTypes" :key="type.phoneTypeId" :value="type.phoneTypeId">
              {{ type.phoneTypeName }}
            </option>
          </select>

          <label for="phoneNumber">Phone Number:</label>
          <input type="text" id="phoneNumber" v-model="editForm.PhoneNumber" required class="input-field" />

          <label for="mobile">Mobile:</label>
          <input type="text" id="mobile" v-model="editForm.Mobile" class="input-field" />

          <button type="submit" class="btn btn-success">Save</button>
          <button type="button" @click="closeEditModal" class="btn btn-secondary">Cancel</button>
        </form>
      </div>
    </div>

    <!-- Add Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h3>Add New Phone Number</h3>
        <form @submit.prevent="submitNewPhoneNumber" class="form">
          <label for="add-job">Job Title:</label>
          <select id="add-job" v-model="newForm.JobID" required class="input-field">
            <option v-for="job in jobs" :key="job.JobID" :value="job.JobID">
              {{ job.JobTitle }}
            </option>
          </select>

          <label for="add-phoneType">Phone Type:</label>
          <select id="add-phoneType" v-model="newForm.PhoneTypeID" class="input-field">
            <option v-for="type in phoneTypes" :key="type.phoneTypeId" :value="type.phoneTypeId">
              {{ type.phoneTypeName }}
            </option>
          </select>

          <label for="add-phoneNumber">Phone Number:</label>
          <input type="text" id="add-phoneNumber" v-model="newForm.PhoneNumber" required class="input-field" />

          <label for="add-mobile">Mobile:</label>
          <input type="text" id="add-mobile" v-model="newForm.Mobile" class="input-field" />

          <button type="submit" class="btn btn-success">Add</button>
          <button type="button" @click="closeAddModal" class="btn btn-secondary">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import EditDeleteButtons from "@/components/EditDeleteButtons.vue";

export default {
  name: "PhoneNumberList",
  components: {
    EditDeleteButtons,
  },
  data() {
    return {
      phonenumbers: [],
      jobs: [],
      sections: [],
      phoneTypes: [],
      loading: false,
      error: "",
      showEditModal: false,
      editForm: {
        PhoneID: null,
        JobID: null,
        SectionID: null,
        PhoneTypeID: null,
        PhoneNumber: "",
        Mobile: ""
      },
      showAddModal: false,
      newForm: {
        JobID: null,
        PhoneTypeID: null,
        PhoneNumber: "",
        Mobile: ""
      },
    };
  },
  created() {
    this.fetchPhonenumbers();
    this.fetchJobs();
    this.fetchSections();
    this.fetchPhoneTypes();
  },
  methods: {
    async fetchPhonenumbers() {
      this.loading = true;
      this.error = "";
      try {
        const response = await axios.get("http://192.168.8.202:5000/api/phones/phonenumbers");
        this.phonenumbers = response.data;
      } catch (error) {
        this.error = "Failed to load phone numbers: " + (error.response?.data?.error || error.message);
      } finally {
        this.loading = false;
      }
    },
    async fetchJobs() {
      try {
        const response = await axios.get("http://192.168.8.202:5000/api/jobs");
        this.jobs = response.data;
      } catch (error) {
        this.error = "Failed to load jobs.";
      }
    },
    async fetchSections() {
      try {
        const response = await axios.get("http://192.168.8.202:5000/api/sections");
        this.sections = response.data;
      } catch (error) {
        this.error = "Failed to load sections.";
      }
    },
    async fetchPhoneTypes() {
      try {
        const response = await axios.get("http://192.168.8.202:5000/api/phonetypes");
        this.phoneTypes = response.data.map((type) => ({
          phoneTypeId: type.phoneTypeId,
          phoneTypeName: type.phoneTypeName,
        }));
      } catch (error) {
        this.error = "Failed to load phone types.";
      }
    },
    openEditModal(phone) {
      const job = this.jobs.find((j) => j.JobID === phone.JobID);
      this.editForm = {
        PhoneID: phone.PhoneID,
        JobID: phone.JobID,
        SectionID: job ? this.sections.find((s) => s.SectionName === phone.SectionName)?.SectionID : null,
        PhoneTypeID: this.phoneTypes.find((t) => t.phoneTypeName === phone.PhoneTypeName)?.phoneTypeId || null,
        PhoneNumber: phone.PhoneNumber,
        Mobile: phone.Mobile || ""
      };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    async saveEdit() {
      try {
        const payload = {
          JobID: this.editForm.JobID,
          PhoneNumber: this.editForm.PhoneNumber,
          PhoneTypeID: this.editForm.PhoneTypeID || null,
          Mobile: this.editForm.Mobile
        };
        await axios.put(`http://192.168.80.202:5000/api/phones/${this.editForm.PhoneID}`, payload);
        this.closeEditModal();
        this.fetchPhonenumbers();
      } catch (error) {
        this.error = "Failed to update phone number: " + (error.response?.data?.error || error.message);
      }
    },
    async handleDelete(phoneId) {
      if (!confirm("Are you sure you want to delete this phone number?")) return;

      try {
        await axios.delete(`http://192.168.80.202:5000/api/phones/${phoneId}`);
        this.phonenumbers = this.phonenumbers.filter((p) => p.PhoneID !== phoneId);
      } catch (error) {
        this.error = "Failed to delete phone number: " + (error.response?.data?.error || error.message);
      }
    },
    openAddModal() {
      this.newForm = {
        JobID: this.jobs.length ? this.jobs[0].JobID : null,
        PhoneTypeID: null,
        PhoneNumber: "",
        Mobile: ""
      };
      this.showAddModal = true;
    },
    closeAddModal() {
      this.showAddModal = false;
    },
    async submitNewPhoneNumber() {
      try {
        const payload = {
          JobID: this.newForm.JobID,
          PhoneNumber: this.newForm.PhoneNumber,
          PhoneTypeID: this.newForm.PhoneTypeID || null,
          Mobile: this.newForm.Mobile
        };
        await axios.post("http://192.168.80.202:5000/api/phones/add/phonenumber", payload);
        this.closeAddModal();
        this.fetchPhonenumbers();
      } catch (error) {
        this.error = "Failed to add phone number: " + (error.response?.data?.error || error.message);
      }
    }
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
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #f9fafb;
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.card-content p {
  font-size: 14px;
  color: #4b5563;
  margin: 6px 0;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 4px;
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
</style>