import Image from "next/image";
import NavigationBar from "./common/navigation_bar/navigation_bar";
import "./globals.css"

export default function Home() {
  return (
    <div id="app-container">
      <div id="app-header">
        <NavigationBar />
      </div>
      <div id="app-body">
          <h1 id="welcome-header">Welcome to OTX-V.</h1>
          <p id="welcome-paragraph">
            Welcome to OTX-V, a visualization &amp; statistical tool for AlienVault's Open Threat Exchange 
            &amp; textual artifacts.
          </p>
      </div>
    </div>
);
}
