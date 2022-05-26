import './App.css';
import React from 'react';
import memuDisplaySettings from './assets/memu_display_settings.png';
import memuInstaceSettings from './assets/memu_instance_settings.png';
import memuAppearanceSettings from './assets/memu_appearance_settings.png';
import SourceBadge from './components/badge/SourceBadge';
import TestBadge from './components/badge/TestBadge';
import ReleaseLink from './components/release/ReleaseLink';
import ReleaseUpdate from './components/release/ReleaseUpdate';
import ReleaseDownloadCount from './components/release/ReleaseDownloadCount';
import {initializeGA} from './GoogleAnalytics';
import PyPiBadge from './components/badge/PyPiBadge';

/**
 * main app
 * @return {Component} App
 */
export default function App() {
  initializeGA();
  return (
    <div className="mume markdown-preview  ">
      <h1 className="mume-header" id="py-clash-bot">py-clash-bot</h1>
      <h2>
        <SourceBadge/>
        <PyPiBadge/>
        <TestBadge/>
      </h2>
      <p>A Clash Royale automation bot written in Python.</p>
      <h2 className="mume-header" id="install">Install</h2>

      <p>Choose one of the install methods below.</p>
      <h4 className="mume-header" id="a-windows-install">a. Windows Install</h4>
      <ReleaseLink />
      <p><ReleaseUpdate />
        with <ReleaseDownloadCount /> downloads.</p>
      <h4 className="mume-header" id="b-install-from-source">
        b. Install with pip
      </h4>

      <p>Enter the following into the command line:</p>
      <code>pip install py-clash-bot</code>

      <h2>MEmu Dependency</h2>
      <p>To emulate the game,
        <a href="https://www.memuplay.com/" rel="nofollow">
          Download and install MEmu
        </a>
        .
      </p>
      <h3>Configure MEmu</h3>
      <p>Using the Multiple Instance Manager, set the instance, display,
        and appearance settings of your instance to match the following</p>
      <p><img src={memuInstaceSettings}
        alt="MEmu instace options" /></p>
      <p><img src={memuDisplaySettings}
        alt="MEmu display options" /></p>
      <p><img src={memuAppearanceSettings}
        alt="MEmu appearance options" /></p>
      <p>
        Then start the emulator and install
        Clash Royale with the Google Play Store.
      </p>
      <h2>Run py-clash-bot</h2>
      <h4>a. Installed on Windows</h4>
      <p>Run the desktop shortcut the installer created.</p>
      <h4>b. Installed with pip</h4>
      <p>Enter <code>pyclashbot</code> in the command line.</p>

    </div>
  );
}