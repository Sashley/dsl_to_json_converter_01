from app import db
from datetime import datetime, date, time
from decimal import Decimal

# Auto-generated models using Flask-SQLAlchemy
class S001_Manifest(db.Model):
    __tablename__ = 's001_manifest'
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
    date_of_receipt = db.Column(db.DateTime)

    line_items = db.relationship('S002_LineItem', backref='s001_manifest_line_items', lazy='dynamic')
    shipper = db.relationship('S015_Client', foreign_keys=[shipper_id], backref='s001_manifest_shipper')
    consignee = db.relationship('S015_Client', foreign_keys=[consignee_id], backref='s001_manifest_consignee')
    vessel = db.relationship('S009_Vessel', foreign_keys=[vessel_id], backref='s001_manifest_vessel')
    voyage = db.relationship('S010_Voyage', foreign_keys=[voyage_id], backref='s001_manifest_voyage')
    port_of_loading = db.relationship('S012_Port', foreign_keys=[port_of_loading_id], backref='s001_manifest_port_of_loading')
    port_of_discharge = db.relationship('S012_Port', foreign_keys=[port_of_discharge_id], backref='s001_manifest_port_of_discharge')


class S002_LineItem(db.Model):
    __tablename__ = 's002_lineitem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    manifest_id = db.Column(db.Integer, db.ForeignKey("s001_manifest.id"))
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    pack_type_id = db.Column(db.Integer, db.ForeignKey("s004_packtype.id"))
    commodity_id = db.Column(db.Integer, db.ForeignKey("s003_commodity.id"))
    container_id = db.Column(db.Integer, db.ForeignKey("s005_container.id"))

    manifest = db.relationship('S001_Manifest', foreign_keys=[manifest_id], backref='s002_lineitem_manifest')
    pack_type = db.relationship('S004_PackType', foreign_keys=[pack_type_id], backref='s002_lineitem_pack_type')
    commodity = db.relationship('S003_Commodity', foreign_keys=[commodity_id], backref='s002_lineitem_commodity')
    container = db.relationship('S005_Container', foreign_keys=[container_id], backref='s002_lineitem_container')


class S003_Commodity(db.Model):
    __tablename__ = 's003_commodity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    line_items = db.relationship('S002_LineItem', backref='s003_commodity_line_items', lazy='dynamic')
    rates = db.relationship('S017_Rate', backref='s003_commodity_rates', lazy='dynamic')


class S004_PackType(db.Model):
    __tablename__ = 's004_packtype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    line_items = db.relationship('S002_LineItem', backref='s004_packtype_line_items', lazy='dynamic')
    rates = db.relationship('S017_Rate', backref='s004_packtype_rates', lazy='dynamic')


class S005_Container(db.Model):
    __tablename__ = 's005_container'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    number = db.Column(db.String(255))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    updated = db.Column(db.DateTime)

    line_items = db.relationship('S002_LineItem', backref='s005_container_line_items', lazy='dynamic')
    container_histories = db.relationship('S006_ContainerHistory', backref='s005_container_container_histories', lazy='dynamic')
    port = db.relationship('S012_Port', foreign_keys=[port_id], backref='s005_container_port')


class S006_ContainerHistory(db.Model):
    __tablename__ = 's006_containerhistory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey("s005_container.id"))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    container_status_id = db.Column(db.Integer, db.ForeignKey("s007_containerstatus.id"))
    damage = db.Column(db.String(255))
    updated = db.Column(db.DateTime)

    container = db.relationship('S005_Container', foreign_keys=[container_id], backref='s006_containerhistory_container')
    port = db.relationship('S012_Port', foreign_keys=[port_id], backref='s006_containerhistory_port')
    client = db.relationship('S015_Client', foreign_keys=[client_id], backref='s006_containerhistory_client')
    container_status = db.relationship('S007_ContainerStatus', foreign_keys=[container_status_id], backref='s006_containerhistory_container_status')


class S007_ContainerStatus(db.Model):
    __tablename__ = 's007_containerstatus'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    container_histories = db.relationship('S006_ContainerHistory', backref='s007_containerstatus_container_histories', lazy='dynamic')


class S008_ShippingCompany(db.Model):
    __tablename__ = 's008_shippingcompany'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))

    vessels = db.relationship('S009_Vessel', backref='s008_shippingcompany_vessels', lazy='dynamic')


