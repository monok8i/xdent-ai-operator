"""Utility functions for the API endpoints."""

from typing import Any

from src.api.schemas import (
    MapLocationResponse,
    MapServiceBaseResponse,
    MapServiceListItemResponse,
)


def build_location_payload(location: Any) -> MapLocationResponse:
    return MapLocationResponse.model_validate(location, from_attributes=True)


def build_map_item_payload(record: Any) -> MapServiceListItemResponse:
    service_payload = MapServiceBaseResponse.model_validate(
        record.service, from_attributes=True
    ).model_dump()

    location = (
        build_location_payload(record.location) if record.location is not None else None
    )

    return MapServiceListItemResponse(
        **service_payload,
        locations_count=record.locations_count,
        target_groups_count=record.target_groups_count,
        distance_km=record.distance_km,
        location=location,
    )


def build_list_item_payload(record: Any) -> MapServiceListItemResponse:
    service_payload = MapServiceBaseResponse.model_validate(
        record.service, from_attributes=True
    ).model_dump()

    location = (
        build_location_payload(record.location) if record.location is not None else None
    )

    return MapServiceListItemResponse(
        **service_payload,
        locations_count=record.locations_count,
        target_groups_count=record.target_groups_count,
        distance_km=record.distance_km,
        location=location,
    )
