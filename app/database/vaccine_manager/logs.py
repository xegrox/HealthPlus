from app.database import Database
from app.models.vaccine_manager.vaccine_log import VaccineLog, VaccineType

vaccine_logs_db = Database('vaccine_logs')


def read_all():
    with vaccine_logs_db.open() as logs:
        return list(logs.values())


def read(batch_no):
    with vaccine_logs_db.open() as logs:
        return logs[batch_no]


def create(batch_no, vaccine_type, quantity, delivery_date, expiry_date):
    log = VaccineLog(batch_no, VaccineType(vaccine_type), quantity, delivery_date, expiry_date)
    with vaccine_logs_db.open() as logs:
        logs.put(log)
        return log


def delete(batch_no):
    with vaccine_logs_db.open() as logs:
        logs.remove(batch_no)
