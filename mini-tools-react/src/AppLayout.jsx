import React, { useState } from 'react';
import logo from './assets/musicadmin-logo.png';

export default function AppLayout({ children }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Header */}
      <header className="bg-[#F5F5F5] sticky top-0 z-50 text-base lg:text-lg">
        <div className="max-w-[1440px] mx-auto py-6 flex justify-between items-center">
          <a href="https://www.musicadmin.com/" className="flex items-center space-x-2">
            <img src={logo} alt="Music Admin" className="h-18 w-auto" />
          </a>

          {/* Desktop Nav */}
          <nav className="space-x-10 hidden md:flex items-center">
            <a href="https://www.musicadmin.com/services/" className="text-black">Services</a>
            <a href="https://www.musicadmin.com/news/" className="text-black">News</a>
            <a href="https://www.musicadmin.com/about/" className="text-black">About</a>
            <a href="https://www.musicadmin.com/tools/" className="text-black">Tools</a>
            <a href="https://www.musicadmin.com/get-started/" className="bg-black text-white text-base px-6 py-2 rounded-full hover:opacity-90">
              Get Started
            </a>
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden focus:outline-none"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <svg
              className="w-7 h-7 text-gray-700"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              {menuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Nav Menu */}
        {menuOpen && (
          <div className="md:hidden px-6 pb-4 space-y-3 bg-white shadow text-base">
            <a href="https://www.musicadmin.com/services/" className="block text-gray-700 hover:text-black">Services</a>
            <a href="https://www.musicadmin.com/about/" className="block text-gray-700 hover:text-black">About</a>
            <a href="https://www.musicadmin.com/contact/" className="block text-gray-700 hover:text-black">Contact</a>
            <a href="https://www.musicadmin.com/tools/" className="block text-gray-700 hover:text-black">Tools</a>
            <a
              href="https://www.musicadmin.com/get-started/"
              className="block bg-black text-white text-center py-2 rounded-full hover:opacity-90"
            >
              Get Started
            </a>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-[#191B20] text-white text-base px-6 py-24">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 items-start">
          {/* Newsletter Section */}
          <div>
            <h2 className="text-xl font-semibold mb-5">Stay Updated with Our Newsletter</h2>
            <form
              id="newsletterForm"
              method="POST"
              action="https://app.kit.com/forms/7617675/subscriptions/"
              className="max-w-md"
            >
              <div className="flex flex-col sm:flex-row gap-2 mb-2">
                <input
                  className="w-full border-b border-white bg-transparent text-white text-lg placeholder-gray-400 px-0 py-2 focus:outline-none focus:border-white transition"
                  type="email"
                  name="email_address"
                  placeholder="Email address"
                  required
                />
                <button
                  className="bg-white text-black text-lg px-5 py-2 rounded-full hover:opacity-90"
                  type="submit"
                >
                  Subscribe
                </button>
              </div>
              <p className="text-gray-400 text-sm">We value your privacy. No spam, ever.</p>
            </form>
          </div>

          {/* Mailing Address */}
          <div className="text-right">
            <h3 className="text-md font-semibold mb-5">Mailing Address</h3>
            <p className='text-gray-400'>2006 Acklen Ave., #120071<br />Nashville, TN 37212</p>
          </div>

          {/* Contact Info */}
          <div className="text-right">
            <h3 className="text-md font-semibold mb-5">Contact Us</h3>
            <p>Email: <a href="mailto:hello@musicadmin.com" className="text-blue-400 hover:underline">hello@musicadmin.com</a></p>
            <p className="text-gray-400">Phone: 615-200-0122</p>
          </div>
        </div>

        {/* Copyright */}
        <div className="text-center mt-12 text-gray-400 text-md">
          <p>&copy; Music Admin, Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}