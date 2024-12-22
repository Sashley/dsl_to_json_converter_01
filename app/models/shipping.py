from app import db
from datetime import datetime

# Auto-generated models using Flask-SQLAlchemy

class S001_Manifest(db.Model):
    __tablename__ = 's001_manifest'
    shipper = db.relationship('S015_Client', foreign_keys=[shipper_id], backref='shipments_as_shipper')
    consignee = db.relationship('S015_Client', foreign_keys=[consignee_id], backref='shipments_as_consignee')
    vessel = db.relationship('S009_Vessel', backref='manifests')
    voyage = db.relationship('S010_Voyage', backref='manifests')
    port_of_loading = db.relationship('S012_Port', foreign_keys=[port_of_loading_id], backref='manifests_as_loading')
    port_of_discharge = db.relationship('S012_Port', foreign_keys=[port_of_discharge_id], backref='manifests_as_discharge')
    line_items = db.relationship('S002_LineItem', backref='manifest', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    bill_of_lading = db.Column(db.String(255), unique=True)
    shipper_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    consignee_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    vessel_id = db.Column(db.Integer, db.ForeignKey("s009_vessel.id"))
    voyage_id = db.Column(db.Integer, db.ForeignKey("s010_voyage.id"))
    port_of_loading_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    port_of_discharge_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    place_of_delivery = db.Column(db.String(255))
    place_of_receipt = db.Column(db.String(255))
    clauses = db.Column(db.String(255))
    date_of_receipt = db.Column(db.String(255))


class S002_LineItem(db.Model):
    __tablename__ = 's002_lineitem'
    pack_type = db.relationship('S004_PackType', backref='line_items')
    commodity = db.relationship('S003_Commodity', backref='line_items')
    container = db.relationship('S005_Container', backref='line_items')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    manifest_id = db.Column(db.Integer, db.ForeignKey("s001_manifest.id"))
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    pack_type_id = db.Column(db.Integer, db.ForeignKey("s004_packtype.id"))
    commodity_id = db.Column(db.Integer, db.ForeignKey("s003_commodity.id"))
    container_id = db.Column(db.Integer, db.ForeignKey("s005_container.id"))


class S003_Commodity(db.Model):
    __tablename__ = 's003_commodity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class S004_PackType(db.Model):
    __tablename__ = 's004_packtype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class S005_Container(db.Model):
    __tablename__ = 's005_container'
    port = db.relationship('S012_Port', backref='containers')
    history = db.relationship('S006_ContainerHistory', backref='container', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    number = db.Column(db.String(255))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    updated = db.Column(db.String(255))


class S006_ContainerHistory(db.Model):
    __tablename__ = 's006_containerhistory'
    port = db.relationship('S012_Port', backref='container_history')
    client = db.relationship('S015_Client', backref='container_history')
    status = db.relationship('S007_ContainerStatus', backref='container_history')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey("s005_container.id"))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    container_status_id = db.Column(db.Integer, db.ForeignKey("s007_containerstatus.id"))
    damage = db.Column(db.String(255))
    updated = db.Column(db.String(255))


class S007_ContainerStatus(db.Model):
    __tablename__ = 's007_containerstatus'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class S008_ShippingCompany(db.Model):
    __tablename__ = 's008_shippingcompany'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))


class S009_Vessel(db.Model):
    __tablename__ = 's009_vessel'
    company = db.relationship('S008_ShippingCompany', backref='vessels')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    shipping_company_id = db.Column(db.Integer, db.ForeignKey("s008_shippingcompany.id"))


class S010_Voyage(db.Model):
    __tablename__ = 's010_voyage'
    vessel = db.relationship('S009_Vessel', backref='voyages')
    legs = db.relationship('S011_Leg', backref='voyage', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    vessel_id = db.Column(db.Integer, db.ForeignKey("s009_vessel.id"))
    rotation_number = db.Column(db.Integer)


class S011_Leg(db.Model):
    __tablename__ = 's011_leg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    voyage_id = db.Column(db.Integer, db.ForeignKey("s010_voyage.id"))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    leg_number = db.Column(db.Integer)
    eta = db.Column(db.String(255))
    etd = db.Column(db.String(255))


class S012_Port(db.Model):
    __tablename__ = 's012_port'
    country = db.relationship('S014_Country', backref='ports')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    country_id = db.Column(db.Integer, db.ForeignKey("s014_country.id"))
    prefix = db.Column(db.String(255))


class S013_PortPair(db.Model):
    __tablename__ = 's013_portpair'
    port_of_loading = db.relationship('S012_Port', foreign_keys=[pol_id], backref='port_pairs_as_loading')
    port_of_discharge = db.relationship('S012_Port', foreign_keys=[pod_id], backref='port_pairs_as_discharge')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pol_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    pod_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    distance = db.Column(db.Integer)
    distance_rate_code = db.Column(db.String(255))


class S014_Country(db.Model):
    __tablename__ = 's014_country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))


class S015_Client(db.Model):
    __tablename__ = 's015_client'
    country = db.relationship('S014_Country', backref='clients')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    town = db.Column(db.String(255))
    country_id = db.Column(db.Integer, db.ForeignKey("s014_country.id"))
    contact_person = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))


class S016_User(db.Model):
    __tablename__ = 's016_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))


class S017_Rate(db.Model):
    __tablename__ = 's017_rate'
    commodity = db.relationship('S003_Commodity', backref='rates')
    pack_type = db.relationship('S004_PackType', backref='rates')
    client = db.relationship('S015_Client', backref='rates')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    distance_rate_code = db.Column(db.Integer)
    commodity_id = db.Column(db.Integer, db.ForeignKey("s003_commodity.id"))
    pack_type_id = db.Column(db.Integer, db.ForeignKey("s004_packtype.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    rate = db.Column(db.String(255))
    effective = db.Column(db.String(255))


