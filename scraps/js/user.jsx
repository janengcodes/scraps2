import React from "react";
import ReactDOM from "react-dom";
import "bootstrap/dist/css/bootstrap.css";

export default function User({ username }) {
  const [username, setUsername] = useState("");
  const [profileFilename, setProfileFilename] = useState("");
  const [email, setEmail] = useState("");
  const [fullname, setFullname] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Perform multiple fetch statements using Promise.all
        const [result1] = await Promise.all([
          fetch(`/api/v1/user/${username}`),
        ]);

        // Assuming the response is in JSON format
        const data1 = await result1.json();

        // Update state with fetched data
        setUsername(data1.username);
        setProfileFilename(data1.filename);
        setEmail(data1.email);
        setFullname(data1.fullname);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [url]);

  return (
    <div>
      <h1>Hello, React!</h1>
      <p>This is a basic JSX template.</p>
    </div>
  );
}
