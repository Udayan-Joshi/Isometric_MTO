"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ResultView from "@/components/ResultView";
import { MTOResponse } from "@/types/mto";

export default function Home() {
  const [result, setResult] = useState<MTOResponse | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const handleSuccess = (
    data: MTOResponse,
    uploadedFile: File
  ) => {
    setResult(data);
    setFile(uploadedFile);
  };

  return (
    <main className="min-h-screen bg-gray-100 py-10">
      <div className="max-w-6xl mx-auto px-6">

        <h1 className="text-4xl font-bold text-center">
          Isometric MTO Extractor
        </h1>

        <p className="text-center text-gray-600 mt-3 mb-10">
          Upload a piping isometric drawing and generate a
          Material Take-Off (MTO).
        </p>

        <UploadForm onSuccess={handleSuccess} />

        {result && file && (
          <ResultView
            result={result}
            file={file}
          />
        )}

      </div>
    </main>
  );
}