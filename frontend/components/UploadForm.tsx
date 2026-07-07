"use client";

import { useState } from "react";
import { MTOResponse } from "@/types/mto";

interface UploadFormProps {
  onSuccess: (result: MTOResponse, file: File) => void;
}

export default function UploadForm({ onSuccess }: UploadFormProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedTypes = [
      "image/png",
      "image/jpeg",
      "application/pdf",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Only PNG, JPG and PDF files are allowed.");
      setSelectedFile(null);
      return;
    }

    if (file.size > 20 * 1024 * 1024) {
      setError("Maximum file size is 20 MB.");
      setSelectedFile(null);
      return;
    }

    setError("");
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        "http://127.0.0.1:8000/api/extract",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed.");
      }

      const data: MTOResponse = await response.json();

      onSuccess(data, selectedFile);
    } catch (err) {
      console.error(err);
      setError("Unable to process the drawing.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-8 max-w-2xl mx-auto">

      <h2 className="text-2xl font-semibold mb-2">
        Upload Drawing
      </h2>

      <p className="text-gray-600 mb-6">
        Supported formats: PNG, JPG, PDF (Max 20 MB)
      </p>

      <input
        type="file"
        accept=".png,.jpg,.jpeg,.pdf"
        onChange={handleFileChange}
        className="block w-full border border-gray-300 rounded-lg p-3"
      />

      {selectedFile && (
        <div className="mt-4 rounded-lg bg-gray-100 p-3">
          <p className="text-sm">
            <strong>Selected File:</strong> {selectedFile.name}
          </p>
        </div>
      )}

      {error && (
        <div className="mt-4 rounded-lg bg-red-100 p-3">
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!selectedFile || loading}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-medium transition"
      >
        {loading ? "Processing..." : "Extract MTO"}
      </button>

    </div>
  );
}