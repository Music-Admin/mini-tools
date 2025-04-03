import { Link } from "react-router-dom";
import { FileText, FileQuestion } from "lucide-react";

const tools = [
  {
    name: "Royalty Compressor",
    description:
      "Compress bulky YouTube royalty reports into lightweight, structured CSVs optimized for ingestion into Music Maestro.",
    path: "/tools/royalty-compressor",
    icon: FileText,
  },
  {
    name: "Coming Soon",
    description:
      "Stay tuned to see what's next.",
    path: "/tools/",
    icon: FileQuestion,
  },
  // Future tools can be added here
];

export default function ToolsDashboard() {
  return (<>
    <div className="bg-[#F5F5F5] pt-20 pb-28 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Music Admin Tools
          </h1>
          <p className="text-black max-w-4xl mx-auto text-lg">
            Streamline your workflows with our collection of mini tools.
            Start below by selecting the tool you need.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {tools.map((tool) => {
            const Icon = tool.icon;
            return (
              <Link
                to={tool.path}
                key={tool.name}
                className="group bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-xl transition duration-200 ease-in-out"
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="bg-black text-white p-3 rounded-lg">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h2 className="text-xl font-semibold text-gray-900 group-hover:underline">
                    {tool.name}
                  </h2>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {tool.description}
                </p>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
    {/* CTA Section */}
    <div className="w-full py-20 px-4 bg-[#F5F5F5] text-center">
      <h3 className="text-4xl font-semibold text-black mb-2">
        Schedule a consultation today.
      </h3>
      <p className="text-xl text-black max-w-4xl mx-auto mb-8">
        Join thousands of songwriters, publishers, artists, labels, and their representatives who trust <br />Music Admin to streamline their rights and royalties.
      </p>
      <a
        href="https://www.musicadmin.com/get-started/"
        className="inline-block bg-black text-white px-8 py-3 rounded-full text-2xl font-medium hover:opacity-90 transition"
      >
        Get Started
      </a>
    </div>
  </>);
}
