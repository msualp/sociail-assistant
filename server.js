const path = require('path');
const express = require('express');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;
const resendApiKey = process.env.RESEND_API_KEY;
const resendFrom = process.env.RESEND_FROM || 'Sociail Assistant <onboarding@resend.dev>';
const resendNotifyTo = process.env.RESEND_NOTIFY_TO || 'msualp@sociail.com';
const resendReplyTo = process.env.RESEND_REPLY_TO;

const isValidEmail = (email) => /\S+@\S+\.\S+/.test(email);
const escapeHtml = (value) => value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

if (!resendApiKey) {
    console.warn('RESEND_API_KEY not set. /api/subscribe will return 500.');
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/styles', express.static(path.join(__dirname, 'styles')));
app.use('/scripts', express.static(path.join(__dirname, 'scripts')));
app.use('/images', express.static(path.join(__dirname, 'images')));
app.get('/favicon.ico', (req, res) => {
    res.sendFile(path.join(__dirname, 'favicon.ico'));
});

app.get('/health', (req, res) => {
    res.json({ ok: true });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

const subscribeHandler = async (req, res) => {
    const email = String(req.body?.email || '').trim();

    if (!isValidEmail(email)) {
        return res.status(400).json({ ok: false, error: 'Invalid email address.' });
    }

    if (!resendApiKey) {
        return res.status(500).json({ ok: false, error: 'Email service not configured.' });
    }

    const payload = {
        from: resendFrom,
        to: resendNotifyTo,
        subject: 'New Sociail Assistant interest',
        text: `New signup: ${email}`,
        html: `<p><strong>New signup:</strong> ${escapeHtml(email)}</p>`
    };

    if (resendReplyTo) {
        payload.reply_to = resendReplyTo;
    }

    try {
        const response = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${resendApiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            let message = 'Failed to send email.';
            try {
                const data = await response.json();
                if (data?.message) {
                    message = data.message;
                }
            } catch {
                const errorText = await response.text();
                if (errorText) {
                    message = errorText;
                }
            }
            console.error('Resend error:', response.status, message);
            return res.status(502).json({ ok: false, error: message });
        }

        return res.json({ ok: true });
    } catch (error) {
        console.error('Resend request failed:', error);
        return res.status(502).json({ ok: false, error: error?.message || 'Failed to send email.' });
    }
};

app.post('/api/subscribe', subscribeHandler);

app.use((req, res) => {
    res.status(404).send('Not found');
});

if (require.main === module) {
    app.listen(port, () => {
        console.log(`Server running on http://localhost:${port}`);
    });
}

module.exports = { app, subscribeHandler };
