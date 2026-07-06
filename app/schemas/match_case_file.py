from pydantic import BaseModel

from app.schemas.evidence_ledger import EvidenceRead
from app.schemas.match import MatchRead
from app.schemas.player import PlayerRead


class MatchCaseFileRead(BaseModel):
    match: MatchRead
    player_a: PlayerRead | None
    player_b: PlayerRead | None
    evidence: list[EvidenceRead]