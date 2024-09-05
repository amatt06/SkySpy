// send_email.js

const { google } = require('googleapis');
const { authenticateGmail } = require('./gmail_api_authenticator');
const { getContactsFromCsv } = require('./read_email_list');

/**
 * Send emails to all contacts in the CSV file.
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

        console.log(`Sending emails to ${contacts.length} contacts...`);

        // Iterate over contacts and email each
        for (const contact of contacts) {
            const emailContent = `
                Hi ${contact.first_name},

                This is a test email sent from the SkySpy project.

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

// Call the function to send emails
sendEmails();

module.exports = { sendEmails };
