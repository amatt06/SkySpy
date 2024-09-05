const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const SENSITIVE_DATA_DIR = path.join(__dirname, 'sensitive_data');

/**
 * Reads contact information (email, first_name) from a CSV file.
 *
 * @param {string} file_name - The name of the CSV file (default: 'email_list.csv').
 * @returns {Promise<Array<{email: string, first_name: string}>>} - A Promise that resolves to an array of contacts.
 */
function getContactsFromCsv(file_name = 'email_list.csv') {
  return new Promise((resolve, reject) => {
    const contacts = [];
    const filePath = path.join(SENSITIVE_DATA_DIR, file_name);

    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (row) => {
        contacts.push({
          email: row.email,
          first_name: row.first_name,
        });
      })
      .on('end', () => {
        resolve(contacts);
      })
      .on('error', (err) => {
        reject(err);
      });
  });
}

module.exports = { getContactsFromCsv };
