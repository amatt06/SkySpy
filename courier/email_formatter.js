// email_formatter.js

class EmailFormatter {
    /**
     * Format flight data for email content with styling.
     * @param {object} flightData - The flight data read from the JSON file.
     * @param {object} contact - The contact information.
     * @returns {string} - The formatted and styled email content.
     */
    static formatEmailContent(flightData, contact) {
    let content = `
        <html lang="eng">
        <body>
            <p>Hi ${contact.first_name},</p>
            <p>Here are some exciting flight deals we've found:</p>
            <h2>Top Deals:</h2>
    `;

    if (flightData.top_deals_by_percentage && flightData.top_deals_by_percentage.length > 0) {
        content += '<h3>Top 15 Deals by Percentage Cheaper:</h3><ul>';
        flightData.top_deals_by_percentage.forEach(deal => {
            content += `
                <li>
                    <strong>Destination: ${deal.destination} - £${deal.price}</strong><br>
                    &nbsp;&nbsp;&nbsp;Percentage Cheaper: ${deal.percentage_cheaper.toFixed(2)}%
                </li><br>
            `;
        });
        content += '</ul>';
    }

    if (flightData.top_deals_by_price && flightData.top_deals_by_price.length > 0) {
        content += '<h3>Top 8 Cheapest Deals:</h3><ul>';
        flightData.top_deals_by_price.forEach(deal => {
            content += `
                <li>
                    <strong>Destination: ${deal.destination} - £${deal.price}</strong><br>
                    &nbsp;&nbsp;&nbsp;Percentage Cheaper: ${deal.percentage_cheaper.toFixed(2)}%
                </li><br>
            `;
        });
        content += '</ul>';
    }

    content += `
            <p>Best regards,<br>SkySpy Team</p>
        </body>
        </html>
    `;

    return content;
}

    /**
     * Create a MIME message for sending an email.
     * @param {string} to - The recipient's email address.
     * @param {string} subject - The subject of the email.
     * @param {string} message - The message body of the email.
     * @returns {string} - The base64-encoded email.
     */
    static createEmail(to, subject, message) {
        const str = [
            `To: ${to}`,
            'Content-Type: text/html; charset=utf-8',
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
}

module.exports = EmailFormatter;