import React, { useState } from "react";
import CourseResultComponent from './CourseResultComponent';

import logo from './logo.svg';
import './App.css';
import sabreImage from './sabre.png';




function SearchComponent() {
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);


  const handleSearchInputChange = (event) => {
    setSearchInput(event.target.value);
  };

  const handleSearch = async () => {
    setIsLoading(true);
    const response = await fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ searchInput }),
    });
    const data = await response.json();
    setIsLoading(false);
    if (data && Array.isArray(data)) {
      const searchResults = data.map((result, index) => (
        <div key={index}>
          
          <CourseResultComponent  
            name={result.name}
            level={result.level}
            catalog_number={result.catalog_number}
            class_number={result.class_number}
            subject={result.subject}
            description = {result.description}
            mnemonic = {result.mnemonic}
            similarity_score = {result.similarity_score}
            credits = {result.credits}
            onMoreLikeThisClick={handleMoreLikeThisRequest}

          />
        </div>
      ));
      setSearchResults(searchResults);
    }
  };




  const handleMoreLikeThisRequest = async(mnemonicInput, catalogNumberInput) => {
    setSearchInput(`More like ${mnemonicInput} ${catalogNumberInput}`);
    setIsLoading(true);
    const response = await fetch("/similar_courses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({mnemonic: mnemonicInput, catalog_number: catalogNumberInput})
    });

    //TODO: extract this out into a separate method because it's copied from handleSearch()
    const data = await response.json();
    setIsLoading(false);
    if (data && Array.isArray(data)) {
      const searchResults = data.map((result, index) => (
        <div key={index}>
          
          <CourseResultComponent  
            name={result.name}
            level={result.level}
            catalog_number={result.catalog_number}
            class_number={result.class_number}
            subject={result.subject}
            description = {result.description}
            mnemonic = {result.mnemonic}
            similarity_score = {result.similarity_score}
            credits = {result.credits}
            onMoreLikeThisClick={handleMoreLikeThisRequest}
          />
        </div>
      ));
      //console.log(searchResults);
      setSearchResults(searchResults);
    }
}
  

  return (
    <div>
      <div><textarea placeholder="What do you want to learn about?" value={searchInput} onChange={handleSearchInputChange} /></div>
      <div><button onClick={handleSearch} style={{fontFamily:'Courier New', fontWeight:'bold'}}>Search</button></div>
      <div>{isLoading && <img src={sabreImage} className="App-logo" alt="logo" />}</div>
      <div>{isLoading && <h5>Running the OpenAI Embedding Engine...</h5>}</div>
      <div>{searchResults}</div>
    </div>
  );
}

export default SearchComponent;