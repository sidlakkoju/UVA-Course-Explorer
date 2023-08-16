import React, { useState, useEffect } from 'react';
import SearchComponent from './SearchComponent';
import './App.css';
import PlotlyGraph from './PlotlyGraph';



// import html from "./graph.html";



function App() {
  
  
  // Testing Code Remove Later
  const [members, setMembers] = useState([]);
  useEffect(() => {
    fetch('/members').then(res => res.json()).then(data => {
      setMembers(data.members);
      //console.log(data.members);
    });
  }, []);
  // END Testing Code 



  return (
    <div className="App">
      <header className="App-header">

        <p style={{fontFamily:'Courier', fontSize:'60px'}}>UVA Course Explorer</p>
        <div><PlotlyGraph src="/graph.html" width="1800px" height="700px" /></div>
        
        <div><SearchComponent /></div>
        
      </header>
    </div>
  );
}

export default App;
