from flightmanagement import db
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, and_, or_, desc, \
    Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
from enum import Enum as MethodEnum


class UserRole(UserEnum):
    ADMIN = 1
    STAFF = 2
    PILOT = 3
    STEWARD = 4
    USER = 5


class MethodPayment(MethodEnum):
    MOMO = 1
    ZALOPAY = 2
    SHOPEEPAY = 3
    CASH = 4


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    active = Column(Boolean, default=True)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.username


class Province(BaseModel):
    __tablename__ = 'province'
    name = Column(String(255), nullable=False)
    code = Column(String(10), nullable=False)
    image = Column(String(200), nullable=True)

    def __str__(self):
        return self.name


class District(BaseModel):
    __tablename__ = 'district'
    name = Column(String(255), nullable=False)
    province_id = Column(Integer, ForeignKey('province.id'), nullable=False)

    def __str__(self):
        return self.name


class Ward(BaseModel):
    __tablename__ = 'ward'
    name = Column(String(255), nullable=False)
    province_id = Column(Integer, ForeignKey('province.id'), nullable=False)
    district_id = Column(Integer, ForeignKey('district.id'), nullable=False)

    def __str__(self):
        return self.name


class Airport(BaseModel):
    __tablename__ = 'airport'
    code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey('ward.id'), nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Airplane(BaseModel):
    __tablename__ = 'airplane'
    code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(255))
    capacity = Column(Integer, nullable=False)
    model_year = Column(String(4), nullable=False)
    location_id = Column(Integer, ForeignKey('airport.id'), nullable=False)
    status = Column(String(255))
    active = Column(Boolean, default=True)
    flights = relationship('Flight', backref='airplane', lazy=True)

    def __str__(self):
        return self.name


class TypeOfPosition(BaseModel):
    __tablename__ = 'type_of_position'
    type_of_position_name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    note = Column(String(255))

    def __str__(self):
        return self.kind_of_room_name


class Position(BaseModel):
    __tablename__ = 'position'
    position_number = Column(String(15), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    type_of_position_id = Column(Integer, ForeignKey('type_of_position.id'), nullable=False)
    airplane_id = Column(Integer, ForeignKey('airplane.id'), nullable=False)
    bookings = relationship('Booking', backref='position', lazy=True)
    note = Column(String(255))

    def __str__(self):
        return str(self.room_number)


class Route(BaseModel):
    __tablename__ = 'route'
    code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    start_location = Column(Integer, ForeignKey('airport.id'), nullable=False)
    end_location = Column(Integer, ForeignKey('airport.id'), nullable=False)

    def __str__(self):
        return self.name


class Flight(BaseModel):
    __tablename__ = 'flight'
    code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    route = Column(Integer, ForeignKey('route.id'), nullable=False)
    airplanes = Column(Integer, ForeignKey('airplane.id'), nullable=False)
    pilot = Column(Integer, ForeignKey('user.id'), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    delay = Column(DateTime, default=0)
    price = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    gate = Column(String(10))
    pricing_id = Column(Integer, ForeignKey('pricing.id'), nullable=False)

    def __str__(self):
        return self.name


class Pricing(BaseModel):
    __tablename__ = 'pricing'
    name = Column(String(50), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    percent = Column(String(50), nullable=False)

    def __str__(self):
        return self.code


class Booking(BaseModel):
    __tablename__ = 'booking'
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    booking_date = Column(DateTime, default=datetime.now())
    cccd_cmnd = Column(String(50), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    gender = Column(String(255))
    phone = Column(String(255))
    date_of_birth = Column(Date)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('position.id'), nullable=False)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)

    def __str__(self):
        return "Vé đặt ghế: {0} - chuyến bay: {1}".format(self.position_id, self.flight_id.name)


class Receipt(BaseModel):
    __tablename__ = 'receipt'
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    bookings = relationship('Booking', backref='receipt', lazy=True)
    details = relationship('ReceiptDetail', backref='receipt.id', lazy=True)

    def __str__(self):
        return "Vé đặt ghế: {0} - chuyến bay: {1}".format(self.position_id, self.flight_id.name)


class ReceiptDetail(BaseModel):
    __tablename__ = 'receipt_detail'
    total = Column(Float, nullable=False)
    note = Column(String(255))
    quantity = Column(Integer, default=0)
    discounts = relationship('Discount', secondary='discount_payment', lazy='subquery',
                             backref=backref('receipt_detail', lazy=True))
    method = Column(Enum(MethodPayment), nullable=False)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)

    def __str__(self):
        return "Mã hóa đơn {0}".format(self.id)


# discount-paymentdetail
discount_payment = db.Table('discount_payment',
                            Column('receipt_detail_id', Integer, ForeignKey('receipt_detail.id'), primary_key=True),
                            Column('discount_id', Integer, ForeignKey('discount.id'), primary_key=True))


class Discount(BaseModel):
    __tablename__ = 'discount'
    name = Column(String(50), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    percent = Column(String(50), nullable=False)

    def __str__(self):
        return self.code


if __name__ == "__main__":
    db.create_all()
