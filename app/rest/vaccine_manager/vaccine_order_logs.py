from flask_login import login_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from .utils import check_is_vaccine_manager, serialize_log
from app.database.vaccine_manager import logs
from ...models.vaccine_manager.vaccine_log import VaccineType


class VaccineOrderLogs(Resource):

    @login_required
    def get(self):
        check_is_vaccine_manager()
        return list(map(serialize_log, logs.read_all())), 200

    @login_required
    def post(self):
        parser = RequestParser() \
            .add_argument('batch_no', required=True) \
            .add_argument('vaccine_type', choices=(e.value for e in VaccineType), required=True) \
            .add_argument('quantity', type=int, required=True) \
            .add_argument('delivery_date', required=True) \
            .add_argument('expiry_date', required=True)
        args = parser.parse_args()
        log = logs.create(
            batch_no=args['batch_no'],
            vaccine_type=args['vaccine_type'],
            quantity=args['quantity'],
            delivery_date=args['delivery_date'],
            expiry_date=args['expiry_date']
        )
        return serialize_log(log), 200

    @login_required
    def delete(self):
        check_is_vaccine_manager()
        parser = RequestParser().add_argument('batch_no', required=True)
        args = parser.parse_args()
        logs.delete(args['batch_no'])
        return '', 200
