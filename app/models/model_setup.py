from app import db
from app.models.shipping import *

def setup_models():
    """
    Set up model relationships after all models are defined.
    This avoids the circular dependency issues in the generated models.
    """
    # Define columns first
    S001_Manifest.shipper_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    S001_Manifest.consignee_id = db.Column(db.Integer, db.ForeignKey("s015_client.id"))
    S001_Manifest.vessel_id = db.Column(db.Integer, db.ForeignKey("s009_vessel.id"))
    S001_Manifest.voyage_id = db.Column(db.Integer, db.ForeignKey("s010_voyage.id"))
    S001_Manifest.port_of_loading_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    S001_Manifest.port_of_discharge_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))

    S013_PortPair.pol_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))
    S013_PortPair.pod_id = db.Column(db.Integer, db.ForeignKey("s012_port.id"))

    # Now set up relationships
    S001_Manifest.shipper = db.relationship('S015_Client', foreign_keys=[S001_Manifest.shipper_id], backref='shipments_as_shipper')
    S001_Manifest.consignee = db.relationship('S015_Client', foreign_keys=[S001_Manifest.consignee_id], backref='shipments_as_consignee')
    S001_Manifest.vessel = db.relationship('S009_Vessel', backref='manifests')
    S001_Manifest.voyage = db.relationship('S010_Voyage', backref='manifests')
    S001_Manifest.port_of_loading = db.relationship('S012_Port', foreign_keys=[S001_Manifest.port_of_loading_id], backref='manifests_as_loading')
    S001_Manifest.port_of_discharge = db.relationship('S012_Port', foreign_keys=[S001_Manifest.port_of_discharge_id], backref='manifests_as_discharge')
    S001_Manifest.line_items = db.relationship('S002_LineItem', backref='manifest', lazy='dynamic')

    S013_PortPair.port_of_loading = db.relationship('S012_Port', foreign_keys=[S013_PortPair.pol_id], backref='port_pairs_as_loading')
    S013_PortPair.port_of_discharge = db.relationship('S012_Port', foreign_keys=[S013_PortPair.pod_id], backref='port_pairs_as_discharge')

    # Create tables
    db.create_all()
