import React, { useState, useEffect } from 'react'

function App() {
  // set state variable to hold the data from the API
  // setData is function to manipulate the state variable
  const [data, setData] = useState([])
  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])
  return (
    <div>
      {typeof data.members === "undefined" ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member, index) => <div key={index}>{member}</div>)
      )}
    </div>
  );
}

export default App