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
  
  
  return (
    <React.Fragment>
      <div className="accordion">
        <div className="accordion-item">
          <div 
          className="accordion-title"
          onClick={() => setIsActive(!isActive)}>
            <div>
              {props.subject} {props.catalog_number}: {props.name} ({props.level})
            </div>
            <div>{isActive ? '-' : '+'}</div>
          </div>
          <div className="accordion-content">
            <body>{props.description}</body>
            </div>
        </div>
        {isActive && <div className="accordion-content"> Add Stuff Here </div>}
      </div>
    </React.Fragment>
  );
  
}

export default CourseResultComponent

