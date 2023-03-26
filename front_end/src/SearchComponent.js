import React, { useState } from "react";
import CourseResultComponent from './CourseResultComponent';



function SearchComponent() {
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);


  const handleInputChange = (event) => {
    setSearchInput(event.target.value);
  };

  const handleSearch = async () => {
    const response = await fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ searchInput }),
    });
    const data = await response.json();
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
          />
        </div>
      ));
      console.log(searchResults);
      setSearchResults(searchResults);
    }
  };
  

  return (
    <div>
      <textarea value={searchInput} onChange={handleInputChange} />
      <button onClick={handleSearch}>Search</button>
      <div>{searchResults}</div>
      
    </div>
  );
}

export default SearchComponent;
