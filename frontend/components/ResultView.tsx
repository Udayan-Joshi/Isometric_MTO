"use client";

import { MTOResponse } from "@/types/mto";
import SummaryCards from "./SummaryCards";
import MtoTable from "./MtoTable";

interface ResultViewProps {
  result: MTOResponse;
  file: File;
}

export default function ResultView({
  result,
  file,
}: ResultViewProps) {

  const imageUrl =
    file.type === "application/pdf"
      ? null
      : URL.createObjectURL(file);

  const meta = result.drawing_meta;

  return (
    <div className="mt-10">

      {/* Drawing + Metadata */}

      <div className="grid md:grid-cols-2 gap-6">

        {/* Preview */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold mb-4">
            Drawing Preview
          </h2>

          {imageUrl ? (
            <img
              src={imageUrl}
              alt="Uploaded Drawing"
              className="rounded-lg border max-h-[500px] object-contain w-full"
            />
          ) : (
            <div className="border rounded-lg h-80 flex items-center justify-center text-gray-500">
              PDF Preview Not Available
            </div>
          )}

        </div>

        {/* Metadata */}

        <div className="bg-white rounded-xl shadow p-6">

          <h2 className="text-xl font-semibold mb-4">
            Drawing Metadata
          </h2>

          <div className="space-y-3">

            <Metadata
              label="Drawing Number"
              value={meta.drawing_no}
            />

            <Metadata
              label="Revision"
              value={meta.revision}
            />

            <Metadata
              label="Line Number"
              value={meta.line_number}
            />

            <Metadata
              label="NPS"
              value={meta.nps}
            />

            <Metadata
              label="Material Class"
              value={meta.material_class}
            />

            <Metadata
              label="Service"
              value={meta.service}
            />

            <Metadata
              label="Pipeline"
              value={result.mock ? "Mock" : "Gemini AI"}
            />

          </div>

        </div>

      </div>

      {/* Summary */}

      <SummaryCards summary={result.summary} />

      {/* Table */}

      <div className="mt-8">

        <h2 className="text-2xl font-semibold mb-4">
          Material Take-Off
        </h2>

        <MtoTable items={result.items} />

      </div>

    </div>
  );
}

interface MetadataProps {
  label: string;
  value?: string | null;
}

function Metadata({
  label,
  value,
}: MetadataProps) {

  return (
    <div className="flex justify-between border-b pb-2">

      <span className="font-medium">
        {label}
      </span>

      <span className="text-gray-600">
        {value || "-"}
      </span>

    </div>
  );
}