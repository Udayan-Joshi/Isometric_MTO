import { Summary } from "@/types/mto";

interface SummaryCardsProps {
  summary: Summary;
}

export default function SummaryCards({
  summary,
}: SummaryCardsProps) {
  const cards = [
    {
      title: "Pipe Length",
      value: `${summary.total_pipe_length_m} m`,
    },
    {
      title: "Fittings",
      value: summary.fittings,
    },
    {
      title: "Flanges",
      value: summary.flanges,
    },
    {
      title: "Valves",
      value: summary.valves,
    },
    {
      title: "Gaskets",
      value: summary.gaskets,
    },
    {
      title: "Bolt Sets",
      value: summary.bolt_sets,
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 my-8">
      {cards.map((card) => (
        <div
          key={card.title}
          className="bg-white rounded-lg shadow p-5 text-center"
        >
          <p className="text-gray-500 text-sm">
            {card.title}
          </p>

          <h3 className="text-2xl font-bold mt-2">
            {card.value}
          </h3>
        </div>
      ))}
    </div>
  );
}