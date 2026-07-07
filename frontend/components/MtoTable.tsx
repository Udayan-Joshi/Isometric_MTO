import { MTOItem } from "@/types/mto";

interface MtoTableProps {
  items: MTOItem[];
}

export default function MtoTable({
  items,
}: MtoTableProps) {
  return (
    <div className="bg-white rounded-lg shadow mt-8 overflow-x-auto">

      <table className="w-full text-sm">

        <thead className="bg-gray-100">

          <tr>
            <th className="p-3 text-left">Item</th>
            <th className="p-3 text-left">Category</th>
            <th className="p-3 text-left">Description</th>
            <th className="p-3 text-left">Size</th>
            <th className="p-3 text-left">Qty</th>
            <th className="p-3 text-left">Unit</th>
            <th className="p-3 text-left">Confidence</th>
          </tr>

        </thead>

        <tbody>

          {items.map((item) => (

            <tr
              key={item.item_no}
              className="border-t"
            >

              <td className="p-3">{item.item_no}</td>

              <td className="p-3">{item.category}</td>

              <td className="p-3">
                {item.description}
              </td>

              <td className="p-3">
                {item.size_nps || "-"}
              </td>

              <td className="p-3">
                {item.quantity}
              </td>

              <td className="p-3">
                {item.unit}
              </td>

              <td className="p-3">
                {item.confidence
                  ? `${(item.confidence * 100).toFixed(0)}%`
                  : "-"}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}