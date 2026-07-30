import { NAV_LINKS } from "./nav_links";

export default function NavigationBar() {
    return (
        <div id="top-nav-bar-container">
            <nav id="top-nav">
                { NAV_LINKS.map((link) => (
                    <a key={link.href} href={link.href}>
                        {link.label}
                    </a>
                ))}
            </nav>
        </div>
    );
}