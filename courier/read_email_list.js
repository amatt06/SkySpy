// read_email_list.js

const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

// Define the path to the sensitive data directory using path.join
const SENSITIVE_DATA_DIR = path.join(__dirname, 'sensitive_data');

/**
 * Reads contacts from a CSV file and returns them as an array of objects.
 * Each object contains 'email' and 'first_name' properties.
 *
 * @param {string} file_name - The name of the CSV file to read.
 * @returns {Array<Object>} - An array of contacts.
 */
function getContactsFromCsv(file_name = 'email_list.csv') {
  const contacts = [];
  // Join the directory path with the file name
  const filePath = path.join(SENSITIVE_DATA_DIR, file_name);

  // Read the CSV file and process each row
  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (row) => {
      contacts.push({
        email: row.email,
        first_name: row.first_name,
      });
    })
    .on('end', () => {
      console.log('CSV file successfully processed.');
    })
    .on('error', (err) => {
      console.error(`Error reading CSV file: ${err.message}`);
    });

  return contacts;
}

// Export the function for use in other modules
module.exports = { getContactsFromCsv };
