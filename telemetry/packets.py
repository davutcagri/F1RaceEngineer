import struct

HEADER_FORMAT = '<HBBBBBQfIIBB'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

SESSION_PACKET_ID = 1
LAP_DATA_PACKET_ID = 2
EVENT_PACKET_ID = 3
CAR_TELEMETRY_PACKET_ID = 6
CAR_STATUS_PACKET_ID = 7
CAR_DAMAGE_PACKET_ID = 10

EVENT_CODE_FORMAT = '<4s'
EVENT_CODE_SIZE = struct.calcsize(EVENT_CODE_FORMAT)
BUTTON_STATUS_EVENT_CODE = b'BUTN'
BUTTON_STATUS_FORMAT = '<I'

# Bit flag for the "UDP Action 1" control - bind any free physical button to
# it in the game's control settings to trigger the race engineer on demand.
TRIGGER_BUTTON_BIT = 0x00100000

TELEM_ENTRY_SIZE = 60
TELEM_ENTRY_FORMAT = '<HfffBbH'

CAR_STATUS_ENTRY_SIZE = 55
CAR_STATUS_ENTRY_FORMAT = '<BBBBBfffHHBBHBBBbfffBfffB'

LAP_DATA_ENTRY_SIZE = 57
LAP_DATA_ENTRY_FORMAT = '<IIHBHBHBHBfffBBBBBBBBBBBBBBBHHBfB'

CAR_DAMAGE_ENTRY_SIZE = 46
CAR_DAMAGE_ENTRY_FORMAT = '<4f4B4B4B18B'

# Session packet fields up to and including m_numMarshalZones. The marshal
# zone and weather forecast arrays that follow are skipped (not needed yet),
# so m_safetyCarStatus/m_networkGame are read via a fixed byte offset instead.
SESSION_LEADING_FORMAT = '<BbbBHBbBHHBBBBBB'
SESSION_LEADING_SIZE = struct.calcsize(SESSION_LEADING_FORMAT)

MARSHAL_ZONE_ENTRY_SIZE = 5
MARSHAL_ZONE_COUNT = 21
SESSION_SAFETY_CAR_OFFSET = SESSION_LEADING_SIZE + (MARSHAL_ZONE_ENTRY_SIZE * MARSHAL_ZONE_COUNT)
SESSION_SAFETY_CAR_FORMAT = '<BB'  # m_safetyCarStatus, m_networkGame
