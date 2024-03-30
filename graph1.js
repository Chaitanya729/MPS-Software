import React, { useState } from 'react';
import axios from 'axios';
// import Graph from './Graph';
import BarChart from './graph2';
// import 'react-vis/dist/style.css';


function MyComponent() {
  //const [inputValue, setInputValue] = useState('');
  const [routeSuffix, setRouteSuffix] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Concatenate the route suffix with the base URL
      const route = `http://localhost:5000/graph/${routeSuffix}`;

      // Make a POST request to your Flask backend
     // const response = await axios.post('/your-flask-route', { data: inputValue });

      // Handle the response if needed
     // console.log(response.data);
    } catch (error) {
      // Handle errors
      console.error('Error:', error.message );
    }
  };

  return ( <div>
    <form onSubmit={handleSubmit}>
      
      <input 
        type="text" 
        value={routeSuffix} 
        onChange={(e) => setRouteSuffix(e.target.value)} 
      />
      <button type="submit">Submit</button>
    </form>
    
    {/* <h1>Graph Example</h1> */}
   
   
    {routeSuffix && routeSuffix.trim() !== '' && (
         <BarChart dataroute={`/graph/${routeSuffix}`} />
      )}
  </div>
   
  );
}

export default MyComponent;