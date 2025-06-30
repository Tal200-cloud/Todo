import React from 'react';
import './App.css';
import TodoList from './components/Todo';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Simple Todo App</h1>
      </header>
      <main>
        <TodoList />
      </main>
    </div>
  );
};

export default App;