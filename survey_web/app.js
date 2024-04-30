// Import required modules
const express = require('express');

// Create an instance of express
const app = express();
const port = 3000; // Port number to listen on

// Define a route handler for the root path
app.get('/', (req, res) => {
  res.send('Hello, world! This is a simple Node.js web server.');
});

// Start the server and listen on the specified port
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
