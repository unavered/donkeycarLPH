from sqlalchemy.orm import Session

from donkeycarmanager import models, schemas
from donkeycarmanager.crud.workers_read import get_worker
from donkeycarmanager.helpers.utils import dict_to_attr
from donkeycarmanager.services.async_job_scheduler import AsyncJobScheduler


def create_worker(db: Session, worker: schemas.Worker) -> schemas.Worker:
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def update_worker(db: Session, worker: schemas.Worker, job_sched: AsyncJobScheduler) -> schemas.Worker:
    db_worker = get_worker(db=db, worker_id=worker.worker_id)
    dict_to_attr(db_worker, worker.dict())
    db.commit()
    db.refresh(db_worker)

    job_sched.on_worker_changed(worker)
    return db_worker
