<template>
  <div class="edit-delete-buttons">
    <button @click.stop="$emit('edit')" class="btn-edit">Edit</button>
    <button @click.stop="$emit('delete')" class="btn-delete">Delete</button>
  </div>
</template>

<script>
export default {
  name: "EditDeleteButtons"
};
</script>

<style scoped>
.edit-delete-buttons {
  display: flex;
  gap: 8px;
}

.btn-edit,
.btn-delete {
  padding: 4px 8px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-edit {
  background-color: #3498db;
  color: white;
}

.btn-edit:hover {
  background-color: #2980b9;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background-color: #c0392b;
}
</style>