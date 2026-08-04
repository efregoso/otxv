import { NAV_LINKS, HOME_LINK } from "./nav_links";
import './navigation_bar.css';

export default function NavigationBar() {
    return (
        <div className="nav-bar-container">
            <nav className="nav-element">
                <a id="home-link" href={HOME_LINK.href}>
                    {HOME_LINK.label}
                </a>
                { NAV_LINKS.map((link) => (
                    <a key={link.href} href={link.href}>
                        {link.label}
                    </a>
                ))}
            </nav>
        </div>
    );
}