import React, { useState, useEffect } from 'react';
import SearchComponent from './SearchComponent';
import logo from './logo.svg';
import './App.css';

function App() {
  
  // Testing Code Remove Later
  const [members, setMembers] = useState([]);
  useEffect(() => {
    fetch('/members').then(res => res.json()).then(data => {
      setMembers(data.members);
      console.log(data.members);
    });
  }, []);
  // END Testing Code 



  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <SearchComponent />
      </header>
    </div>
  );
}

export default App;
