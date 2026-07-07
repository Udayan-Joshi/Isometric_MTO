import csv
import io

from app.models.mto import MTOResponse


def generate_csv(mto: MTOResponse) -> str:
    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            "Item",
            "Category",
            "Description",
            "Size",
            "Schedule",
            "Material",
            "End Type",
            "Quantity",
            "Unit",
            "Length (m)",
            "Confidence",
            "Remarks",
        ]
    )

    for item in mto.items:
        writer.writerow(
            [
                item.item_no,
                item.category,
                item.description,
                item.size_nps,
                item.schedule_rating,
                item.material_spec,
                item.end_type,
                item.quantity,
                item.unit,
                item.length_m,
                item.confidence,
                item.remarks,
            ]
        )

    return output.getvalue()