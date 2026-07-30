interface NavLink {
  label: string;
  href: string;
  icon?: React.ReactNode;
}

export const NAV_LINKS: NavLink[] = [
  { label: "OTX-V", href: "index.html", icon: undefined },
  { label: "IP Lookup", href: "legacy/ip_lookup/iplookup.html", icon: undefined },
  { label: "Port Checker", href: "legacy/port_checker/portchecker.html", icon: undefined },
  { label: "STYLO", href: "legacy/stylometry/stylo.html", icon: undefined },
  { label: "Kibana", href: "http://localhost:32771/app/kibana", icon: undefined },
  { label: "Glossary", href: "legacy/glossary/glossary.html", icon: undefined }
];