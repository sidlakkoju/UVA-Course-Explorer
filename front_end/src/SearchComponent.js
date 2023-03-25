import React, { useState } from "react";

function SearchComponent() {
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState("");

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
    setSearchResults(data.results);
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
