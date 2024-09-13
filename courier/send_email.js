// send_email.js

const path = require('path');
const { google } = require('googleapis');
const { authenticateGmail } = require('./gmail_api_authenticator');
const { getContactsFromCsv } = require('./read_email_list');
const fs = require('fs').promises;
const EmailFormatter = require('./email_formatter');

const flightDataPath = path.resolve(__dirname, '../scraper/flight_data/london_flight_data.json');

async function sendEmails() {
    try {
        const auth = await authenticateGmail();
        if (!auth) {
            console.error("Authentication failed.");
            return;
        }

        const gmail = google.gmail({ version: 'v1', auth });
        const contacts = await getContactsFromCsv();
        if (!contacts.length) {
            console.log("No contacts to send emails to.");
            return;
        }

        let flightData;
        try {
            const data = await fs.readFile(flightDataPath, 'utf8');
            flightData = JSON.parse(data);
        } catch (error) {
            console.error("Error reading flight data JSON file:", error);
            return;
        }

        console.log(`Sending emails to ${contacts.length} contacts...`);

        for (const contact of contacts) {
            const emailContent = EmailFormatter.formatEmailContent(flightData, contact);
            const email = EmailFormatter.createEmail(contact.email, 'SkySpy Flight Deals', emailContent);

            try {
                const res = await gmail.users.messages.send({
                    userId: 'me',
                    requestBody: {
                        raw: email,
                    },
                });

                console.log(`Email sent to ${contact.email}: ${res.status}`);
                console.log(`Response details: ${JSON.stringify(res.data)}`);
            } catch (sendError) {
                console.error(`Error sending email to ${contact.email}:`, sendError);
            }
        }

        console.log("All emails sent successfully.");

    } catch (error) {
        console.error("Error sending emails:", error);
    }
}

sendEmails().then(r => console.log("Emails sent successfully.")).catch(e => console.error("Error sending emails:", e));