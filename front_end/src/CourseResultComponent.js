import React, { useState } from 'react'




/*
name
level
catalog_number
class_number
subject
*/




const CourseResultComponent = (props) => {

  const accordionData = {
    title: 'Section 1',
    content: `Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quis sapiente
      laborum cupiditate possimus labore, hic temporibus velit dicta earum
      suscipit commodi eum enim atque at? Et perspiciatis dolore iure
      voluptatem.`
  };

  const { title, content } = accordionData;
  const [isActive, setIsActive] = useState(false);
  
  /*
  return (
    <div>{props.name} {props.level} {props.catalog_number} {props.class_number} {props.subject} {props.description}</div>
  );
  */
  
  return (
    <React.Fragment>
      <div className="accordion">
        <div className="accordion-item">
          <div 
          className="accordion-title"
          onClick={() => setIsActive(!isActive)}>
            <div>
              {props.catalog_number}: {props.name} ({props.level})
            </div>
            <div>{isActive ? '-' : '+'}</div>
          </div>
          <div className="accordion-content">
            <body>{props.description}</body>
            </div>
        </div>
        {isActive && <div className="accordion-content">{content}</div>}
      </div>
    </React.Fragment>
  );
  
}

export default CourseResultComponent


/*
const App = () => {
  const accordionData = {
    title: 'Section 1',
    content: `Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quis sapiente
      laborum cupiditate possimus labore, hic temporibus velit dicta earum
      suscipit commodi eum enim atque at? Et perspiciatis dolore iure
      voluptatem.`
  };

  const { title, content } = accordionData;

  return (
    <React.Fragment>
      <h1>React Accordion Demo</h1>
      <div className="accordion">
        <div className="accordion-item">
          <div className="accordion-title">
            <div>{title}</div>
            <div>+</div>
          </div>
          <div className="accordion-content">{content}</div>
        </div>
      </div>
    </React.Fragment>
  );
};

export default App;
*/

/*
import React, { Component } from 'react'

export default class CourseResultComponent extends Component {
  render() {
    return (
      <div>CourseResultComponent</div>
    )
  }
}

*/