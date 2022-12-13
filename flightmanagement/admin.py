from flightmanagement import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightmanagement.models import Airport, Airplane, Route, District, \
    Discount, Pricing, Position, Province, Receipt, Ward, Flight, User


admin = Admin(app=app, name="QUẢN LÝ CHUYẾN BAY", template_mode="bootstrap4")
admin.add_view(ModelView(Airport, db.session))
admin.add_view(ModelView(Airplane, db.session))
admin.add_view(ModelView(Route, db.session))
admin.add_view(ModelView(District, db.session))
admin.add_view(ModelView(Discount, db.session))
admin.add_view(ModelView(Pricing, db.session))
admin.add_view(ModelView(Position, db.session))
admin.add_view(ModelView(Province, db.session))
admin.add_view(ModelView(Receipt, db.session))
admin.add_view(ModelView(Ward, db.session))
admin.add_view(ModelView(Flight, db.session))
admin.add_view(ModelView(User, db.session))
