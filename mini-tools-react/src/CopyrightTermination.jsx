import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

export default function CopyrightTermination() {
  const [grantDate, setGrantDate] = useState('');
  const [terminationPeriod, setTerminationPeriod] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openFaq, setOpenFaq] = useState(null);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };
  
  function calculateTermination(grantDateStr, includesPublicationRight) {
    const grantDate = new Date(grantDateStr);
  
    const terminationStart = new Date(grantDate);
    terminationStart.setFullYear(terminationStart.getFullYear() + 35);
  
    const terminationEnd = includesPublicationRight
      ? new Date(grantDateStr).setFullYear(new Date(grantDateStr).getFullYear() + 40)
      : new Date(terminationStart).setFullYear(terminationStart.getFullYear() + 5);
  
    const noticeStart = new Date(terminationStart);
    noticeStart.setFullYear(noticeStart.getFullYear() - 10);
  
    const noticeEnd = new Date(terminationEnd);
    noticeEnd.setFullYear(noticeEnd.getFullYear() - 2);
  
    const today = new Date();
    let status = '';
  
    if (today > terminationEnd) {
      status = 'expired';
    } else if (today < noticeStart) {
      status = 'too_early';
    } else if (today >= noticeStart && today <= noticeEnd) {
      status = 'can_serve';
    } else {
      status = 'outside_notice_window';
    }
  
    return {
      termination_start: new Date(terminationStart).toISOString().split('T')[0],
      termination_end: new Date(terminationEnd).toISOString().split('T')[0],
      notice_start: new Date(noticeStart).toISOString().split('T')[0],
      notice_end: new Date(noticeEnd).toISOString().split('T')[0],
      status
    };
  }  

  const handleCalculate = () => {
    setLoading(true);
    const data = calculateTermination(grantDate, true); // plug in checkbox state if needed
    setTerminationPeriod(data);
    setLoading(false);
  };  

  const sectionInfo = grantDate
  ? new Date(grantDate) < new Date('1978-01-01')
    ? { label: 'Section 304', description: 'Works published before January 1, 1978' }
    : { label: 'Section 203', description: 'Works published on or after January 1, 1978' }
  : null;

  const faqList = [
    {
      q: 'Can I terminate a work-for-hire?',
      a: 'No, works created as "work-for-hire" are generally not eligible for termination.'
    },
    {
      q: 'Can termination rights be waived?',
      a: 'No, termination rights cannot be waived or assigned in advance.'
    },
    {
      q: 'What if I missed my window?',
      a: 'If your termination window has passed, you cannot reclaim rights under current law.'
    },
    {
      q: 'What about multiple authors?',
      a: 'Termination requires agreement from a majority of authors or their heirs.'
    },
    {
      q: 'Do I need a lawyer?',
      a: 'Legal guidance isn’t mandatory but strongly recommended to ensure proper procedures are followed.'
    },
    {
      q: 'Can heirs terminate?',
      a: 'Yes. If the author is deceased, statutory heirs such as a spouse, children, or grandchildren may terminate.'
    },
    {
      q: 'What about international rights?',
      a: 'U.S. termination laws apply only within the U.S.'
    },
    {
      q: 'Is termination automatic?',
      a: 'No, you must actively serve a valid termination notice.'
    },
    {
      q: 'What about derivative works?',
      a: 'Pre-existing derivative works may continue to be exploited under the original terms.'
    },
    {
      q: 'Does termination affect copyright duration?',
      a: 'No, termination does not extend or shorten the original copyright duration.'
    },
    {
      q: 'How precise must the notice be?',
      a: 'Notices must precisely specify the work, dates, and termination details; inaccuracies may invalidate the notice.'
    },
    {
      q: 'Can I serve notice electronically?',
      a: 'No, it must be served via certified mail or courier to ensure legal compliance.'
    }
  ];

  return (
    <div className="min-h-screen bg-[#F5F5F5]">
      <div className="max-w-5xl mx-auto space-y-10 py-10 px-4">
        {/* Calculator Section */}
        <div className="bg-white p-8 rounded-2xl shadow-md space-y-6">
          <h1 className="text-3xl font-bold text-center text-gray-800">Copyright Termination Eligibility</h1>
          <p className="text-center text-gray-600">Check your U.S. copyright termination rights under Sections 304 & 203</p>

          <label className="block text-sm font-medium text-gray-700">Enter Album/Song Release Date:</label>
          <input
            type="date"
            value={grantDate}
            onChange={(e) => setGrantDate(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-lg"
          />
          <p className="text-xs text-gray-500">Enter the original release date of your copyrighted work.</p>

          <button
            onClick={handleCalculate}
            className="w-full bg-black text-white py-2 rounded-full hover:opacity-90 hover:cursor-pointer transition"
          >
            {loading ? 'Checking...' : 'Check Eligibility'}
          </button>

          {terminationPeriod && (
            <div className="bg-white p-6 rounded-2xl shadow space-y-6 border border-gray-200">
              {/* Header: Status */}
              <div className="flex items-center gap-2">
                <div className={`h-3 w-3 rounded-full ${
                    terminationPeriod.status === 'can_serve'
                      ? 'bg-green-500'
                      : terminationPeriod.status === 'too_early'
                      ? 'bg-yellow-400'
                      : terminationPeriod.status === 'expired'
                      ? 'bg-red-500'
                      : 'bg-gray-400'
                  }`}
                />
                <h2 className="text-lg font-semibold text-gray-900">
                  {terminationPeriod.status === 'can_serve' && 'Can Serve Notice Now'}
                  {terminationPeriod.status === 'too_early' && 'Cannot Serve Notice Yet'}
                  {terminationPeriod.status === 'expired' && 'Termination Right Expired'}
                  {terminationPeriod.status === 'outside_notice_window' && 'Outside Notice Window'}
                </h2>
              </div>

              {/* Status Message */}
              {terminationPeriod.status === 'can_serve' && (
                <div className="bg-green-100 text-green-800 text-sm rounded-lg p-4 border border-green-300">
                  You can serve termination notice now. If you serve notice today, you can choose any termination date between <strong>{formatDate(terminationPeriod.termination_start)}</strong> and <strong>{formatDate(terminationPeriod.termination_end)}</strong>.
                </div>
              )}
              {terminationPeriod.status === 'too_early' && (
                <div className="bg-yellow-50 text-yellow-800 text-sm rounded-lg p-4 border border-yellow-200">
                  You cannot serve termination notice yet. The earliest date you can serve notice is <strong>{formatDate(terminationPeriod.notice_start)}</strong>.
                </div>
              )}
              {terminationPeriod.status === 'expired' && (
                <div className="bg-red-100 text-red-800 text-sm rounded-lg p-4 border border-red-300">
                  Your termination window has expired. Unfortunately, you can no longer exercise your termination right for this work.
                </div>
              )}
              {terminationPeriod.status === 'outside_notice_window' && (
                <div className="bg-yellow-100 text-yellow-800 text-sm rounded-lg p-4 border border-yellow-300">
                  You're outside the notice window for this termination period.
                </div>
              )}

              {/* Section badge */}
              <div className="flex items-center gap-3">
                <span className="bg-blue-100 text-blue-600 text-sm px-3 py-1 rounded-full font-semibold">
                  {sectionInfo.label}
                </span>
                <span className="text-sm text-gray-500">{sectionInfo.description}</span>
              </div>

              {/* Termination Window */}
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-1">Termination Window</h3>
                <div className="border border-gray-200 rounded-lg p-3 text-sm text-gray-700 bg-gray-50">
                  {formatDate(terminationPeriod.termination_start)} <span className="text-gray-400">to</span> {formatDate(terminationPeriod.termination_end)}
                </div>
              </div>

              {/* Notice Requirements */}
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-2">Notice Period Requirements</h3>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-2 text-sm text-gray-700">
                  <p>You must serve notice 2–10 years before your chosen termination date.</p>
                  <p>
                    For this work, you can serve notice between:<br />
                    <strong>{formatDate(terminationPeriod.notice_start)} — {formatDate(terminationPeriod.notice_end)}</strong>
                  </p>

                  {terminationPeriod.status === 'can_serve' && (
                    <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3 text-blue-800">
                      <p className="mb-1">
                        <strong>If you serve notice today</strong>, your possible termination dates would be:<br />
                        <strong>{formatDate(terminationPeriod.termination_start)} — {formatDate(terminationPeriod.termination_end)}</strong>
                      </p>
                      <p className="text-xs text-blue-700">You can choose any specific date within this range as your termination date.</p>
                    </div>
                  )}
                </div>
              </div>

              {/* CTA */}
              {terminationPeriod.status && (
                <div className="pt-2">
                  {terminationPeriod.status === 'can_serve' && (
                    <a
                      href="https://www.musicadmin.com/get-started/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block w-full text-center bg-black text-white py-2 rounded-full font-medium hover:opacity-90 transition"
                    >
                      Contact Us
                    </a>
                  )}

                  {(terminationPeriod.status === 'expired' || terminationPeriod.status === 'outside_notice_window') && (
                    <a
                      href="https://www.musicadmin.com/get-started/"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block w-full text-center bg-black text-white py-2 rounded-full font-medium hover:opacity-90 transition"
                    >
                      Explore Other Options
                    </a>
                  )}

                  {terminationPeriod.status === 'too_early' && (
                    <a
                      href="https://calendar.google.com/calendar/r/eventedit"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block w-full text-center bg-black text-white py-2 rounded-full font-medium hover:opacity-90 transition"
                    >
                      Set Calendar Reminder
                    </a>
                  )}
                </div>
              )}
              </div>
            )}
        </div>

        {/* Comprehensive Guide Section */}
        <div className="bg-white p-8 rounded-2xl shadow-md space-y-6 text-black">
          <h2 className="text-2xl font-bold text-center">Comprehensive Guide to Copyright Terminations Under Sections 203 and 304</h2>
          <p>Understanding your right to terminate previously granted copyrights can dramatically impact your control over creative works. Whether you're an artist, songwriter, heir, or rights holder, knowing when and how to reclaim your copyrights is crucial.</p>
          <p>This guide provides clear, actionable information to help you determine eligibility under Sections 203 and 304 of the U.S. Copyright Act.</p>

          <h3 className="text-xl font-semibold">What Are Copyright Terminations?</h3>
          <p>Copyright termination rights empower creators or their heirs to reclaim rights previously transferred to publishers, labels, or other entities. These rights allow renegotiation or new opportunities to monetize your work.</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-gray-100 p-4 rounded-xl bg-white">
              <h3 className="text-xl font-semibold mb-2 text-black">Section 203</h3>
              <p><strong>Applies To:</strong> Works published on or after January 1, 1978.</p>
              <p><strong>Termination Window:</strong> Opens 35 years after publication and lasts for 5 years.</p>
              <p><strong>Notice Serving Period:</strong> Notice must be served 2 to 10 years prior to your chosen termination date.</p>
              <br /><hr className='text-gray-100' /><br />
              <p className='mb-2'><strong>Example:</strong></p>
              <p><strong>Original Release Date:</strong> January 1, 1990</p>
              <p><strong>Termination Window:</strong> January 1, 2025 – January 1, 2030</p>
              <p><strong>Serve Notice Between:</strong> January 1, 2015 – January 1, 2028</p>
            </div>
            <div className="border border-gray-100 p-4 rounded-xl bg-white">
              <h3 className="text-xl font-semibold mb-2 text-black">Section 304</h3>
              <p><strong>Applies To:</strong> Works published before January 1, 1978.</p>
              <p><strong>Termination Windows:</strong></p>
              <ul className="list-disc list-inside">
                <li>First Window: Opens 56 years after initial copyright and lasts for 5 years.</li>
                <li>Second Window: Opens 75 years after initial copyright and lasts for 5 years.</li>
              </ul>
              <p><strong>Notice Serving Period:</strong> Notice must be served between 2 to 10 years before the desired termination date.</p>
              <br /><hr className='text-gray-100' /><br />
              <p className='mb-2'><strong>Example:</strong></p>
              <p><strong>Original Release Date:</strong> January 1, 1965</p>
              <p><strong>First Termination Window:</strong> January 1, 2021 – January 1, 2026</p>
              <p><strong>Serve Notice Between:</strong> January 1, 2011 – January 1, 2024</p>
            </div>
          </div>

          <h3 className="text-xl font-semibold">How to Serve a Termination Notice</h3>
          <ol className="list-decimal list-inside space-y-2">
            <li>Identify your termination window based on your work's release date.</li>
            <li>Calculate the notice-serving period (between 2-10 years before your intended termination date).</li>
            <li>Prepare a formal written notice detailing:
              <ul className="list-disc list-inside ml-4">
                <li>Work Title</li>
                <li>Original Publication Date</li>
                <li>Specific Termination Date</li>
                <li>Names and Addresses of Rights Holders</li>
              </ul>
            </li>
            <li>Deliver the notice via certified mail or courier with return receipt.</li>
          </ol>

          <h3 className="text-xl font-semibold">What Happens After Serving Notice?</h3>
          <p>Once notice is served, rights revert to the original author or heirs on the chosen termination date. It's then possible to negotiate new deals or licensing arrangements at current market rates.</p>
        </div>

        {/* FAQ Section */}
        <div className="bg-white p-6 rounded-2xl shadow-md space-y-4">
          <h2 className="text-2xl font-bold text-black text-center">Frequently Asked Questions</h2>
          {faqList.map((item, index) => (
            <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
              <button
                onClick={() => setOpenFaq(openFaq === index ? null : index)}
                className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition"
              >
                <span className="text-base font-medium text-black">{item.q}</span>
                {openFaq === index ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
              </button>
              {openFaq === index && (
                <div className="px-4 pb-4 text-gray-700 text-sm">
                  {item.a}
                </div>
              )}
            </div>
          ))}
        </div>

        <p className="text-xs text-gray-400 text-center mt-10">This application is for informational purposes only and does not constitute legal advice.</p>
      </div>

      {/* CTA Section */}
      <div className="w-full bg-[#F5F5F5] py-16 px-4">
        <div className="max-w-5xl mx-auto text-center space-y-6">
          <h3 className="text-3xl font-semibold text-black">Need personalized guidance?</h3>
          <p className="text-lg text-black max-w-5xl mx-auto">
            Understanding copyright terminations can empower you financially and creatively. Our experts can help you navigate the process and maximize your rights.
            Get started today for a consultation about your specific situation.
          </p>
          <a
            href="https://www.musicadmin.com/get-started/"
            className="inline-block bg-black text-white px-6 py-3 rounded-full text-base font-semibold hover:opacity-90 transition"
          >
            Get Started
          </a>
        </div>
      </div>
    </div>
  );
}
