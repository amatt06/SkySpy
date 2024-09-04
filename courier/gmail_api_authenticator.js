// gmail_api_authenticator.js

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const { authenticate } = require('@google-cloud/local-auth');

// Define the path to the credentials and token files
const SENSITIVE_DATA_DIR = path.join(__dirname, 'sensitive_data');
const CREDENTIALS_PATH = path.join(SENSITIVE_DATA_DIR, 'credentials.json');
const TOKEN_PATH = path.join(SENSITIVE_DATA_DIR, 'token.json');

// Define the scopes your application will use
const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];

/**
 * Load or request authorization to call Gmail API.
 */
async function authenticateGmail() {
    let credentials;
    try {
        // Load client secrets from a local file and convert Buffer to string
        credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH).toString('utf-8'));
    } catch (err) {
        console.error('Error loading client secret file:', err);
        return null;
    }

    let token;
    try {
        // Check if we have previously stored a token and convert Buffer to string
        token = JSON.parse(fs.readFileSync(TOKEN_PATH).toString('utf-8'));
    } catch (err) {
        console.log('No previous token found. Requesting a new one...');
        token = await getNewToken(credentials);
    }

    // Create an OAuth2 client with the given credentials and token.
    const { client_secret, client_id, redirect_uris } = credentials.web;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    if (token) {
        oAuth2Client.setCredentials(token);
    }

    // Return the authenticated OAuth2 client
    return oAuth2Client;
}

/**
 * Get and store new token after prompting for user authorization.
 * @param {Object} credentials The client credentials.
 */
async function getNewToken(credentials) {
    const { client_secret, client_id, redirect_uris } = credentials.web;
    const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    // Generate an authentication URL
    const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
    });
    console.log('Authorize this app by visiting this URL:', authUrl);

    // Authenticate the user and get the tokens directly from the returned OAuth2Client object
    const authClient = await authenticate({
        scopes: SCOPES,
        keyfilePath: CREDENTIALS_PATH,
    });

    // Get the tokens from the OAuth2Client instance
    const tokens = authClient.credentials;
    oAuth2Client.setCredentials(tokens);

    // Store the token to disk for later program executions
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens));
    console.log('Token stored to', TOKEN_PATH);

    return tokens;
}

// Call the function to initiate authentication
authenticateGmail().then(() => {
    console.log('Gmail API authenticated successfully.');
}).catch((error) => {
    console.error('Error during Gmail API authentication:', error);
});

module.exports = { authenticateGmail };
