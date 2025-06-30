import React, { useEffect, useState } from 'react';
import AddTodoForm from './addTodoForm';
import DeleteTodo from './deleteTodo';
import api from '../api';

const TodoList = () => {
  const [todos, setTodos] = useState([]);


  //displaying todos
  const fetchTodos = async () => {
    try {
      const response = await api.get('/todos/');
      setTodos(response.data);
    } catch (error) {
      console.error("Error fetching todos", error);
    }
  };

  //adding todos
  const addTodo = async (title, description = '') => {
    try {
      await api.post('/todos/', { title, description });
      fetchTodos();
    } catch (error) {
      console.error("Error adding todo", error);
    }
  };

  const toggleComplete = async (id, currentStatus) => {
    try {
      const todo = todos.find(t => t.id === id);
      await api.put(`/todos/${id}`, { 
        title: todo.title, 
        description: todo.description, 
        completed: !currentStatus 
      });
      fetchTodos();
    } catch (error) {
      console.error("Error updating todo", error);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="todo-container">
      <h2>Todo List</h2>
      {todos.length === 0 ? (
        <div className="empty-state">No todos yet</div>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <li key={todo.id} className={`todo-item ${todo.completed ? 'todo-completed' : ''}`}>
              <div className="checkbox-container">
                <input
                  type="checkbox"
                  className="checkbox-input"
                  checked={todo.completed}
                  onChange={() => toggleComplete(todo.id, todo.completed)}
                />
              </div>
              <div className="todo-content">
                <h3 className="todo-title">{todo.title}</h3>
                {todo.description && <p className="todo-description">{todo.description}</p>}
              </div>
              <div className="todo-actions">
                <span className={`todo-status ${todo.completed ? 'status-completed' : 'status-pending'}`}>
                  {todo.completed ? 'Completed' : 'Pending'}
                </span>
                <DeleteTodo id={todo.id} onDelete={fetchTodos} />
              </div>
            </li>
          ))}
        </ul>
      )}
      <AddTodoForm addTodo={addTodo} />
    </div>
  );
};

export default TodoList;