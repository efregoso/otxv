interface GlossaryTerm {
    word: string;
    meaning: string;
}

export const GLOSSARY_TERMS = [
    {
        word: 'CTI',
        meaning: 'cyber threat indicators.  Any data that indicates potential malicious cyber activities.',
    },
    {
        word: 'domain',
        meaning: 'a standard web address, typically ending in .com, .net, .org, and .edu, among others.',
    },
    {
        word: 'URL',
        meaning: 'uniform resource locator.  A complete web address, including the protocol (http/https), domain, and any additional pathing information.',
    },
    {
        word: 'IP address',
        meaning: 'a decimal-separated numerical address assigned to acting systems on the internet to uniquely identify them.',
    },
    {
        word: 'port',
        meaning: 'a numerical identifier assigned to specific services running on a system.  Common ports include 80 (HTTP), 443 (HTTPS), and 22 (SSH).',
    },
    {
        word: 'ASN',
        meaning: 'autonomous system number.  A uniquely-assigned number allowing a system to broadcast its presence to other systems.',
    },
    {
        word: 'IOC',
        meaning: 'indicators of compromise.  Data that points to potentially malicious activity on a network system.',
    },
    {
        word: 'STIX',
        meaning: 'Structured Threat Indication Expression.  A language designed specifically for communication of CTI.',
    },
    {
        word: 'TAXII',
        meaning: 'Trusted Automated Exchange of Indicator Information. A transport protocol designed specifically for the communication of CTI over a network.',
    },
    {
        word: 'IDS',
        meaning: 'Intrusion Detection system.  An automated system built to detect when another system has been or is actively being compromised, usually by malicious actors on the internet.',
    },
];

export const ORDERED_GLOSSARY_TERMS = GLOSSARY_TERMS.sort((a, b) => a.word.localeCompare(b.word));