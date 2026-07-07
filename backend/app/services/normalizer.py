from app.models.mto import (
    DrawingMeta,
    MTOItem,
    MTOResponse,
    Summary,
)


def normalize_mto(raw: dict) -> MTOResponse:
    """
    Converts Gemini output into the application's
    MTOResponse schema.
    """

    drawing = raw.get("drawing_meta", {})

    summary = raw.get("summary", {})

    items = []

    for idx, item in enumerate(raw.get("items", []), start=1):

        category = item.get("category")

        if not category:
            category = item.get("type", "OTHER").upper()

        description = (
            item.get("description")
            or item.get("type")
            or "Unknown Item"
        )

        quantity = item.get("quantity", 1)

        unit = "EA"

        if category.upper() == "PIPE":
            unit = "M"

        items.append(
            MTOItem(
                item_no=idx,
                category=category.upper(),
                description=description,
                size_nps=item.get("size_nps"),
                schedule_rating=item.get("schedule_rating"),
                material_spec=item.get("material_spec"),
                end_type=item.get("end_type"),
                quantity=float(quantity),
                unit=unit,
                length_m=item.get("length_m"),
                confidence=item.get("confidence"),
                remarks=item.get("remarks", ""),
            )
        )

        if confidence is None:
            confidence = 0.80

    return MTOResponse(
        drawing_meta=DrawingMeta(**drawing),
        items=items,
        summary=Summary(**summary),
        mock=False,
    )