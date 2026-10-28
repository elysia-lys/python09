from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must starts with 'M'")

        has_leader = any(
                member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
                for member in self.crew
                )
        if not has_leader:
            raise ValueError(
                    "Mission must have at least"
                    "one Commander or Captian"
                    )
        if self.duration_days > 365:
            experienced = sum(
                    member.years_experience >= 5
                    for member in self.crew
                    )
            if experienced * 2 < len(self.crew):
                raise ValueError(
                        "Long missions need at least"
                        "50% experienced crew"
                        )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat(
                "2027-06-15T10:00:00"
            ),
            duration_days=900,
            budget_millions=2500.0,

            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=38,
                    specialization="Mission Command",
                    years_experience=12,
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=32,
                    specialization="Navigation",
                    years_experience=6,
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=2,
                ),
            ],
        )
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")

        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) "
                f"- {member.specialization}"
            )
    except ValidationError as error:
        print(error)

    print("=" * 41)
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime.fromisoformat(
                "2027-07-01T10:00:00"
            ),
            duration_days=100,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="C004",
                    name="David Lee",
                    rank=Rank.OFFICER,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                ),
                CrewMember(
                    member_id="C005",
                    name="Mary Tan",
                    rank=Rank.LIEUTENANT,
                    age=28,
                    specialization="Navigation",
                    years_experience=4,
                ),
            ],
        )

    except ValidationError as error:
        for detail in error.errors():
            print(detail["msg"])
