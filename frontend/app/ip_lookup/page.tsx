'use client';

import { useState, useEffect } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import './ip_lookup.css'

export default function IpLookupPage() {

    const [ipAddress, setIpAddress] = useState("");
    const [dnsResult, setDnsResult] = useState("");

    const handleSubmit = () => {
        console.log(`Submitted IP address: ${ipAddress}`);
    };

    useEffect(() => {
        if (dnsResult) {
            console.log(`DNS Result: ${dnsResult}`);
        }
    }, [dnsResult]);

    return (
        <div id="ip-lookup-content-container">
            <h1>IP Address DNS Lookup</h1>
            <Stack className="ip-lookup-form-stack" direction="row" spacing={2}>
                <TextField
                    required
                    id="ip-address-input"
                    label="IPv4 or IPv6 address"
                    value={ipAddress}
                    onChange={(e) => setIpAddress(e.target.value)}
                />
                <Button variant="contained" onClick={handleSubmit}>
                    Submit
                </Button>
            </Stack>
        </div>
    );
}