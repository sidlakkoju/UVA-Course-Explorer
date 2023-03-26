import React, { useState } from 'react'

/*
name
level
catalog_number
class_number
subject
*/

const CourseResultComponent = (props) => {
  const [isActive, setIsActive] = useState(false);
  const [sessions, setSessions] = useState([]);


  const handleClick = async () => {
    setIsActive(!isActive);
    console.log("clicked");

    const response = await fetch("/detailed_info", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ catalog_number: props.catalog_number, mnemonic: props.mnemonic}),
    });
    const data = await response.json();

    if (data && Array.isArray(data)) {
      const sessions = data.map((result, index) => (
        <div key={index}>
          <body> {result.instructor}, {result.location}, {result.enrollment_capacity}, {result.current_enrolled}, {result.waitlist_capacity}, {result.current_waitlisted}, {result.days}, {result.start_time}, {result.end_time}</body>
        </div>
      ));
      console.log(sessions);
      setSessions(sessions);
    }
  }
  
  
  return (
    <React.Fragment>
      <div className="accordion">
        <div className="accordion-item">
          <div 
          className="accordion-title"
          onClick={handleClick}>
            <div>
              {props.subject} {props.catalog_number}: {props.name} ({props.level})
            </div>
            <div>{isActive ? '-' : '+'}</div>
          </div>
          <div className="accordion-content">
            <body>{props.description}</body>
            </div>
        </div>
        {isActive && <div className="accordion-content"> {sessions} </div>}
      </div>
    </React.Fragment>
  );
  
}

export default CourseResultComponent

