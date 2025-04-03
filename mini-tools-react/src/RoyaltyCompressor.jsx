import { useEffect, useState, useCallback } from "react";
import { CloudUpload, Download, Loader2 } from "lucide-react";
import { useDropzone } from "react-dropzone";
import toast, { Toaster } from "react-hot-toast";
import { v4 as uuidv4 } from "uuid"; // for anonymous session ID

import { createSession, trackUsage, getSessionData } from "./api/sessionManager";
import { uploadFile } from "./api/fileManager";
import { compressRoyaltyReport } from "./api/royaltyCompressor";
import { countTodayCompressions } from "./utils/sessionUtils";

const DAILY_LIMIT = 5;

export default function RoyaltyCompressor() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [filename, setFilename] = useState("");
  const [compressionsToday, setCompressionsToday] = useState(0);

  async function fetchCompressionCount(sessionId) {
    try {
      const res = await getSessionData(sessionId);
      const logs = res.data.usage_logs || [];
      const count = countTodayCompressions(logs);
      setCompressionsToday(count);
    } catch (err) {
      console.warn("Could not fetch compression count", err);
    }
  }

  useEffect(() => {
    const existing = localStorage.getItem("session_id");
  
    if (!existing) {
      createSession({ user_agent: navigator.userAgent }).then((res) => {
        const id = res.data.session_id;
        localStorage.setItem("session_id", id);
        fetchCompressionCount(id);
      });
    } else {
      fetchCompressionCount(existing);
    }
  }, []);

  useEffect(() => {
    return () => {
      if (downloadUrl) {
        URL.revokeObjectURL(downloadUrl);
      }
    };
  }, [downloadUrl]);

  const MAX_FILE_SIZE = 524288000; // 500MB in bytes

  const onDrop = useCallback((acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    if (!selectedFile) return;

    if (selectedFile.type !== "text/csv") {
      toast.error("Only CSV files are supported.");
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      toast.error("File is too large. 500MB max.");
      return;
    }

    setFile(selectedFile);
    setDownloadUrl(null);
    setFilename(`COMPRESSED_${selectedFile.name}`);
    toast.success("File added successfully!");
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/csv": [".csv"] },
    multiple: false,
    disabled: loading || compressionsToday >= DAILY_LIMIT,
  });

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a file first.");
      return;
    }
  
    setLoading(true);
    toast.loading("Uploading...");
  
    try {
      // 1. Upload file to S3
      const uploadRes = await uploadFile(file);
      const s3Key = uploadRes.data.key;
  
      // 2. Compress the file
      const compressRes = await compressRoyaltyReport(s3Key);
      const { download_url, output_key, input_key } = compressRes.data;
  
      // 3. Track usage
      const sessionId =
        localStorage.getItem("session_id") || uuidv4(); // basic anon session
      localStorage.setItem("session_id", sessionId);
  
      await trackUsage(sessionId, {
        tool_name: "Royalty Compressor",
        action: "compress",
        details: { input_key, output_key },
      });
  
      // 4. Prepare download
      setDownloadUrl(download_url);
      setFilename(`COMPRESSED_${file.name}`);

      setCompressionsToday((prev) => prev + 1);
  
      toast.dismiss();
      toast.success("File compressed successfully!");
    } catch (error) {
      console.error("Upload failed", error);
      toast.dismiss();
      toast.error("Something went wrong. Check console.");
    }
  
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#F5F5F5]">
      <Toaster position="top-center" />
      <div className="max-w-5xl mx-auto py-12 px-4 space-y-10">
        {/* Main Upload Card */}
        <div className="bg-white p-8 rounded-2xl shadow-md space-y-6">
          <h1 className="text-3xl font-bold text-center text-gray-900">
            Royalty Report Compressor
          </h1>
          <p className="text-center text-gray-600 text-base">
            Drop your YouTube raw financial reports and get them compressed in seconds.
          </p>

          {/* Drag & Drop Upload */}
          <div
            {...getRootProps()}
            className={`relative flex flex-col items-center justify-center w-full border-2 border-dashed rounded-lg p-6 cursor-pointer transition-all ${
              isDragActive
                ? "border-black bg-gray-50"
                : "border-gray-300 hover:border-gray-500"
            }`}
          >
            <input {...getInputProps()} />
            <CloudUpload className="w-12 h-12 text-gray-600 mb-3" />
            <p className="text-sm text-gray-700 text-center">
              {file
                ? file.name
                : isDragActive
                ? "Drop the file here..."
                : "Drag and drop or click to upload a CSV file"}
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Max file size: 500MB. CSV format only.
            </p>
          </div>

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={loading || !file || compressionsToday >= DAILY_LIMIT}
            className={`w-full py-3 rounded-full font-medium transition flex items-center justify-center gap-2 ${
              compressionsToday >= DAILY_LIMIT
                ? "bg-gray-400 cursor-not-allowed text-white"
                : "bg-black text-white hover:opacity-90"
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <CloudUpload className="w-5 h-5" />
                Upload & Compress
              </>
            )}
          </button>

          {/* Download Button */}
          {downloadUrl && (
            <button
              onClick={() => {
                const link = document.createElement("a");
                link.href = downloadUrl;
                link.download = filename;
                link.click();
              }}
              className="w-full mt-2 text-center bg-black text-white py-3 rounded-full font-medium hover:opacity-90 transition flex items-center justify-center gap-2"
            >
              <Download className="w-5 h-5" />
              Download your compressed report!
            </button>
          )}

          <p
            className={`text-sm text-center ${
              compressionsToday >= 10 ? "text-red-600" : "text-gray-500"
            }`}
          >
            {compressionsToday} of 10 compressions used today
          </p>
        </div>

        {/* About Section */}
        <div className="bg-white p-8 rounded-2xl shadow-md text-base text-gray-700 space-y-4">
          <h2 className="text-2xl font-bold text-gray-900 text-center">
            About This Tool
          </h2>
          <p>
            This compressor simplifies your financial data by minimizing bulky raw CSV files pulled from YouTube. It reduces file size for faster loading, easier readability, and smooth ingestion into platforms like Music Maestro or any custom reporting tool you use.
          </p>
          <ul className="list-disc list-inside space-y-1">
            <li>One-click CSV upload</li>
            <li>Instant download of compressed output</li>
            <li>No logins or signups required</li>
          </ul>
          <p className="text-xs text-gray-400 text-center">
            DISCLAIMER: We only process your file to deliver results — we don’t store, access, or use your data for any other purpose.
          </p>
        </div>

        {/* CTA Section */}
        <div className="w-full py-12 px-4 bg-[#F5F5F5] text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            Need Help Collecting Your Royalties?
          </h3>
          <p className="text-base text-gray-700 max-w-5xl mx-auto mb-6">
            Let our royalty experts track down every penny you’re owed — from YouTube, streaming platforms, and beyond. Focus on what you do best and we'll handle the rest.
          </p>
          <a
            href="https://www.musicadmin.com/get-started/"
            className="inline-block bg-black text-white px-6 py-3 rounded-full font-medium hover:opacity-90 transition"
          >
            Get Started
          </a>
        </div>
      </div>
    </div>
  );
}
