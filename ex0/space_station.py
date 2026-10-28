from datetime import datetime
from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validate")
    print("=" * 40)

    station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-10-20T10:30:00"),
            )

    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")

    status = "Operational" if station.is_operational else "Offline"
    print(f"Status: {status}")

    print("=" * 40)
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="ISS002",
            name="Invalid Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-10-20T10:30:00"),
        )
    except ValueError as error:
        print(error)
    # except ValueError as error:
        # for i in error.errors():
        # print(i["msg"])
