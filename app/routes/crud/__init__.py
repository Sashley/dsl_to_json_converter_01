from flask import Blueprint

bp = Blueprint('crud', __name__)

from app.routes.crud import s001_manifest
bp.register_blueprint(s001_manifest.bp)

from app.routes.crud import s002_lineitem
bp.register_blueprint(s002_lineitem.bp)

from app.routes.crud import s003_commodity
bp.register_blueprint(s003_commodity.bp)

from app.routes.crud import s004_packtype
bp.register_blueprint(s004_packtype.bp)

from app.routes.crud import s005_container
bp.register_blueprint(s005_container.bp)

from app.routes.crud import s006_containerhistory
bp.register_blueprint(s006_containerhistory.bp)

from app.routes.crud import s007_containerstatus
bp.register_blueprint(s007_containerstatus.bp)

from app.routes.crud import s008_shippingcompany
bp.register_blueprint(s008_shippingcompany.bp)

from app.routes.crud import s009_vessel
bp.register_blueprint(s009_vessel.bp)

from app.routes.crud import s010_voyage
bp.register_blueprint(s010_voyage.bp)

from app.routes.crud import s011_leg
bp.register_blueprint(s011_leg.bp)

from app.routes.crud import s012_port
bp.register_blueprint(s012_port.bp)

from app.routes.crud import s013_portpair
bp.register_blueprint(s013_portpair.bp)

from app.routes.crud import s014_country
bp.register_blueprint(s014_country.bp)

from app.routes.crud import s015_client
bp.register_blueprint(s015_client.bp)

from app.routes.crud import s016_user
bp.register_blueprint(s016_user.bp)

from app.routes.crud import s017_rate
bp.register_blueprint(s017_rate.bp)

