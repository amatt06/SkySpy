const { google } = require('googleapis');
const { authenticateGmail } = require('./gmail_api_authenticator');
const { getContactsFromCsv } = require('./read_email_list');
const fs = require('fs').promises;

/**
 * Send emails to all contacts in the CSV file with flight data.
 */
async function sendEmails() {
    try {
        // Authenticate with Gmail API
        const auth = await authenticateGmail();
        if (!auth) {
            console.error("Authentication failed.");
            return;
        }

        const gmail = google.gmail({ version: 'v1', auth });

        // Retrieve contacts from the CSV file (await for async function)
        const contacts = await getContactsFromCsv();
        if (!contacts.length) {
            console.log("No contacts to send emails to.");
            return;
        }

        // Read flight data from JSON file
        let flightData;
        try {
            const data = await fs.readFile('../scraper/london_flight_data.json', 'utf8');
            flightData = JSON.parse(data);
        } catch (error) {
            console.error("Error reading flight data JSON file:", error);
            return;
        }

        console.log(`Sending emails to ${contacts.length} contacts...`);

        // Format flight data for email
        const flightDataContent = formatFlightData(flightData);

        // Iterate over contacts and email each
        for (const contact of contacts) {
            const emailContent = `
                Hi ${contact.first_name},

                Here are some exciting flight deals we've found:

                ${flightDataContent}

                Best regards,
                SkySpy Team
            `;

            const email = createEmail(contact.email, 'SkySpy Flight Deals', emailContent);

            // Send the email
            const res = await gmail.users.messages.send({
                userId: 'me',
                requestBody: {
                    raw: email,
                },
            });

            console.log(`Email sent to ${contact.email}: ${res.status}`);
        }

        console.log("All emails sent successfully.");

    } catch (error) {
        console.error("Error sending emails:", error);
    }
}

/**
 * Create a MIME message for sending an email.
 * @param {string} to - The recipient's email address.
 * @param {string} subject - The subject of the email.
 * @param {string} message - The message body of the email.
 * @returns {string} - The base64-encoded email.
 */
function createEmail(to, subject, message) {
    const str = [
        `To: ${to}`,
        'Content-Type: text/plain; charset=utf-8',
        'MIME-Version: 1.0',
        `Subject: ${subject}`,
        '',
        message
    ].join('\n');

    return Buffer.from(str)
        .toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

/**
 * Format flight data for email content.
 * @param {object} flightData - The flight data read from the JSON file.
 * @returns {string} - The formatted flight data content.
 */
function formatFlightData(flightData) {
    let content = 'Top Deals:\n\n';

    if (flightData.top_deals_by_percentage && flightData.top_deals_by_percentage.length > 0) {
        content += 'Top 15 Deals by Percentage Cheaper:\n';
        flightData.top_deals_by_percentage.forEach(deal => {
            content += `Destination: ${deal.destination}\nPrice: £${deal.price}\nPercentage Cheaper: ${deal.percentage_cheaper.toFixed(2)}%\n\n`;
        });
    }

    if (flightData.top_deals_by_price && flightData.top_deals_by_price.length > 0) {
        content += 'Top 8 Cheapest Deals:\n';
        flightData.top_deals_by_price.forEach(deal => {
            content += `Destination: ${deal.destination}\nPrice: £${deal.price}\nPercentage Cheaper: ${deal.percentage_cheaper.toFixed(2)}%\n\n`;
        });
    }

    return content;
}

// Call the function to send emails
sendEmails();

module.exports = { sendEmails };
