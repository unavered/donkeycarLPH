from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import datetime


class PlayerBase(BaseModel):
    player_pseudo: str
    # See pydantic documentation here : https://pydantic-docs.helpmanual.io/usage/types/#datetime-types
    register_datetime: Optional[datetime.datetime]


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    player_id: int

    class Config:
        orm_mode = True


# ---- Driving Waiting Queue ----
class DrivingWaitingQueueBase(BaseModel):
    player_id: int


class DrivingWaitingQueueCreate(DrivingWaitingQueueBase):
    pass


class DrivingWaitingQueue(DrivingWaitingQueueBase):
    rank: int
    start_waiting_datetime: datetime.datetime
    player: Player

    class Config:
        orm_mode = True


# ---- Stage ----
class Stage(str, Enum):
    DRIVE = "DRIVE"
    RECORDING = "RECORDING"
    AI_ASSISTED = "AI_ASSISTED"
    MAINTENANCE = "MAINTENANCE"


# ---- Lap Timer ----
class LapTimerBase(BaseModel):
    race_id: int
    start_datetime: datetime.datetime
    duration: int
    end_datetime: datetime.datetime


class LapTimerCreate(LapTimerBase):
    pass


class LapTimerUpdate(LapTimerBase):
    laptimer_id: int


class LapTimer(LapTimerUpdate):

    class Config:
        orm_mode = True


# ---- Race ----
class RaceBase(BaseModel):
    player_id: int
    stage: Stage
    car_name: str
    start_datetime: datetime.datetime


class RaceCreate(RaceBase):
    pass


class RaceUpdate(RaceBase):
    race_id: int


class Race(RaceUpdate):
    player: Player
    laptimers: List[LapTimer]

    class Config:
        orm_mode = True


# ---- Worker  ----
class WorkerType(str, Enum):
    CAR = "CAR"
    AI_TRAINER = "AI_TRAINER"


class WorkerState(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    STOPPED = "STOPPED"


class WorkerBase(BaseModel):
    type: WorkerType
    state: WorkerState


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(WorkerBase):
    worker_id: int


class Worker(WorkerUpdate):

    class Config:
        orm_mode = True


# ---- Car ----
class CarBase(BaseModel):
    name: str
    ip: str
    color: str
    worker_id: int


class CarCreate(CarBase):
    pass


class CarUpdate(CarBase):
    current_stage: Optional[Stage]
    current_player_id: Optional[int]
    current_race_id: Optional[str]


class Car(CarUpdate):  # As additional nested extended fields
    player: Optional[Player]
    race: Optional[Race]
    worker: Worker

    class Config:
        orm_mode = True


# ---- Worker  ----
class JobState(str, Enum):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    SUCCEED = "SUCCEED"


class JobBase(BaseModel):
    worker_type: WorkerType
    name: str
    parameters: Optional[str]
    state: JobState = Field(default=JobState.WAITING)
    worker_id: Optional[int]
    player_id: int


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    job_id: int
    created_at: datetime.datetime
    rank: int


class Job(JobUpdate):
    worker: Worker
    player: Player

    class Config:
        orm_mode = True


# ---- Events ----
class EventDrivingWaitingQueueUpdated(BaseModel):
    drivePlayersWaitingPool: List[DrivingWaitingQueue]

    class Config:
        orm_mode = True


class EventCar(BaseModel):
    car: Car

    class Config:
        orm_mode = True


class EventCarUpdated(EventCar):
    pass


class EventCarAdded(EventCar):
    pass


class EventCarRemoved(BaseModel):
    car_name: str


class EventLapTimerAdded(BaseModel):
    laptimer: LapTimer

    class Config:
        orm_mode = True


class EventJobQueue(BaseModel):
    jobs: List[Job]

    class Config:
        orm_mode = True


class EventJobChanged(BaseModel):
    job: Job

    class Config:
        orm_mode = True
