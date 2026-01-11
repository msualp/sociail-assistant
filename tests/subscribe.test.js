const assert = require('node:assert');
const test = require('node:test');

// Set env before importing the handler
process.env.RESEND_API_KEY = 'test_key';
process.env.RESEND_FROM = 'Sociail Assistant <onboarding@resend.dev>';
process.env.RESEND_REPLY_TO = 'reply@example.com';

const { subscribeHandler } = require('../server');

const nativeFetch = globalThis.fetch;

const createMockRes = () => {
    const res = {
        statusCode: 200,
        body: null
    };
    res.status = (code) => {
        res.statusCode = code;
        return res;
    };
    res.json = (payload) => {
        res.body = payload;
        return res;
    };
    return res;
};

test('rejects invalid email without calling Resend', async (t) => {
    t.after(() => {
        globalThis.fetch = nativeFetch;
    });

    globalThis.fetch = () => {
        assert.fail('Resend should not be called for invalid email');
    };

    const req = { body: { email: 'not-an-email', plan: 'USB-C Only' } };
    const res = createMockRes();

    await subscribeHandler(req, res);

    assert.strictEqual(res.statusCode, 400);
    assert.deepStrictEqual(res.body, { ok: false, error: 'Invalid email address.' });
});

test('sends payload to Resend with reply-to when email is valid', async (t) => {
    let resendPayload;

    t.after(() => {
        globalThis.fetch = nativeFetch;
    });

    globalThis.fetch = async (_url, options) => {
        resendPayload = JSON.parse(options.body);
        return {
            ok: true,
            json: async () => ({ id: 'test-id' }),
            status: 200
        };
    };

    const req = { body: { email: 'user@example.com', plan: 'Full Battery' } };
    const res = createMockRes();

    await subscribeHandler(req, res);

    assert.strictEqual(res.statusCode, 200);
    assert.deepStrictEqual(res.body, { ok: true });
    assert.ok(resendPayload);
    assert.strictEqual(resendPayload.reply_to, 'reply@example.com');
    assert.ok(resendPayload.text.includes('user@example.com'));
    assert.ok(resendPayload.text.includes('Full Battery'));
});
