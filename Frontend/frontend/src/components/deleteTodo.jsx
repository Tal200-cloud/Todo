import React from 'react';

const DeleteTodo = ({ id, onDelete }) => {
  const handleDelete = async () => {
    if (window.confirm('Confirm delete')) {
      try {
        await api.delete(`/todos/${id}`);
        onDelete();
      } catch (error) {
        console.error("Error deleting todo", error);
      }
    }
  };

  return (
    <button onClick={handleDelete} className="btn btn-danger">
      Delete
    </button>
  );
};

export default DeleteTodo;