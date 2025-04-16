import React, { useState, useEffect } from "react";
import {
  getTodos,
  addTodo,
  updateTodo,
  deleteTodo,
  filterTodos,
} from "./api";
import "./styles.css";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [filter, setFilter] = useState("all");
  const [editId, setEditId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [darkMode, setDarkMode] = useState(false); // Dark mode state

  const loadTodos = async () => {
    const data =
      filter === "all" ? await getTodos() : await filterTodos(filter);
    setTodos(data);
  };

  useEffect(() => {
    loadTodos();
  }, [filter]);

  const handleAdd = async () => {
    if (!title.trim()) return;
    await addTodo({ title });
    setTitle("");
    loadTodos();
  };

  const toggleTodo = async (todo) => {
    if (todo.completed) return; // Prevent changing from completed to pending
    await updateTodo(todo.id, { ...todo, completed: !todo.completed });
    loadTodos();
  };

  const handleDelete = async (id) => {
    await deleteTodo(id);
    loadTodos();
  };

  const handleEdit = (todo) => {
    setEditId(todo.id);
    setEditTitle(todo.title);
  };

  const handleEditSave = async (id) => {
    if (!editTitle.trim()) return;
    await updateTodo(id, { title: editTitle });
    setEditId(null);
    setEditTitle("");
    loadTodos();
  };

  const handleEditCancel = () => {
    setEditId(null);
    setEditTitle("");
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`todo-container ${darkMode ? "dark" : "light"}`}>
      <h1 className="todo-title">💫 Celestial To-Do</h1>

      <button onClick={toggleDarkMode} className="dark-mode-toggle">
        {darkMode ? "🌙 Light Mode" : "🌑 Dark Mode"}
      </button>

      <div className="todo-input-section">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Add a new task..."
          className="todo-input"
        />
        <button onClick={handleAdd} className="todo-add-button">
          🌟 Add
        </button>
      </div>

      <div className="filter-buttons">
        {["all", "completed", "pending"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`filter-button ${filter === f ? "active" : ""}`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          <li key={todo.id} className="todo-item">
            {editId === todo.id ? (
              <>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="todo-input"
                />
                <button
                  onClick={() => handleEditSave(todo.id)}
                  className="custom-button"
                >
                  Save
                </button>
                <button
                  onClick={handleEditCancel}
                  className="delete-button"
                >
                  ✖
                </button>
              </>
            ) : (
              <>
                <span
                  className={`todo-text ${todo.completed ? "completed" : ""}`}
                >
                  {todo.title}
                </span>
                <div>
                  <button
                    onClick={() => toggleTodo(todo)}
                    className="custom-button"
                    style={{ marginRight: "0.5rem" }}
                    disabled={todo.completed} // Disable if already completed
                  >
                    {todo.completed ? "Completed" : "Mark as Complete"}
                  </button>
                  <button
                    onClick={() => handleEdit(todo)}
                    className="custom-button"
                    style={{ marginRight: "0.5rem" }}
                  >
                    ✏️
                  </button>
                  <button
                    onClick={() => handleDelete(todo.id)}
                    className="delete-button"
                  >
                    🗑️
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
