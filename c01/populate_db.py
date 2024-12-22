import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import (Base, S001_Manifest, S002_LineItem, S003_Commodity, S004_PackType, 
                    S005_Container, S006_ContainerHistory, S007_ContainerStatus, 
                    S008_ShippingCompany, S009_Vessel, S010_Voyage, S011_Leg, 
                    S012_Port, S013_PortPair, S014_Country, S015_Client, S016_User, 
                    S017_Rate)

# Connect to the database
print("Connecting to database...")
engine = create_engine("sqlite:///shipping.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("Dropping existing tables...")
    Base.metadata.drop_all(engine)
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully")
except Exception as e:
    print(f"Error during database setup: {str(e)}")
    raise

def generate_container_number(owner_code, equipment_type, serial_number):
    """
    Generate an ISO 6346-compliant container number.
    Args:
        owner_code (str): The 4-letter owner code (e.g., MAEU, CSQU).
        equipment_type (str): The 3-character equipment identifier (e.g., 22G, 45R).
        serial_number (int): The 6-digit unique serial number.
    Returns:
        str: A valid container number with a check digit.
    """
    container_base = f"{owner_code}{equipment_type}{serial_number:06d}"
    
    # Calculate the check digit
    char_weights = {str(i): i for i in range(10)}
    char_weights.update({chr(i): i - 55 for i in range(65, 91)})  # A=10, B=11, ..., Z=35
    total = sum(char_weights[char] * (2 ** idx) for idx, char in enumerate(container_base))
    check_digit = total % 11
    check_digit = 0 if check_digit == 10 else check_digit

    return f"{container_base}{check_digit}"

def generate_bill_of_lading(voyage, pol, pod, sequence_counters):
    """
    Generate a bill of lading number in the format: VOYAGE-ROT-POL-POD-SEQ
    """
    # Get voyage abbreviation (first letter of each word, max 4 letters)
    voyage_name = ''.join(word[0].upper() for word in voyage.name.split())[:4]
    
    # Get port codes
    pol_code = pol.prefix[-3:]  # Last 3 chars of port prefix
    pod_code = pod.prefix[-3:]  # Last 3 chars of port prefix
    
    # Create the combination key for sequence tracking
    combo_key = f"{voyage_name}-{voyage.rotation_number:03d}-{pol_code}-{pod_code}"
    
    # Get and increment sequence number
    if combo_key not in sequence_counters:
        sequence_counters[combo_key] = 1
    else:
        sequence_counters[combo_key] += 1
    
    # Format the bill of lading number
    return f"{combo_key}-{sequence_counters[combo_key]:05d}"

def populate_data():
    try:
        print("Starting to populate data...")
        
        # Dictionary to track sequence numbers
        sequence_counters = {}

        # Populate Level 1: Static Context
        countries = [
            S014_Country(name=country)
            for country in ["USA", "Netherlands", "China", "India", "Germany", "UK", "Japan", "Australia", "Singapore", "Brazil"]
        ]
        session.add_all(countries)

        ports = [
            S012_Port(name=name, country_id=random.randint(1, len(countries)), prefix=prefix)
            for i, (name, prefix) in enumerate([
                ("Port of Los Angeles", "USLAX"),
                ("Port of Rotterdam", "NLRTM"),
                ("Shanghai Port", "CNSHA"),
                ("Port of Mumbai", "INBOM"),
                ("Hamburg Port", "DEHAM"),
                ("London Gateway", "GBLGP"),
                ("Yokohama Port", "JPYOK"),
                ("Sydney Harbor", "AUSYD"),
                ("Port of Singapore", "SGSIN"),
                ("Santos Port", "BRSTS")
            ], start=1)
        ]
        session.add_all(ports)

        companies = [
            S008_ShippingCompany(name=name)
            for name in ["Maersk Line", "CMA CGM", "MSC"]
        ]
        session.add_all(companies)

        packtypes = [
            S004_PackType(name=type_name, description=f"{type_name} Description")
            for type_name in ["20ft Container", "40ft Container", "Refrigerated Container", "Flat Rack Container"]
        ]
        session.add_all(packtypes)

        statuses = [
            S007_ContainerStatus(name=status, description=f"Container is {status.lower()}")
            for status in ["In Transit", "At Port", "Loaded", "Damaged"]
        ]
        session.add_all(statuses)

        clients = [
            S015_Client(
                name=f"Client_{i}", address=f"{random.randint(100, 999)} Market Street",
                town=random.choice(["Los Angeles", "Rotterdam", "Shanghai", "Mumbai", "Hamburg"]),
                country_id=random.randint(1, len(countries)), 
                contact_person=f"Contact_{i}", email=f"client_{i}@shipping.com", 
                phone=f"+123456789{i:02d}"
            )
            for i in range(300)
        ]
        session.add_all(clients)

        commodities = [
            S003_Commodity(name=name, description=f"Shipments of {name.lower()}")
            for name in ["Electronics", "Machinery", "Textiles", "Furniture", "Automobiles"]
        ]
        session.add_all(commodities)

        users = [
            S016_User(name=role, email=f"{role.lower().replace(' ', '_')}@harbor.com", password_hash="hashed_password")
            for role in ["Operations Manager", "Harbor Master", "Shipping Clerk", "Cargo Inspector", "Logistics Coordinator"]
        ]
        session.add_all(users)

        # Populate Level 2
        vessels = [
            S009_Vessel(name=name, shipping_company_id=random.randint(1, len(companies)))
            for name in ["MV Atlantic Star", "SS Oceanic", "HMS Victory", "Evergreen"]
        ]
        session.add_all(vessels)

        port_pairs = [
            S013_PortPair(
                pol_id=random.randint(1, len(ports)), pod_id=random.randint(1, len(ports)),
                distance=random.randint(500, 2000), distance_rate_code=f"RATE_{i:03d}"
            )
            for i in range(50)
        ]
        session.add_all(port_pairs)

        # Populate Level 3
        # Create meaningful voyage names
        voyages = [
            S010_Voyage(
                name=random.choice([
                    "Asia Express Line",
                    "Trans Pacific Service",
                    "Europe Direct Route",
                    "Mediterranean Link",
                    "Atlantic Connection",
                    "Americas Service",
                    "Far East Loop",
                    "Indian Ocean Circuit",
                    "Global Express",
                    "Pacific Rim Route"
                ]),
                vessel_id=random.randint(1, len(vessels)),
                rotation_number=random.randint(1, 10)
            )
            for _ in range(100)
        ]
        session.add_all(voyages)

        # Populate Level 4
        containers = [
            S005_Container(
                number=generate_container_number(
                    owner_code=random.choice(["MAEU", "CMAU", "CSQU"]),
                    equipment_type=random.choice(["22G", "45R", "20T", "40H"]),
                    serial_number=i
                ),
                port_id=random.randint(1, len(ports)),
                updated=datetime.now()
            )
            for i in range(1, 1001)
        ]
        session.add_all(containers)

        # Populate Container Histories
        container_histories = [
            S006_ContainerHistory(
                container_id=container_id,
                port_id=random.randint(1, len(ports)),
                client_id=random.randint(1, len(clients)),
                container_status_id=random.randint(1, len(statuses)),
                damage=random.choice(["None", "Minor", "Major"]),
                updated=datetime.now() - timedelta(days=random.randint(1, 365))
            )
            for container_id in range(1, 1001)
            for _ in range(5)  # 5 history records per container
        ]
        session.add_all(container_histories)

        # Populate Manifests
        # Create manifests with proper bill of lading numbers
        manifests = []
        for _ in range(200):
            # Get random voyage, ports
            voyage = session.query(S010_Voyage).get(random.randint(1, len(voyages)))
            pol = session.query(S012_Port).get(random.randint(1, len(ports)))
            pod = session.query(S012_Port).get(random.randint(1, len(ports)))
            
            # Generate unique bill of lading
            bl_number = generate_bill_of_lading(voyage, pol, pod, sequence_counters)
            
            manifest = S001_Manifest(
                bill_of_lading=bl_number,
                shipper_id=random.randint(1, len(clients)),
                consignee_id=random.randint(1, len(clients)),
                vessel_id=random.randint(1, len(vessels)),
                voyage_id=voyage.id,
                port_of_loading_id=pol.id,
                port_of_discharge_id=pod.id,
                place_of_delivery=random.choice(["Warehouse A", "Terminal B", "Distribution Center C"]),
                place_of_receipt=random.choice(["Factory X", "Supplier Y", "Warehouse Z"]),
                clauses="Standard shipping terms apply",
                date_of_receipt=datetime.now().strftime("%Y-%m-%d")
            )
            manifests.append(manifest)
        session.add_all(manifests)
        session.flush()  # Flush to get manifest IDs

        # Populate LineItems
        line_items = []
        for manifest in manifests:
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                line_items.append(
                    S002_LineItem(
                        manifest_id=manifest.id,
                        description=f"Cargo item for {manifest.bill_of_lading}",
                        quantity=random.randint(1, 100),
                        weight=random.randint(100, 5000),
                        volume=random.randint(1, 100),
                        pack_type_id=random.randint(1, len(packtypes)),
                        commodity_id=random.randint(1, len(commodities)),
                        container_id=random.randint(1, len(containers))
                    )
                )
        session.add_all(line_items)

        # Populate Rates
        rates = [
            S017_Rate(
                distance_rate_code=random.randint(100, 999),
                commodity_id=random.randint(1, len(commodities)),
                pack_type_id=random.randint(1, len(packtypes)),
                client_id=random.randint(1, len(clients)),
                rate=str(random.uniform(500.0, 5000.0)),
                effective=datetime.now().strftime("%Y-%m-%d")
            )
            for _ in range(300)
        ]
        session.add_all(rates)

        # Commit all changes
        session.commit()
        print("Data populated successfully.")
    except Exception as e:
        print(f"Error during data population: {str(e)}")
        session.rollback()
        raise

if __name__ == "__main__":
    populate_data()