class S009_Vessel(db.Model):
    __tablename__ = 's009_vessel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    shipping_company_id = db.Column(db.Integer, db.ForeignKey("s008_shippingcompany.id"))

    manifests = db.relationship('S001_Manifest', backref='s009_vessel_manifests', lazy='dynamic')
    voyages = db.relationship('S010_Voyage', backref='s009_vessel_voyages', lazy='dynamic')
    shipping_company = db.relationship('S008_ShippingCompany', foreign_keys=[shipping_company_id], backref='s009_vessel_shipping_company')


class S010_Voyage(db.Model):
    __tablename__ = 's010_voyage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    vessel_id = db.Column(db.Integer, db.ForeignKey("s009_vessel.id"))
    rotation_number = db.Column(db.Integer)

    legs = db.relationship('S011_Leg', backref='s010_voyage_legs', lazy='dynamic')
    manifests = db.relationship('S001_Manifest', backref='s010_voyage_manifests', lazy='dynamic')
    vessel = db.relationship('S009_Vessel', foreign_keys=[vessel_id], backref='s010_voyage_vessel')


class S011_Leg(db.Model):
    __tablename__ = 's011_leg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    voyage_id = db.Column(db.Integer, db.ForeignKey("s010_voyage.id"))
    port_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    leg_number = db.Column(db.Integer)
    eta = db.Column(db.DateTime)
    etd = db.Column(db.DateTime)

    voyage = db.relationship('S010_Voyage', foreign_keys=[voyage_id], backref='s011_leg_voyage')
    port = db.relationship('S012_Port', foreign_keys=[port_id], backref='s011_leg_port')


class S012_Port(db.Model):
    __tablename__ = 's012_port'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    country_id = db.Column(db.Integer, db.ForeignKey("s014_country.id"))
    prefix = db.Column(db.String(255))

    legs = db.relationship('S011_Leg', backref='s012_port_legs', lazy='dynamic')
    containers = db.relationship('S005_Container', backref='s012_port_containers', lazy='dynamic')
    port_pairs_as_pol = db.relationship('S013_PortPair', backref='s012_port_port_pairs_as_pol', lazy='dynamic')
    port_pairs_as_pod = db.relationship('S013_PortPair', backref='s012_port_port_pairs_as_pod', lazy='dynamic')
    country = db.relationship('S014_Country', foreign_keys=[country_id], backref='s012_port_country')


class S013_PortPair(db.Model):
    __tablename__ = 's013_portpair'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    pol_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    pod_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    distance = db.Column(db.Integer)
    distance_rate_code = db.Column(db.String(255))

    pol = db.relationship('S012_Port', foreign_keys=[pol_id], backref='s013_portpair_pol')
    pod = db.relationship('S012_Port', foreign_keys=[pod_id], backref='s013_portpair_pod')


class S014_Country(db.Model):
    __tablename__ = 's014_country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))

    ports = db.relationship('S012_Port', backref='s014_country_ports', lazy='dynamic')
    clients = db.relationship('S015_Client', backref='s014_country_clients', lazy='dynamic')


class S015_Client(db.Model):
    __tablename__ = 's015_client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    town = db.Column(db.String(255))
    country_id = db.Column(db.Integer, db.ForeignKey("s014_country.id"))
    contact_person = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    manifests = db.relationship('S001_Manifest', backref='s015_client_manifests', lazy='dynamic')
    consigned_manifests = db.relationship('S001_Manifest', backref='s015_client_consigned_manifests', lazy='dynamic')
    rates = db.relationship('S017_Rate', backref='s015_client_rates', lazy='dynamic')
    country = db.relationship('S014_Country', foreign_keys=[country_id], backref='s015_client_country')


class S016_User(db.Model):
    __tablename__ = 's016_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    line_items = db.relationship('S002_LineItem', backref='s016_user_line_items', lazy='dynamic')


class S017_Rate(db.Model):
    __tablename__ = 's017_rate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    distance_rate_code = db.Column(db.Integer)
    commodity_id = db.Column(db.Integer, db.ForeignKey("s003_commodity.id"))
    pack_type_id = db.Column(db.Integer, db.ForeignKey("s004_packtype.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    rate = db.Column(db.Float)
    effective = db.Column(db.DateTime)

    commodity = db.relationship('S003_Commodity', foreign_keys=[commodity_id], backref='s017_rate_commodity')
    pack_type = db.relationship('S004_PackType', foreign_keys=[pack_type_id], backref='s017_rate_pack_type')
    client = db.relationship('S015_Client', foreign_keys=[client_id], backref='s017_rate_client')


