'use client';

import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import './port_checker.css';

export default function PortCheckerPage() {
    const [domain, setDomain] = useState('');
    const [pingTimes, setPingTimes] = useState(0);

    const handleSubmit = () => {
        console.log(`Submitted domain: ${domain}`);
        console.log(`Number of ping times: ${pingTimes}`);
    };

    return (
        <div className="port-checker-content-container">
            <h1>Port Checker</h1>
            <Stack className="port-checker-form-stack" direction="row" spacing={2}>
                <TextField
                    required
                    id="port-checker-domain-input"
                    label="Domain to port-check"
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                />
                <TextField
                    required
                    id="port-checker-ping-times-input"
                    label="Number of times to ping"
                    value={pingTimes}
                    onChange={(e) => setPingTimes(Number(e.target.value))}
                />
                <Button variant="contained" onClick={handleSubmit}>
                    Submit
                </Button>
            </Stack>
        </div>
    );
}