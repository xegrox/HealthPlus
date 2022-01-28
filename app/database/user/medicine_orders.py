from uuid import uuid4
from app.database import BasicDatabase
from app.database.exceptions import UserNotFoundError, OrderNotFoundError
from app.models.user_medicine_order import UserMedicineOrder

user_medicine_orders_db = BasicDatabase('user_medicine_orders')


def __get_user_orders(orders, user_account_id) -> dict:
    try:
        return orders[user_account_id]
    except KeyError:
        raise UserNotFoundError()


def __get_user_order(user_orders, order_id) -> UserMedicineOrder:
    try:
        return user_orders[order_id]
    except KeyError:
        raise OrderNotFoundError()


def create(user_account_id, medicine_name, quantities, method, collection_date):
    # TODO: check user exists
    # TODO: check medicine id exists
    order = UserMedicineOrder(uuid4().hex, user_account_id, medicine_name, quantities, method, collection_date)
    with user_medicine_orders_db.open() as orders:
        user_orders = orders.get(user_account_id, {})
        user_orders[order.order_id] = order
        orders[user_account_id] = user_orders
        return order


def read(user_account_id, order_id=None):
    with user_medicine_orders_db.open() as orders:
        user_orders = __get_user_orders(orders, user_account_id)
        if order_id is not None:
            return __get_user_order(user_orders, order_id)
        else:
            return user_orders


def update(user_account_id, order_id, status):
    with user_medicine_orders_db.open() as orders:
        user_orders = __get_user_orders(orders, user_account_id)
        order = __get_user_order(user_orders, order_id)
        order.update_status(status)
        orders[user_account_id] = user_orders
        return order


def delete(user_account_id, order_id):
    with user_medicine_orders_db.open() as orders:
        user_orders = __get_user_orders(orders, user_account_id)
        try:
            del user_orders[order_id]
            orders[user_account_id] = user_orders
        except KeyError:
            raise OrderNotFoundError()


def read_all():
    with user_medicine_orders_db.open() as orders:
        return list(orders.values())
