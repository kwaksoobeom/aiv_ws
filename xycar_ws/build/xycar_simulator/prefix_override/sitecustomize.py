import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kwaksoobeom/xycar_ws/install/xycar_simulator'
