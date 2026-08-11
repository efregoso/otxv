interface NavLink {
  label: string;
  href: string;
  icon?: React.ReactNode;
}

export const HOME_LINK = { label: "OTX-V", href: "/", icon: undefined };

export const NAV_LINKS: NavLink[] = [
  { label: "IP Lookup", href: "/ip_lookup", icon: undefined },
  { label: "Port Checker", href: "/port_checker", icon: undefined },
  { label: "STYLO", href: "/stylometry", icon: undefined },
  { label: "Kibana", href: "http://localhost:32771/app/kibana", icon: undefined },
  { label: "Glossary", href: "/glossary", icon: undefined }
];