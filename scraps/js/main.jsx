import React from "react";
import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';
// import SimpleComponent from './SimpleComponent.js';
// import Post from './post'

// const root = createRoot(document.getElementById('reactEntry'));
const root = ReactDOM.createRoot(document.getElementById('reactEntry'));
const SimpleComponent = () => {
  return (<div>Hello, I'm a simple component!</div>);
};


// im sad and confused 
// dont be sad we will figure this out 
root.render(
    <SimpleComponent />
);

// root.render(
//     <SimpleComponent />
//     {/* <Post /> */}
// );
