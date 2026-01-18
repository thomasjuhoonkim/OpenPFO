
# Facade Code
# **********************************************************************************
import os
import sys
import socket
from time import sleep, time
import subprocess
import pickle
from openvsp.facade_server import pack_data, unpack_data
from traceback import format_exception
import openvsp_config
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _vsp
else:
    import _vsp
# decorator for wrapping every function
def client_wrap(func):
    def wrapper(self, *args, **kwargs):
        return self._send_receive(func.__name__, args, kwargs)
    return wrapper
def _exception_hook(exc_type, exc_value, tb):
    regular_traceback = []
    facade_traceback = []
    for line in exc_value.args[0].split("\n")[:3]:
        facade_traceback.append(line)

    for line in format_exception(exc_type, exc_value, tb)[:-1]:
        if "facade.py" in line or "facade_server.py" in line:
            facade_traceback.append(line.strip("\n"))
        else:
            regular_traceback.append(line.strip("\n"))
    for line in exc_value.args[0].split("\n")[3:]:
        regular_traceback.append(line)

    print("This error occurred while using the facade API")
    print("Facade Traceback:")
    for line in facade_traceback:
        print(line)
    print("")
    print("Regular Traceback:")
    for line in regular_traceback:
        print(line)

class _vsp_server():
    def __init__(self, name, funcs=[], port=-1):
        self.server_name = name
        HOST = 'localhost'
        if port>0:
            self.port = port
        else:
            self.port = 0
        python_exe = None
        if "python" in os.path.basename(sys.executable):
            python_exe = sys.executable
        elif "python" in os.path.basename(os.__file__):
            python_exe = os.__file__
        else:
            python_exe = "python"
        server_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'facade_server.py')
        for i in range(openvsp_config.FACADE_SERVER_ATTEMPTS):
            try:
                self._proc = subprocess.Popen([python_exe, server_file, str(self.port), str(openvsp_config.LOAD_GRAPHICS)], stderr=subprocess.PIPE)
                start_time = time()
                timeout = openvsp_config.FACADE_SERVER_TIMEOUT  # seconds
                while True:
                    line = self._proc.stderr.readline().strip().decode()
                    # print(line)
                    if not line:
                        if self._proc.poll() is not None:
                            raise RuntimeError("Server process exited unexpectedly")
                        if time() - start_time > timeout:
                            raise TimeoutError("Waiting for server timed out")
                        continue  # No line, but process still alive wait more

                    if line.startswith("Server Socket Thread: Bound to"):
                        self.port = int(line.split()[6][:-2])
                        break
                break
            except Exception as e:
                print(f'Failed to start server, attempt {i+1}, trying again; "{str(e)}"')
                try:
                    self._proc.close()
                    self._proc = None
                except:
                    pass
        if self._proc is None:
            raise RuntimeError("Facade failed to start the server")
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((HOST, self.port))

        for func in funcs:
            setattr(self, func.__name__, (lambda  *args, func=func, **kwargs: self._run_func(func, *args, **kwargs)))

        self.ABS = _vsp.ABS
        r""" Absolute position"""
        self.REL = _vsp.REL
        r""" Relative position"""
        self.SELIG_AF_EXPORT = _vsp.SELIG_AF_EXPORT
        r""" Selig airfoil file format"""
        self.BEZIER_AF_EXPORT = _vsp.BEZIER_AF_EXPORT
        r""" Bezier airfoil file format"""
        self.ALIGN_LEFT = _vsp.ALIGN_LEFT
        r""" Align to left"""
        self.ALIGN_CENTER = _vsp.ALIGN_CENTER
        r""" Align to center"""
        self.ALIGN_RIGHT = _vsp.ALIGN_RIGHT
        r""" Align to right"""
        self.ALIGN_PIXEL = _vsp.ALIGN_PIXEL
        r""" Align to specified pixel"""
        self.ALIGN_TOP = _vsp.ALIGN_TOP
        r""" Align to top"""
        self.ALIGN_MIDDLE = _vsp.ALIGN_MIDDLE
        r""" Align to middle"""
        self.ALIGN_BOTTOM = _vsp.ALIGN_BOTTOM
        r""" Align to bottom"""
        self.NUM_ALIGN_TYPE = _vsp.NUM_ALIGN_TYPE
        r""" Number of alignment types"""
        self.ANG_RAD = _vsp.ANG_RAD
        r""" Radians"""
        self.ANG_DEG = _vsp.ANG_DEG
        r""" Degrees"""
        self.ANG_0 = _vsp.ANG_0
        r""" Zero deg"""
        self.ANG_90 = _vsp.ANG_90
        r""" 90 deg"""
        self.ANG_180 = _vsp.ANG_180
        r""" 180 deg"""
        self.ANG_270 = _vsp.ANG_270
        r""" 270 deg"""
        self.NUM_ANG = _vsp.NUM_ANG
        r""" Number of angle choices"""
        self.ATMOS_TYPE_US_STANDARD_1976 = _vsp.ATMOS_TYPE_US_STANDARD_1976
        r""" US Standard Atmosphere 1976 (default)"""
        self.ATMOS_TYPE_HERRINGTON_1966 = _vsp.ATMOS_TYPE_HERRINGTON_1966
        r""" USAF 1966"""
        self.ATMOS_TYPE_MANUAL_P_R = _vsp.ATMOS_TYPE_MANUAL_P_R
        r""" Manual: pressure and density control"""
        self.ATMOS_TYPE_MANUAL_P_T = _vsp.ATMOS_TYPE_MANUAL_P_T
        r""" Manual: pressure and temperature control"""
        self.ATMOS_TYPE_MANUAL_R_T = _vsp.ATMOS_TYPE_MANUAL_R_T
        r""" Manual: density and temperature control"""
        self.ATMOS_TYPE_MANUAL_RE_L = _vsp.ATMOS_TYPE_MANUAL_RE_L
        r""" Manual: Reynolds number and length control"""
        self.ATTACH_TRANS_NONE = _vsp.ATTACH_TRANS_NONE
        r""" No parent attachment for translations"""
        self.ATTACH_TRANS_COMP = _vsp.ATTACH_TRANS_COMP
        r""" Translation relative to parent body axes"""
        self.ATTACH_TRANS_UV = _vsp.ATTACH_TRANS_UV
        r""" Translation relative to parent surface coordinate frame"""
        self.ATTACH_TRANS_RST = _vsp.ATTACH_TRANS_RST
        r""" Translation relative to parent per-section volume coordinate frame"""
        self.ATTACH_TRANS_LMN = _vsp.ATTACH_TRANS_LMN
        r""" Translation relative to parent uniform volume coordinate frame"""
        self.ATTACH_TRANS_EtaMN = _vsp.ATTACH_TRANS_EtaMN
        r""" Translation relative to wing parent uniform eta volume coordinate frame"""
        self.ATTACH_TRANS_NUM_TYPES = _vsp.ATTACH_TRANS_NUM_TYPES
        r""" Number of translation attachment types"""
        self.ATTACH_ROT_NONE = _vsp.ATTACH_ROT_NONE
        r""" No parent attachment for rotations"""
        self.ATTACH_ROT_COMP = _vsp.ATTACH_ROT_COMP
        r""" Rotation relative to parent body axes"""
        self.ATTACH_ROT_UV = _vsp.ATTACH_ROT_UV
        r""" Rotation relative to parent surface coordinate frame"""
        self.ATTACH_ROT_RST = _vsp.ATTACH_ROT_RST
        r""" Rotation relative to parent per-section volume coordinate frame"""
        self.ATTACH_ROT_LMN = _vsp.ATTACH_ROT_LMN
        r""" Rotation relative to parent uniform volume coordinate frame"""
        self.ATTACH_ROT_EtaMN = _vsp.ATTACH_ROT_EtaMN
        r""" Rotation relative to wing parent eta volume coordinate frame"""
        self.ATTACH_ROT_NUM_TYPES = _vsp.ATTACH_ROT_NUM_TYPES
        r""" Number of rotation attachment types"""
        self.ATTROBJ_PARM = _vsp.ATTROBJ_PARM
        r""" Parm"""
        self.ATTROBJ_GEOM = _vsp.ATTROBJ_GEOM
        r""" Geom"""
        self.ATTROBJ_VEH = _vsp.ATTROBJ_VEH
        r""" Vehicle"""
        self.ATTROBJ_SUBSURF = _vsp.ATTROBJ_SUBSURF
        r""" SubSurf"""
        self.ATTROBJ_MEASURE = _vsp.ATTROBJ_MEASURE
        r""" Measure"""
        self.ATTROBJ_LINK = _vsp.ATTROBJ_LINK
        r""" Link"""
        self.ATTROBJ_ADVLINK = _vsp.ATTROBJ_ADVLINK
        r""" Adv Link"""
        self.ATTROBJ_ATTR = _vsp.ATTROBJ_ATTR
        r""" Attribute"""
        self.ATTROBJ_COLLECTION = _vsp.ATTROBJ_COLLECTION
        r""" Attribute Collection"""
        self.ATTROBJ_XSEC = _vsp.ATTROBJ_XSEC
        r""" Cross Section"""
        self.ATTROBJ_SEC = _vsp.ATTROBJ_SEC
        r""" Wing Section"""
        self.ATTROBJ_MODE = _vsp.ATTROBJ_MODE
        r""" Mode"""
        self.ATTROBJ_SET = _vsp.ATTROBJ_SET
        r""" Geom Set"""
        self.ATTROBJ_VARGROUP = _vsp.ATTROBJ_VARGROUP
        r""" Var Preset Group"""
        self.ATTROBJ_VARSETTING = _vsp.ATTROBJ_VARSETTING
        r""" Var Preset Setting"""
        self.ATTROBJ_FREE = _vsp.ATTROBJ_FREE
        r""" Unattached attribute"""
        self.ATTR_GROUP_NONE = _vsp.ATTR_GROUP_NONE
        r""" No event (user attributes)"""
        self.ATTR_GROUP_WATERMARK = _vsp.ATTR_GROUP_WATERMARK
        r""" Watermark group"""
        self.NUM_ATTR_EVENT_GROUPS = _vsp.NUM_ATTR_EVENT_GROUPS
        r""" Number attribute event groups"""
        self.AUX_GEOM_ROTOR_TIP_PATH = _vsp.AUX_GEOM_ROTOR_TIP_PATH
        r""" Rotor tip path"""
        self.AUX_GEOM_ROTOR_BURST = _vsp.AUX_GEOM_ROTOR_BURST
        r""" Rotor burst zone"""
        self.AUX_GEOM_THREE_PT_GROUND = _vsp.AUX_GEOM_THREE_PT_GROUND
        r""" Three contact point ground plane"""
        self.AUX_GEOM_TWO_PT_GROUND = _vsp.AUX_GEOM_TWO_PT_GROUND
        r""" Two contact point ground plane"""
        self.AUX_GEOM_ONE_PT_GROUND = _vsp.AUX_GEOM_ONE_PT_GROUND
        r""" One contact point ground plane"""
        self.AUX_GEOM_THREE_PT_CCE = _vsp.AUX_GEOM_THREE_PT_CCE
        r""" Three contact point composite clearance envelope"""
        self.AUX_GEOM_SUPER_CONE = _vsp.AUX_GEOM_SUPER_CONE
        r""" Super cone (XSecCurve based profile)"""
        self.NUM_AUX_GEOM_MODES = _vsp.NUM_AUX_GEOM_MODES
        r""" Number of auxiliary geom modes."""
        self.BOGIE_CENTER_DIST = _vsp.BOGIE_CENTER_DIST
        r""" Distance between centers"""
        self.BOGIE_CENTER_DIST_FRAC = _vsp.BOGIE_CENTER_DIST_FRAC
        r""" Fractional distance between centers"""
        self.BOGIE_GAP = _vsp.BOGIE_GAP
        r""" Gap"""
        self.BOGIE_GAP_FRAC = _vsp.BOGIE_GAP_FRAC
        r""" Fractional gap"""
        self.NUM_BOGIE_SPACING_TYPE = _vsp.NUM_BOGIE_SPACING_TYPE
        r""" Number of bogie spacing control modes"""
        self.BOR_FLOWTHROUGH = _vsp.BOR_FLOWTHROUGH
        r""" Flowthrough mode (default)"""
        self.BOR_UPPER = _vsp.BOR_UPPER
        r""" Upper surface mode"""
        self.BOR_LOWER = _vsp.BOR_LOWER
        r""" Lower surface mode"""
        self.BOR_NUM_MODES = _vsp.BOR_NUM_MODES
        r""" Number of Body of Revolution modes"""
        self.MAX_CAMB = _vsp.MAX_CAMB
        r""" Input maximum camber, calculate ideal lift coefficient"""
        self.DESIGN_CL = _vsp.DESIGN_CL
        r""" Input ideal lift coefficient, calculate maximum camber"""
        self.CAM_TOP = _vsp.CAM_TOP
        r""" Camera top view"""
        self.CAM_FRONT = _vsp.CAM_FRONT
        r""" Camera front view"""
        self.CAM_FRONT_YUP = _vsp.CAM_FRONT_YUP
        r""" Camera front Y-up view"""
        self.CAM_LEFT = _vsp.CAM_LEFT
        r""" Camera left view"""
        self.CAM_LEFT_ISO = _vsp.CAM_LEFT_ISO
        r""" Camera left isometric view"""
        self.CAM_BOTTOM = _vsp.CAM_BOTTOM
        r""" Camera bottom view"""
        self.CAM_REAR = _vsp.CAM_REAR
        r""" Camera rear view"""
        self.CAM_RIGHT = _vsp.CAM_RIGHT
        r""" Camera right view"""
        self.CAM_RIGHT_ISO = _vsp.CAM_RIGHT_ISO
        r""" Camera right isometric view"""
        self.CAM_CENTER = _vsp.CAM_CENTER
        r""" Camera center view"""
        self.NO_END_CAP = _vsp.NO_END_CAP
        r""" No end cap"""
        self.FLAT_END_CAP = _vsp.FLAT_END_CAP
        r""" Flat end cap"""
        self.ROUND_END_CAP = _vsp.ROUND_END_CAP
        r""" Round end cap"""
        self.EDGE_END_CAP = _vsp.EDGE_END_CAP
        r""" Edge end cap"""
        self.SHARP_END_CAP = _vsp.SHARP_END_CAP
        r""" Sharp end cap"""
        self.POINT_END_CAP = _vsp.POINT_END_CAP
        r""" Point end cap"""
        self.ROUND_EXT_END_CAP_NONE = _vsp.ROUND_EXT_END_CAP_NONE
        r""" Extended round end cap, but not extended"""
        self.ROUND_EXT_END_CAP_LE = _vsp.ROUND_EXT_END_CAP_LE
        r""" Extended round end cap, extend LE"""
        self.ROUND_EXT_END_CAP_TE = _vsp.ROUND_EXT_END_CAP_TE
        r""" Extended round end cap, extend TE"""
        self.ROUND_EXT_END_CAP_BOTH = _vsp.ROUND_EXT_END_CAP_BOTH
        r""" Extended round end cap, extend both"""
        self.NUM_END_CAP_OPTIONS = _vsp.NUM_END_CAP_OPTIONS
        r""" Number of end cap options"""
        self.CFD_MIN_EDGE_LEN = _vsp.CFD_MIN_EDGE_LEN
        r""" Minimum mesh edge length"""
        self.CFD_MAX_EDGE_LEN = _vsp.CFD_MAX_EDGE_LEN
        r""" Maximum mesh edge length"""
        self.CFD_MAX_GAP = _vsp.CFD_MAX_GAP
        r""" Maximum mesh edge gap"""
        self.CFD_NUM_CIRCLE_SEGS = _vsp.CFD_NUM_CIRCLE_SEGS
        r""" Number of edge segments to resolve circle"""
        self.CFD_GROWTH_RATIO = _vsp.CFD_GROWTH_RATIO
        r""" Maximum allowed edge growth ratio"""
        self.CFD_LIMIT_GROWTH_FLAG = _vsp.CFD_LIMIT_GROWTH_FLAG
        r""" Rigorous 3D growth limiting flag"""
        self.CFD_INTERSECT_SUBSURFACE_FLAG = _vsp.CFD_INTERSECT_SUBSURFACE_FLAG
        r""" Flag to intersect sub-surfaces"""
        self.CFD_HALF_MESH_FLAG = _vsp.CFD_HALF_MESH_FLAG
        r""" Flag to generate a half mesh"""
        self.CFD_FAR_FIELD_FLAG = _vsp.CFD_FAR_FIELD_FLAG
        r""" Flag to generate a far field mesh"""
        self.CFD_FAR_MAX_EDGE_LEN = _vsp.CFD_FAR_MAX_EDGE_LEN
        r""" Maximum far field mesh edge length"""
        self.CFD_FAR_MAX_GAP = _vsp.CFD_FAR_MAX_GAP
        r""" Maximum far field mesh edge gap"""
        self.CFD_FAR_NUM_CIRCLE_SEGS = _vsp.CFD_FAR_NUM_CIRCLE_SEGS
        r""" Number of far field edge segments to resolve circle"""
        self.CFD_FAR_SIZE_ABS_FLAG = _vsp.CFD_FAR_SIZE_ABS_FLAG
        r""" Relative or absolute size flag"""
        self.CFD_FAR_LENGTH = _vsp.CFD_FAR_LENGTH
        r""" Far field length"""
        self.CFD_FAR_WIDTH = _vsp.CFD_FAR_WIDTH
        r""" Far field width"""
        self.CFD_FAR_HEIGHT = _vsp.CFD_FAR_HEIGHT
        r""" Far field height"""
        self.CFD_FAR_X_SCALE = _vsp.CFD_FAR_X_SCALE
        r"""  Far field X scale"""
        self.CFD_FAR_Y_SCALE = _vsp.CFD_FAR_Y_SCALE
        r"""  Far field Y scale"""
        self.CFD_FAR_Z_SCALE = _vsp.CFD_FAR_Z_SCALE
        r"""  Far field Z scale"""
        self.CFD_FAR_LOC_MAN_FLAG = _vsp.CFD_FAR_LOC_MAN_FLAG
        r""" Far field location flag: centered or manual"""
        self.CFD_FAR_LOC_X = _vsp.CFD_FAR_LOC_X
        r""" Far field X location"""
        self.CFD_FAR_LOC_Y = _vsp.CFD_FAR_LOC_Y
        r""" Far field Y location"""
        self.CFD_FAR_LOC_Z = _vsp.CFD_FAR_LOC_Z
        r""" Far field Z location"""
        self.CFD_SRF_XYZ_FLAG = _vsp.CFD_SRF_XYZ_FLAG
        r""" Flag to include X,Y,Z intersection curves in export files"""
        self.CFD_STL_FILE_NAME = _vsp.CFD_STL_FILE_NAME
        r""" STL export type"""
        self.CFD_POLY_FILE_NAME = _vsp.CFD_POLY_FILE_NAME
        r""" POLY export type"""
        self.CFD_TRI_FILE_NAME = _vsp.CFD_TRI_FILE_NAME
        r""" TRI export type"""
        self.CFD_OBJ_FILE_NAME = _vsp.CFD_OBJ_FILE_NAME
        r""" OBJ export type"""
        self.CFD_DAT_FILE_NAME = _vsp.CFD_DAT_FILE_NAME
        r""" DAT export type"""
        self.CFD_KEY_FILE_NAME = _vsp.CFD_KEY_FILE_NAME
        r""" KEY export type"""
        self.CFD_GMSH_FILE_NAME = _vsp.CFD_GMSH_FILE_NAME
        r""" GMSH export type"""
        self.CFD_TKEY_FILE_NAME = _vsp.CFD_TKEY_FILE_NAME
        r""" TKEY export type"""
        self.CFD_FACET_FILE_NAME = _vsp.CFD_FACET_FILE_NAME
        r""" FACET export type"""
        self.CFD_VSPGEOM_FILE_NAME = _vsp.CFD_VSPGEOM_FILE_NAME
        r""" VSPGEOM export type"""
        self.CFD_NUM_FILE_NAMES = _vsp.CFD_NUM_FILE_NAMES
        r""" Number of CFD Mesh export file types"""
        self.POINT_SOURCE = _vsp.POINT_SOURCE
        r""" Point source"""
        self.LINE_SOURCE = _vsp.LINE_SOURCE
        r""" Line source"""
        self.BOX_SOURCE = _vsp.BOX_SOURCE
        r""" Box source"""
        self.ULINE_SOURCE = _vsp.ULINE_SOURCE
        r""" Constant U Line source"""
        self.WLINE_SOURCE = _vsp.WLINE_SOURCE
        r""" Constant W Line source"""
        self.NUM_SOURCE_TYPES = _vsp.NUM_SOURCE_TYPES
        r""" Number of CFD Mesh source types"""
        self.TAG = _vsp.TAG
        r""" Color mesh by tag value (component, subsurface, part, etc)"""
        self.REASON = _vsp.REASON
        r""" Color mesh by local edge length reason"""
        self.CF_LAM_BLASIUS = _vsp.CF_LAM_BLASIUS
        r""" Blasius laminar Cf equation"""
        self.CF_LAM_BLASIUS_W_HEAT = _vsp.CF_LAM_BLASIUS_W_HEAT
        r""" Blasius laminar Cf equation with heat (NOT IMPLEMENTED)"""
        self.CF_TURB_EXPLICIT_FIT_SPALDING = _vsp.CF_TURB_EXPLICIT_FIT_SPALDING
        r""" Explicit Fit of Spalding turbulent Cf equation"""
        self.CF_TURB_EXPLICIT_FIT_SPALDING_CHI = _vsp.CF_TURB_EXPLICIT_FIT_SPALDING_CHI
        r""" Explicit Fit of Spalding and Chi turbulent Cf equation"""
        self.CF_TURB_EXPLICIT_FIT_SCHOENHERR = _vsp.CF_TURB_EXPLICIT_FIT_SCHOENHERR
        r""" Explicit Fit of Schoenherr turbulent Cf equation"""
        self.DO_NOT_USE_CF_TURB_IMPLICIT_KARMAN = _vsp.DO_NOT_USE_CF_TURB_IMPLICIT_KARMAN
        r""" Implicit Karman turbulent Cf equation (DO NOT USE)"""
        self.CF_TURB_IMPLICIT_SCHOENHERR = _vsp.CF_TURB_IMPLICIT_SCHOENHERR
        r""" Implicit Schoenherr turbulent Cf equation"""
        self.CF_TURB_IMPLICIT_KARMAN_SCHOENHERR = _vsp.CF_TURB_IMPLICIT_KARMAN_SCHOENHERR
        r""" Implicit Karman-Schoenherr turbulent Cf equation"""
        self.CF_TURB_POWER_LAW_BLASIUS = _vsp.CF_TURB_POWER_LAW_BLASIUS
        r""" Power Law Blasius turbulent Cf equation"""
        self.CF_TURB_POWER_LAW_PRANDTL_LOW_RE = _vsp.CF_TURB_POWER_LAW_PRANDTL_LOW_RE
        r"""Power Law Prandtl Low Re turbulent Cf equation"""
        self.CF_TURB_POWER_LAW_PRANDTL_MEDIUM_RE = _vsp.CF_TURB_POWER_LAW_PRANDTL_MEDIUM_RE
        r""" Power Law Prandtl Medium Re turbulent Cf equation"""
        self.CF_TURB_POWER_LAW_PRANDTL_HIGH_RE = _vsp.CF_TURB_POWER_LAW_PRANDTL_HIGH_RE
        r""" Power Law Prandtl High Re turbulent Cf equation"""
        self.CF_TURB_SCHLICHTING_COMPRESSIBLE = _vsp.CF_TURB_SCHLICHTING_COMPRESSIBLE
        r""" Schlichting Compressible turbulent Cf equation"""
        self.DO_NOT_USE_CF_TURB_SCHLICHTING_INCOMPRESSIBLE = _vsp.DO_NOT_USE_CF_TURB_SCHLICHTING_INCOMPRESSIBLE
        r""" Schlichting Incompressible turbulent Cf equation (DO NOT USE)"""
        self.DO_NOT_USE_CF_TURB_SCHLICHTING_PRANDTL = _vsp.DO_NOT_USE_CF_TURB_SCHLICHTING_PRANDTL
        r""" Schlichting-Prandtl turbulent Cf equation (DO NOT USE)"""
        self.DO_NOT_USE_CF_TURB_SCHULTZ_GRUNOW_HIGH_RE = _vsp.DO_NOT_USE_CF_TURB_SCHULTZ_GRUNOW_HIGH_RE
        r""" Schultz-Grunow High Re turbulent Cf equation (DO NOT USE)"""
        self.CF_TURB_SCHULTZ_GRUNOW_SCHOENHERR = _vsp.CF_TURB_SCHULTZ_GRUNOW_SCHOENHERR
        r""" Schultz-Grunow Estimate of Schoenherr turbulent Cf equation."""
        self.DO_NOT_USE_CF_TURB_WHITE_CHRISTOPH_COMPRESSIBLE = _vsp.DO_NOT_USE_CF_TURB_WHITE_CHRISTOPH_COMPRESSIBLE
        r""" White-Christoph Compressible turbulent Cf equation (DO NOT USE)"""
        self.CF_TURB_ROUGHNESS_SCHLICHTING_AVG = _vsp.CF_TURB_ROUGHNESS_SCHLICHTING_AVG
        r""" Roughness Schlichting Avg turbulent Cf equation."""
        self.DO_NOT_USE_CF_TURB_ROUGHNESS_SCHLICHTING_LOCAL = _vsp.DO_NOT_USE_CF_TURB_ROUGHNESS_SCHLICHTING_LOCAL
        r""" Roughness Schlichting Local turbulent Cf equation (DO NOT USE)"""
        self.DO_NOT_USE_CF_TURB_ROUGHNESS_WHITE = _vsp.DO_NOT_USE_CF_TURB_ROUGHNESS_WHITE
        r""" Roughness White turbulent Cf equation (DO NOT USE)"""
        self.CF_TURB_ROUGHNESS_SCHLICHTING_AVG_FLOW_CORRECTION = _vsp.CF_TURB_ROUGHNESS_SCHLICHTING_AVG_FLOW_CORRECTION
        r""" Roughness Schlichting Avg Compressible turbulent Cf equation."""
        self.CF_TURB_HEATTRANSFER_WHITE_CHRISTOPH = _vsp.CF_TURB_HEATTRANSFER_WHITE_CHRISTOPH
        r""" Heat Transfer White-Christoph turbulent Cf equation."""
        self.CHEVRON_NONE = _vsp.CHEVRON_NONE
        r""" No chevron."""
        self.CHEVRON_PARTIAL = _vsp.CHEVRON_PARTIAL
        r""" One or more chevrons of limited extent."""
        self.CHEVRON_FULL = _vsp.CHEVRON_FULL
        r""" Full period of chevrons."""
        self.CHEVRON_NUM_TYPES = _vsp.CHEVRON_NUM_TYPES
        r""" Number of chevron types."""
        self.CHEVRON_W01_SE = _vsp.CHEVRON_W01_SE
        r""" Start and End"""
        self.CHEVRON_W01_CW = _vsp.CHEVRON_W01_CW
        r""" Center and Width"""
        self.CHEVRON_W01_NUM_MODES = _vsp.CHEVRON_W01_NUM_MODES
        r""" Number of chevron W parameter mode types."""
        self.COLLISION_OK = _vsp.COLLISION_OK
        r""" No Error."""
        self.COLLISION_INTERSECT_NO_SOLUTION = _vsp.COLLISION_INTERSECT_NO_SOLUTION
        r""" Touching, no solution"""
        self.COLLISION_CLEAR_NO_SOLUTION = _vsp.COLLISION_CLEAR_NO_SOLUTION
        r""" Not touching, no solution"""
        self.NO_FILE_TYPE = _vsp.NO_FILE_TYPE
        r""" No export file type"""
        self.COMP_GEOM_TXT_TYPE = _vsp.COMP_GEOM_TXT_TYPE
        self.COMP_GEOM_CSV_TYPE = _vsp.COMP_GEOM_CSV_TYPE
        self.DRAG_BUILD_TSV_TYPE_DEPRECATED = _vsp.DRAG_BUILD_TSV_TYPE_DEPRECATED
        self.SLICE_TXT_TYPE = _vsp.SLICE_TXT_TYPE
        self.MASS_PROP_TXT_TYPE = _vsp.MASS_PROP_TXT_TYPE
        self.DEGEN_GEOM_CSV_TYPE = _vsp.DEGEN_GEOM_CSV_TYPE
        self.DEGEN_GEOM_M_TYPE = _vsp.DEGEN_GEOM_M_TYPE
        self.CFD_STL_TYPE = _vsp.CFD_STL_TYPE
        self.CFD_POLY_TYPE = _vsp.CFD_POLY_TYPE
        self.CFD_TRI_TYPE = _vsp.CFD_TRI_TYPE
        self.CFD_OBJ_TYPE = _vsp.CFD_OBJ_TYPE
        self.CFD_DAT_TYPE = _vsp.CFD_DAT_TYPE
        self.CFD_KEY_TYPE = _vsp.CFD_KEY_TYPE
        self.CFD_GMSH_TYPE = _vsp.CFD_GMSH_TYPE
        self.CFD_SRF_TYPE_DEPRECATED = _vsp.CFD_SRF_TYPE_DEPRECATED
        self.CFD_TKEY_TYPE = _vsp.CFD_TKEY_TYPE
        self.PROJ_AREA_CSV_TYPE = _vsp.PROJ_AREA_CSV_TYPE
        self.WAVE_DRAG_TXT_TYPE = _vsp.WAVE_DRAG_TXT_TYPE
        self.VSPAERO_PANEL_TRI_TYPE = _vsp.VSPAERO_PANEL_TRI_TYPE
        self.DRAG_BUILD_CSV_TYPE = _vsp.DRAG_BUILD_CSV_TYPE
        self.CFD_FACET_TYPE = _vsp.CFD_FACET_TYPE
        self.CFD_CURV_TYPE_DEPRECATED = _vsp.CFD_CURV_TYPE_DEPRECATED
        self.CFD_PLOT3D_TYPE_DEPRECATED = _vsp.CFD_PLOT3D_TYPE_DEPRECATED
        self.CFD_VSPGEOM_TYPE = _vsp.CFD_VSPGEOM_TYPE
        self.VSPAERO_VSPGEOM_TYPE = _vsp.VSPAERO_VSPGEOM_TYPE
        self.U_TRIM = _vsp.U_TRIM
        r""" Trim by U coordinate"""
        self.L_TRIM = _vsp.L_TRIM
        r""" Trim by L coordinate"""
        self.ETA_TRIM = _vsp.ETA_TRIM
        r""" Trim by Eta coordinate"""
        self.NUM_TRIM_TYPES = _vsp.NUM_TRIM_TYPES
        r""" Number of conformal component trim types"""
        self.DELIM_COMMA = _vsp.DELIM_COMMA
        r""" Comma delimiter"""
        self.DELIM_USCORE = _vsp.DELIM_USCORE
        r""" Underscore delimiter"""
        self.DELIM_SPACE = _vsp.DELIM_SPACE
        r""" Space delimiter"""
        self.DELIM_NONE = _vsp.DELIM_NONE
        r""" No delimiter"""
        self.DELIM_NUM_TYPES = _vsp.DELIM_NUM_TYPES
        r""" Number of delimiter types"""
        self.DEPTH_FRONT = _vsp.DEPTH_FRONT
        r""" Set 3D background before model"""
        self.DEPTH_REAR = _vsp.DEPTH_REAR
        r""" Set 3D background behind model"""
        self.DEPTH_FREE = _vsp.DEPTH_FREE
        r""" Set 3D background at specified location"""
        self.NUM_DEPTH_TYPE = _vsp.NUM_DEPTH_TYPE
        r""" Number of depth types"""
        self.SET_3D = _vsp.SET_3D
        r""" 3D DXF export (default)"""
        self.SET_2D = _vsp.SET_2D
        r""" 2D DXF export"""
        self.X_DIR = _vsp.X_DIR
        r""" X direction"""
        self.Y_DIR = _vsp.Y_DIR
        self.Z_DIR = _vsp.Z_DIR
        self.ALL_DIR = _vsp.ALL_DIR
        self.DISPLAY_BEZIER = _vsp.DISPLAY_BEZIER
        r""" Display the normal Bezier surface (default)"""
        self.DISPLAY_DEGEN_SURF = _vsp.DISPLAY_DEGEN_SURF
        r""" Display as surface Degen Geom"""
        self.DISPLAY_DEGEN_PLATE = _vsp.DISPLAY_DEGEN_PLATE
        r""" Display as plate Degen Geom"""
        self.DISPLAY_DEGEN_CAMBER = _vsp.DISPLAY_DEGEN_CAMBER
        r""" Display as camber Degen Geom"""
        self.GEOM_DRAW_WIRE = _vsp.GEOM_DRAW_WIRE
        r""" Draw the wireframe mesh (see through)"""
        self.GEOM_DRAW_HIDDEN = _vsp.GEOM_DRAW_HIDDEN
        r""" Draw the hidden mesh"""
        self.GEOM_DRAW_SHADE = _vsp.GEOM_DRAW_SHADE
        r""" Draw the shaded mesh"""
        self.GEOM_DRAW_TEXTURE = _vsp.GEOM_DRAW_TEXTURE
        r""" Draw the textured mesh"""
        self.GEOM_DRAW_NONE = _vsp.GEOM_DRAW_NONE
        r""" Do not draw anything"""
        self.ENGINE_GEOM_NONE = _vsp.ENGINE_GEOM_NONE
        r""" Component is not an integrated flowpath component."""
        self.ENGINE_GEOM_INLET = _vsp.ENGINE_GEOM_INLET
        r""" Component represents integrated flowpath inlet."""
        self.ENGINE_GEOM_INLET_OUTLET = _vsp.ENGINE_GEOM_INLET_OUTLET
        r""" Component represents integrated flowpath inlet and outlet."""
        self.ENGINE_GEOM_OUTLET = _vsp.ENGINE_GEOM_OUTLET
        r""" Component represents integrated flowpath outlet."""
        self.ENGINE_GEOM_IO_NUM_TYPES = _vsp.ENGINE_GEOM_IO_NUM_TYPES
        r""" Number of integrated flowpath component types."""
        self.ENGINE_GEOM_FLOWTHROUGH = _vsp.ENGINE_GEOM_FLOWTHROUGH
        r""" Component is modeled as flowthrough engine."""
        self.ENGINE_GEOM_TO_LIP = _vsp.ENGINE_GEOM_TO_LIP
        r""" Component is modeled to the lip."""
        self.ENGINE_GEOM_FLOWPATH = _vsp.ENGINE_GEOM_FLOWPATH
        r""" Component flowpath is modeled."""
        self.ENGINE_GEOM_TO_FACE = _vsp.ENGINE_GEOM_TO_FACE
        r""" Component is modeled to face."""
        self.ENGINE_GEOM_NUM_TYPES = _vsp.ENGINE_GEOM_NUM_TYPES
        r""" Number of integrated flowpath modeling types."""
        self.ENGINE_LOC_INDEX = _vsp.ENGINE_LOC_INDEX
        r""" Integrated flowpath key point identified by XSec index."""
        self.ENGINE_LOC_U = _vsp.ENGINE_LOC_U
        r""" Integrated flowpath key point identified by U parameter."""
        self.ENGINE_LOC_INLET_LIP = _vsp.ENGINE_LOC_INLET_LIP
        r""" Integrated flowpath key point is inlet lip."""
        self.ENGINE_LOC_INLET_FACE = _vsp.ENGINE_LOC_INLET_FACE
        r""" Integrated flowpath key point is inlet face."""
        self.ENGINE_LOC_OUTLET_LIP = _vsp.ENGINE_LOC_OUTLET_LIP
        r""" Integrated flowpath key point is outlet lip."""
        self.ENGINE_LOC_OUTLET_FACE = _vsp.ENGINE_LOC_OUTLET_FACE
        r""" Integrated flowpath key point is outlet face."""
        self.ENGINE_LOC_NUM = _vsp.ENGINE_LOC_NUM
        r""" Number of integrated flowpath key point locations."""
        self.ENGINE_MODE_FLOWTHROUGH = _vsp.ENGINE_MODE_FLOWTHROUGH
        r""" Represent integrated flowpath as flowthrough engine."""
        self.ENGINE_MODE_FLOWTHROUGH_NEG = _vsp.ENGINE_MODE_FLOWTHROUGH_NEG
        r""" Represent integrated flowpath as flowthrough engine with negative flowpath."""
        self.ENGINE_MODE_TO_LIP = _vsp.ENGINE_MODE_TO_LIP
        r""" Represent integrated flowpath to the lip."""
        self.ENGINE_MODE_TO_FACE = _vsp.ENGINE_MODE_TO_FACE
        r""" Represent integrated flowpath to the face."""
        self.ENGINE_MODE_TO_FACE_NEG = _vsp.ENGINE_MODE_TO_FACE_NEG
        r""" Represent integrated flowpath to the face with negative flowpath to the face."""
        self.ENGINE_MODE_EXTEND = _vsp.ENGINE_MODE_EXTEND
        r""" Represent integrated flowpath with farfield extensions."""
        self.ENGINE_MODE_NUM_TYPES = _vsp.ENGINE_MODE_NUM_TYPES
        r""" Number of integrated flowpath representations."""
        self.VSP_OK = _vsp.VSP_OK
        r""" No error"""
        self.VSP_INVALID_PTR = _vsp.VSP_INVALID_PTR
        r""" Invalid pointer error"""
        self.VSP_INVALID_TYPE = _vsp.VSP_INVALID_TYPE
        r""" Invalid type error"""
        self.VSP_CANT_FIND_TYPE = _vsp.VSP_CANT_FIND_TYPE
        r""" Can't find type error"""
        self.VSP_CANT_FIND_PARM = _vsp.VSP_CANT_FIND_PARM
        r""" Can't find parm error"""
        self.VSP_CANT_FIND_NAME = _vsp.VSP_CANT_FIND_NAME
        r""" Can't find name error"""
        self.VSP_INVALID_GEOM_ID = _vsp.VSP_INVALID_GEOM_ID
        r""" Invalid Geom ID error"""
        self.VSP_FILE_DOES_NOT_EXIST = _vsp.VSP_FILE_DOES_NOT_EXIST
        r""" File does not exist error"""
        self.VSP_FILE_WRITE_FAILURE = _vsp.VSP_FILE_WRITE_FAILURE
        r""" File write failure error"""
        self.VSP_FILE_READ_FAILURE = _vsp.VSP_FILE_READ_FAILURE
        r""" File read failure error"""
        self.VSP_WRONG_GEOM_TYPE = _vsp.VSP_WRONG_GEOM_TYPE
        r""" Wrong Geom type error"""
        self.VSP_WRONG_XSEC_TYPE = _vsp.VSP_WRONG_XSEC_TYPE
        r""" Wrong XSec type error"""
        self.VSP_WRONG_FILE_TYPE = _vsp.VSP_WRONG_FILE_TYPE
        r""" Wrong file type error"""
        self.VSP_INDEX_OUT_RANGE = _vsp.VSP_INDEX_OUT_RANGE
        r""" Index out of range error"""
        self.VSP_INVALID_XSEC_ID = _vsp.VSP_INVALID_XSEC_ID
        r""" Invalid XSec ID error"""
        self.VSP_INVALID_ID = _vsp.VSP_INVALID_ID
        r""" Invalid ID error"""
        self.VSP_CANT_SET_NOT_EQ_PARM = _vsp.VSP_CANT_SET_NOT_EQ_PARM
        r""" Can't set NotEqParm error"""
        self.VSP_AMBIGUOUS_SUBSURF = _vsp.VSP_AMBIGUOUS_SUBSURF
        r""" Ambiguous flow-through sub-surface error"""
        self.VSP_INVALID_VARPRESET_SETNAME = _vsp.VSP_INVALID_VARPRESET_SETNAME
        r""" Invalid Variable Preset set name error"""
        self.VSP_INVALID_VARPRESET_GROUPNAME = _vsp.VSP_INVALID_VARPRESET_GROUPNAME
        r""" Invalid Variable Preset group name error"""
        self.VSP_CONFORMAL_PARENT_UNSUPPORTED = _vsp.VSP_CONFORMAL_PARENT_UNSUPPORTED
        r""" Unsupported Conformal Geom parent error"""
        self.VSP_UNEXPECTED_RESET_REMAP_ID = _vsp.VSP_UNEXPECTED_RESET_REMAP_ID
        r""" Unexpected reset remap ID error"""
        self.VSP_INVALID_INPUT_VAL = _vsp.VSP_INVALID_INPUT_VAL
        r""" Invalid input value error"""
        self.VSP_INVALID_CF_EQN = _vsp.VSP_INVALID_CF_EQN
        r""" Invalid friction coefficient equation error"""
        self.VSP_INVALID_DRIVERS = _vsp.VSP_INVALID_DRIVERS
        r""" Invalid drivers for driver group"""
        self.VSP_ADV_LINK_BUILD_FAIL = _vsp.VSP_ADV_LINK_BUILD_FAIL
        r""" Advanced link build failure"""
        self.VSP_DEPRECATED = _vsp.VSP_DEPRECATED
        r""" This capability has been deprecated and is not longer supported"""
        self.VSP_LINK_LOOP_DETECTED = _vsp.VSP_LINK_LOOP_DETECTED
        r""" A parameter link loop was detected and stopped"""
        self.VSP_LINK_OUTPUT_NOT_ASSIGNED = _vsp.VSP_LINK_OUTPUT_NOT_ASSIGNED
        r""" An output of a parameter link was not set"""
        self.VSP_DUPLICATE_NAME = _vsp.VSP_DUPLICATE_NAME
        r""" A duplicate name has been provided"""
        self.VSP_GUI_DEVICE_DEACTIVATED = _vsp.VSP_GUI_DEVICE_DEACTIVATED
        r""" A deactivated GUI device was touched"""
        self.VSP_COULD_NOT_CREATE_BACKGROUND3D = _vsp.VSP_COULD_NOT_CREATE_BACKGROUND3D
        r""" Could not create and add Background3D"""
        self.VSP_NUM_ERROR_CODE = _vsp.VSP_NUM_ERROR_CODE
        r""" Total number of VSP error codes"""
        self.EXCRESCENCE_COUNT = _vsp.EXCRESCENCE_COUNT
        r""" Drag counts excressence type"""
        self.EXCRESCENCE_CD = _vsp.EXCRESCENCE_CD
        r""" Drag coefficient excressence type"""
        self.EXCRESCENCE_PERCENT_GEOM = _vsp.EXCRESCENCE_PERCENT_GEOM
        r""" Percent of parent Geom drag coefficient excressence type"""
        self.EXCRESCENCE_MARGIN = _vsp.EXCRESCENCE_MARGIN
        r""" Percent margin excressence type"""
        self.EXCRESCENCE_DRAGAREA = _vsp.EXCRESCENCE_DRAGAREA
        r""" Drag area (D/q) excressence type"""
        self.EXPORT_FELISA = _vsp.EXPORT_FELISA
        r""" FELISA export type (NOT IMPLEMENTED)"""
        self.EXPORT_XSEC = _vsp.EXPORT_XSEC
        r""" XSec (*.hrm) export type"""
        self.EXPORT_STL = _vsp.EXPORT_STL
        r""" Stereolith (*.stl) export type"""
        self.EXPORT_AWAVE = _vsp.EXPORT_AWAVE
        r""" AWAVE export type (NOT IMPLEMENTED)"""
        self.EXPORT_NASCART = _vsp.EXPORT_NASCART
        r""" NASCART (*.dat) export type"""
        self.EXPORT_POVRAY = _vsp.EXPORT_POVRAY
        r""" POVRAY (*.pov) export type"""
        self.EXPORT_CART3D = _vsp.EXPORT_CART3D
        r""" Cart3D (*.tri) export type"""
        self.EXPORT_VSPGEOM = _vsp.EXPORT_VSPGEOM
        r""" VSPGeom (*.vspgeom) export type"""
        self.EXPORT_VORXSEC = _vsp.EXPORT_VORXSEC
        r""" VORXSEC  export type (NOT IMPLEMENTED)"""
        self.EXPORT_XSECGEOM = _vsp.EXPORT_XSECGEOM
        r""" XSECGEOM export type (NOT IMPLEMENTED)"""
        self.EXPORT_GMSH = _vsp.EXPORT_GMSH
        r""" Gmsh (*.msh) export type"""
        self.EXPORT_X3D = _vsp.EXPORT_X3D
        r""" X3D (*.x3d) export type"""
        self.EXPORT_STEP = _vsp.EXPORT_STEP
        r""" STEP (*.stp) export type"""
        self.EXPORT_PLOT3D = _vsp.EXPORT_PLOT3D
        r""" PLOT3D (*.p3d) export type"""
        self.EXPORT_IGES = _vsp.EXPORT_IGES
        r""" IGES (*.igs) export type"""
        self.EXPORT_BEM = _vsp.EXPORT_BEM
        r""" Blade Element (*.bem) export type"""
        self.EXPORT_DXF = _vsp.EXPORT_DXF
        r""" AutoCAD (*.dxf) export type"""
        self.EXPORT_FACET = _vsp.EXPORT_FACET
        r""" Xpatch (*.facet) export type"""
        self.EXPORT_SVG = _vsp.EXPORT_SVG
        r""" SVG (*.svg) export type"""
        self.EXPORT_PMARC = _vsp.EXPORT_PMARC
        r""" PMARC 12 (*.pmin) export type"""
        self.EXPORT_OBJ = _vsp.EXPORT_OBJ
        r""" OBJ (*.obj) export type"""
        self.EXPORT_SELIG_AIRFOIL = _vsp.EXPORT_SELIG_AIRFOIL
        r""" Airfoil points (*.dat) export type"""
        self.EXPORT_BEZIER_AIRFOIL = _vsp.EXPORT_BEZIER_AIRFOIL
        r""" Airfoil curves (*.bz) export type"""
        self.EXPORT_IGES_STRUCTURE = _vsp.EXPORT_IGES_STRUCTURE
        r""" IGES structure (*.igs) export type"""
        self.EXPORT_STEP_STRUCTURE = _vsp.EXPORT_STEP_STRUCTURE
        r""" STEP structure (*.stp) export type"""
        self.FEA_BCM_USER = _vsp.FEA_BCM_USER
        r""" FEA boundary condition constraints user defined."""
        self.FEA_BCM_ALL = _vsp.FEA_BCM_ALL
        r""" FEA boundary condition constrains all DOF."""
        self.FEA_BCM_PIN = _vsp.FEA_BCM_PIN
        r""" FEA boundary condition pin constraints."""
        self.FEA_BCM_SYMM = _vsp.FEA_BCM_SYMM
        r""" FEA boundary condition symmetrical constraints."""
        self.FEA_BCM_ASYMM = _vsp.FEA_BCM_ASYMM
        r""" FEA boundary condition antisymmetrical constraints."""
        self.FEA_NUM_BCM_MODES = _vsp.FEA_NUM_BCM_MODES
        r""" Number of FEA boundary condition constraint types."""
        self.FEA_BC_STRUCTURE = _vsp.FEA_BC_STRUCTURE
        r""" FEA boundary condition assigned to structure."""
        self.FEA_BC_PART = _vsp.FEA_BC_PART
        r""" FEA boundary condition assigned to part."""
        self.FEA_BC_SUBSURF = _vsp.FEA_BC_SUBSURF
        r""" FEA boundary condition assigned to subsurface."""
        self.FEA_NUM_BC_TYPES = _vsp.FEA_NUM_BC_TYPES
        r""" Number of FEA boundary condition definition types."""
        self.FEA_XSEC_GENERAL = _vsp.FEA_XSEC_GENERAL
        r""" General XSec type"""
        self.FEA_XSEC_CIRC = _vsp.FEA_XSEC_CIRC
        r""" Circle XSec type"""
        self.FEA_XSEC_PIPE = _vsp.FEA_XSEC_PIPE
        r""" Pipe XSec type"""
        self.FEA_XSEC_I = _vsp.FEA_XSEC_I
        r""" I XSec type"""
        self.FEA_XSEC_RECT = _vsp.FEA_XSEC_RECT
        r""" Rectangle XSec type"""
        self.FEA_XSEC_BOX = _vsp.FEA_XSEC_BOX
        r""" Box XSec type"""
        self.FEA_MASS_FILE_NAME = _vsp.FEA_MASS_FILE_NAME
        r""" FEA Mesh mass export type"""
        self.FEA_NASTRAN_FILE_NAME = _vsp.FEA_NASTRAN_FILE_NAME
        r""" FEA Mesh NASTRAN export type"""
        self.FEA_NKEY_FILE_NAME = _vsp.FEA_NKEY_FILE_NAME
        r""" FEA Mesh NKey export type"""
        self.FEA_CALCULIX_FILE_NAME = _vsp.FEA_CALCULIX_FILE_NAME
        r""" FEA Mesh Calculix export type"""
        self.FEA_STL_FILE_NAME = _vsp.FEA_STL_FILE_NAME
        r""" FEA Mesh STL export type"""
        self.FEA_GMSH_FILE_NAME = _vsp.FEA_GMSH_FILE_NAME
        r""" FEA Mesh GMSH export type"""
        self.FEA_SRF_FILE_NAME = _vsp.FEA_SRF_FILE_NAME
        r""" FEA Mesh SRF export type"""
        self.FEA_CURV_FILE_NAME = _vsp.FEA_CURV_FILE_NAME
        r""" FEA Mesh CURV export type"""
        self.FEA_PLOT3D_FILE_NAME = _vsp.FEA_PLOT3D_FILE_NAME
        r""" FEA Mesh PLOT3D export type"""
        self.FEA_IGES_FILE_NAME = _vsp.FEA_IGES_FILE_NAME
        r""" FEA Mesh trimmed IGES export type"""
        self.FEA_STEP_FILE_NAME = _vsp.FEA_STEP_FILE_NAME
        r""" FEA Mesh trimmed STEP export type"""
        self.FEA_NUM_FILE_NAMES = _vsp.FEA_NUM_FILE_NAMES
        r""" Number of FEA Mesh export type."""
        self.FEA_FIX_PT_ON_BODY = _vsp.FEA_FIX_PT_ON_BODY
        r""" On body fixed point type"""
        self.FEA_FIX_PT_GLOBAL_XYZ = _vsp.FEA_FIX_PT_GLOBAL_XYZ
        r""" Global XYZ off body fixed point type"""
        self.FEA_FIX_PT_DELTA_XYZ = _vsp.FEA_FIX_PT_DELTA_XYZ
        r""" Delta XYZ off body fixed point type"""
        self.FEA_FIX_PT_DELTA_UVN = _vsp.FEA_FIX_PT_DELTA_UVN
        r""" Delta UVN off body fixed point type"""
        self.FEA_FIX_PT_GEOM_ORIGIN = _vsp.FEA_FIX_PT_GEOM_ORIGIN
        r""" Geom origin off body fixed point type"""
        self.FEA_FIX_PT_GEOM_CG = _vsp.FEA_FIX_PT_GEOM_CG
        r""" Geom CG off body fixed point type"""
        self.FEA_NUM_FIX_PT_TYPES = _vsp.FEA_NUM_FIX_PT_TYPES
        r""" Number of off body fixed point types"""
        self.FEA_ISOTROPIC = _vsp.FEA_ISOTROPIC
        r""" Isotropic material"""
        self.FEA_ENG_ORTHO = _vsp.FEA_ENG_ORTHO
        r""" Orthotropic material in engineering parameters"""
        self.FEA_ENG_ORTHO_TRANS_ISO = _vsp.FEA_ENG_ORTHO_TRANS_ISO
        r""" Orthotropic material with transverse isotropy assumed in engineering parameters"""
        self.FEA_LAMINATE = _vsp.FEA_LAMINATE
        r""" Laminate buildup material"""
        self.FEA_NUM_MAT_TYPES = _vsp.FEA_NUM_MAT_TYPES
        r""" Number of FEA material types"""
        self.FEA_ORIENT_GLOBAL_X = _vsp.FEA_ORIENT_GLOBAL_X
        r""" FEA Global X material orientation"""
        self.FEA_ORIENT_GLOBAL_Y = _vsp.FEA_ORIENT_GLOBAL_Y
        r""" FEA Global Y material orientation"""
        self.FEA_ORIENT_GLOBAL_Z = _vsp.FEA_ORIENT_GLOBAL_Z
        r""" FEA Global Z material orientation"""
        self.FEA_ORIENT_COMP_X = _vsp.FEA_ORIENT_COMP_X
        r""" FEA Comp X material orientation"""
        self.FEA_ORIENT_COMP_Y = _vsp.FEA_ORIENT_COMP_Y
        r""" FEA Comp Y material orientation"""
        self.FEA_ORIENT_COMP_Z = _vsp.FEA_ORIENT_COMP_Z
        r""" FEA Comp Z material orientation"""
        self.FEA_ORIENT_PART_U = _vsp.FEA_ORIENT_PART_U
        r""" FEA Part U material orientation"""
        self.FEA_ORIENT_PART_V = _vsp.FEA_ORIENT_PART_V
        r""" FEA Part V material orientation"""
        self.FEA_ORIENT_OML_U = _vsp.FEA_ORIENT_OML_U
        r""" FEA OML U material orientation"""
        self.FEA_ORIENT_OML_V = _vsp.FEA_ORIENT_OML_V
        r""" FEA OML V material orientation"""
        self.FEA_ORIENT_OML_R = _vsp.FEA_ORIENT_OML_R
        r""" FEA OML R material orientation"""
        self.FEA_ORIENT_OML_S = _vsp.FEA_ORIENT_OML_S
        r""" FEA OML S material orientation"""
        self.FEA_ORIENT_OML_T = _vsp.FEA_ORIENT_OML_T
        r""" FEA OML T material orientation"""
        self.FEA_NUM_ORIENT_TYPES = _vsp.FEA_NUM_ORIENT_TYPES
        r""" Number of FEA material orientation types"""
        self.FEA_DEPRECATED = _vsp.FEA_DEPRECATED
        r""" Flag for deprecated element type option"""
        self.FEA_SHELL = _vsp.FEA_SHELL
        r""" Shell (tris) FEA element type"""
        self.FEA_BEAM = _vsp.FEA_BEAM
        r""" Beam FEA element type"""
        self.FEA_SHELL_AND_BEAM = _vsp.FEA_SHELL_AND_BEAM
        r""" Both Shell and Beam FEA element types"""
        self.FEA_NO_ELEMENTS = _vsp.FEA_NO_ELEMENTS
        r""" FEA part with no elements"""
        self.FEA_NUM_ELEMENT_TYPES = _vsp.FEA_NUM_ELEMENT_TYPES
        r""" Number of FEA element type choices"""
        self.FEA_SLICE = _vsp.FEA_SLICE
        r""" Slice FEA Part type"""
        self.FEA_RIB = _vsp.FEA_RIB
        r""" Rib FEA Part type"""
        self.FEA_SPAR = _vsp.FEA_SPAR
        r""" Spar FEA Part type"""
        self.FEA_FIX_POINT = _vsp.FEA_FIX_POINT
        r""" Fixed Point FEA Part type"""
        self.FEA_DOME = _vsp.FEA_DOME
        r""" Dome FEA Part type"""
        self.FEA_RIB_ARRAY = _vsp.FEA_RIB_ARRAY
        r""" Rib array FEA Part type"""
        self.FEA_SLICE_ARRAY = _vsp.FEA_SLICE_ARRAY
        r""" Slice array FEA Part type"""
        self.FEA_SKIN = _vsp.FEA_SKIN
        r""" Skin FEA Part type"""
        self.FEA_TRIM = _vsp.FEA_TRIM
        r""" Trim FEA Part type"""
        self.FEA_POLY_SPAR = _vsp.FEA_POLY_SPAR
        r""" Poly Spar FEA Part type"""
        self.FEA_NUM_TYPES = _vsp.FEA_NUM_TYPES
        r""" Number of FEA Part types"""
        self.NO_NORMAL = _vsp.NO_NORMAL
        r""" FEA Rib or Rib Array has no set perpendicular edge"""
        self.LE_NORMAL = _vsp.LE_NORMAL
        r""" FEA Rib or Rib Array is set perpendicular to the leading edge"""
        self.TE_NORMAL = _vsp.TE_NORMAL
        r""" FEA Rib or Rib Array is set perpendicular to the trailing edge"""
        self.SPAR_NORMAL = _vsp.SPAR_NORMAL
        r""" FEA Rib or Rib Array is set perpendicular to an FEA Spar"""
        self.FEA_KEEP = _vsp.FEA_KEEP
        r""" Keep shell elements"""
        self.FEA_DELETE = _vsp.FEA_DELETE
        r""" Delete shell elements"""
        self.FEA_NUM_SHELL_TREATMENT_TYPES = _vsp.FEA_NUM_SHELL_TREATMENT_TYPES
        r""" Number of FEA subsurface treatment choices"""
        self.XY_BODY = _vsp.XY_BODY
        r""" Slice is parallel to parent Geom body XY plane"""
        self.YZ_BODY = _vsp.YZ_BODY
        r""" Slice is parallel to parent Geom body YZ plane"""
        self.XZ_BODY = _vsp.XZ_BODY
        r""" Slice is parallel to parent Geom body XZ plane"""
        self.XY_ABS = _vsp.XY_ABS
        r""" Slice is parallel to absolute XY plane"""
        self.YZ_ABS = _vsp.YZ_ABS
        r""" Slice is parallel to absolute YZ plane"""
        self.XZ_ABS = _vsp.XZ_ABS
        r""" Slice is parallel to absolute XZ plane"""
        self.SPINE_NORMAL = _vsp.SPINE_NORMAL
        r""" Slice is perpendicular to thespine of the parent Geom"""
        self.POLY_SPAR_POINT_U01 = _vsp.POLY_SPAR_POINT_U01
        r""" Spar points span specified in U01"""
        self.POLY_SPAR_POINT_U0N = _vsp.POLY_SPAR_POINT_U0N
        r""" Spar points span specified in U0N"""
        self.POLY_SPAR_POINT_ETA = _vsp.POLY_SPAR_POINT_ETA
        r""" Spar points span specified in eta"""
        self.NUM_POLY_SPAR_POINT_TYPES = _vsp.NUM_POLY_SPAR_POINT_TYPES
        r""" Number of poly spar point types"""
        self.SI_UNIT = _vsp.SI_UNIT
        r""" FEA Files output in (m, kg)"""
        self.CGS_UNIT = _vsp.CGS_UNIT
        r""" FEA Files output in (cm, g)"""
        self.MPA_UNIT = _vsp.MPA_UNIT
        r""" FEA Files output in (mm, tonne)"""
        self.BFT_UNIT = _vsp.BFT_UNIT
        r""" FEA Files output in (ft, slug)"""
        self.BIN_UNIT = _vsp.BIN_UNIT
        r""" FEA Files output in (in, lbf*sec^2/in)"""
        self.FF_B_MANUAL = _vsp.FF_B_MANUAL
        r""" Manual FF equation"""
        self.FF_B_SCHEMENSKY_FUSE = _vsp.FF_B_SCHEMENSKY_FUSE
        r""" Schemensky Fuselage FF equation"""
        self.FF_B_SCHEMENSKY_NACELLE = _vsp.FF_B_SCHEMENSKY_NACELLE
        r""" Schemensky Nacelle FF equation"""
        self.FF_B_HOERNER_STREAMBODY = _vsp.FF_B_HOERNER_STREAMBODY
        r""" Hoerner Streamlined Body FF equation"""
        self.FF_B_TORENBEEK = _vsp.FF_B_TORENBEEK
        r""" Torenbeek FF equation"""
        self.FF_B_SHEVELL = _vsp.FF_B_SHEVELL
        r""" Shevell FF equation"""
        self.FF_B_COVERT = _vsp.FF_B_COVERT
        r""" Covert FF equation"""
        self.FF_B_JENKINSON_FUSE = _vsp.FF_B_JENKINSON_FUSE
        r""" Jenkinson Fuselage FF equation"""
        self.FF_B_JENKINSON_WING_NACELLE = _vsp.FF_B_JENKINSON_WING_NACELLE
        r""" Jenkinson Wing Nacelle FF equation"""
        self.FF_B_JENKINSON_AFT_FUSE_NACELLE = _vsp.FF_B_JENKINSON_AFT_FUSE_NACELLE
        r""" Jenkinson Aft Fuselage Nacelle FF equation"""
        self.FF_W_MANUAL = _vsp.FF_W_MANUAL
        r""" Manual FF equation"""
        self.FF_W_EDET_CONV = _vsp.FF_W_EDET_CONV
        r""" EDET Conventional Airfoil FF equation"""
        self.FF_W_EDET_ADV = _vsp.FF_W_EDET_ADV
        r""" EDET Advanced Airfoil FF equation"""
        self.FF_W_HOERNER = _vsp.FF_W_HOERNER
        r""" Hoerner FF equation"""
        self.FF_W_COVERT = _vsp.FF_W_COVERT
        r""" Covert FF equation"""
        self.FF_W_SHEVELL = _vsp.FF_W_SHEVELL
        r""" Shevell FF equation"""
        self.FF_W_KROO = _vsp.FF_W_KROO
        r""" Kroo FF equation"""
        self.FF_W_TORENBEEK = _vsp.FF_W_TORENBEEK
        r""" Torenbeek FF equation"""
        self.FF_W_DATCOM = _vsp.FF_W_DATCOM
        r""" DATCOM FF equation"""
        self.FF_W_SCHEMENSKY_6_SERIES_AF = _vsp.FF_W_SCHEMENSKY_6_SERIES_AF
        r""" Schemensky 6 Series Airfoil FF equation"""
        self.FF_W_SCHEMENSKY_4_SERIES_AF = _vsp.FF_W_SCHEMENSKY_4_SERIES_AF
        r""" Schemensky 4 Series Airfoil FF equation"""
        self.FF_W_JENKINSON_WING = _vsp.FF_W_JENKINSON_WING
        r""" Jenkinson Wing FF equation"""
        self.FF_W_JENKINSON_TAIL = _vsp.FF_W_JENKINSON_TAIL
        r""" Jenkinson Tail FF equation"""
        self.FF_W_SCHEMENSKY_SUPERCRITICAL_AF = _vsp.FF_W_SCHEMENSKY_SUPERCRITICAL_AF
        r""" Schemensky Supercritical Airfoil FF equation"""
        self.PD_UNITS_IMPERIAL = _vsp.PD_UNITS_IMPERIAL
        r""" Imperial unit system"""
        self.PD_UNITS_METRIC = _vsp.PD_UNITS_METRIC
        r""" Metric unit system"""
        self.OPEN = _vsp.OPEN
        r""" Browse files that already exist"""
        self.SAVE = _vsp.SAVE
        r""" Browse file system and enter file name"""
        self.NUM_FILE_CHOOSER_MODES = _vsp.NUM_FILE_CHOOSER_MODES
        r""" Number of file chooser modes"""
        self.FC_OPENVSP = _vsp.FC_OPENVSP
        r""" OpenVSP's own file chooser with directory preferences."""
        self.FC_NATIVE = _vsp.FC_NATIVE
        r""" Operating system's native file chooser"""
        self.NUM_FILE_CHOOSER_TYPES = _vsp.NUM_FILE_CHOOSER_TYPES
        r""" Number of file chooser types"""
        self.GDEV_TAB = _vsp.GDEV_TAB
        r""" Custom GUI Tab"""
        self.GDEV_SCROLL_TAB = _vsp.GDEV_SCROLL_TAB
        r""" Custom GUI Fl_Scroll and Tab"""
        self.GDEV_GROUP = _vsp.GDEV_GROUP
        r""" Custom GUI Group"""
        self.GDEV_PARM_BUTTON = _vsp.GDEV_PARM_BUTTON
        r""" Custom GUI ParmButton"""
        self.GDEV_INPUT = _vsp.GDEV_INPUT
        r""" Custom GUI Input"""
        self.GDEV_OUTPUT = _vsp.GDEV_OUTPUT
        r""" Custom GUI Output"""
        self.GDEV_SLIDER = _vsp.GDEV_SLIDER
        r""" Custom GUI Slider"""
        self.GDEV_SLIDER_ADJ_RANGE = _vsp.GDEV_SLIDER_ADJ_RANGE
        r""" Custom GUI SliderAdjRangeInput"""
        self.GDEV_CHECK_BUTTON = _vsp.GDEV_CHECK_BUTTON
        r""" Custom GUI CheckButton"""
        self.GDEV_CHECK_BUTTON_BIT = _vsp.GDEV_CHECK_BUTTON_BIT
        r""" Custom GUI CheckButtonBit"""
        self.GDEV_RADIO_BUTTON = _vsp.GDEV_RADIO_BUTTON
        r""" Custom GUI RadioButton"""
        self.GDEV_TOGGLE_BUTTON = _vsp.GDEV_TOGGLE_BUTTON
        r""" Custom GUI ToggleButton"""
        self.GDEV_TOGGLE_BUTTON_FREE = _vsp.GDEV_TOGGLE_BUTTON_FREE
        r""" Custom GUI ToggleButton without Parm"""
        self.GDEV_TOGGLE_RADIO_GROUP = _vsp.GDEV_TOGGLE_RADIO_GROUP
        r""" Custom GUI ToggleRadioGroup (NOT IMPLEMENTED)"""
        self.GDEV_TRIGGER_BUTTON = _vsp.GDEV_TRIGGER_BUTTON
        r""" Custom GUI TriggerButton"""
        self.GDEV_COUNTER = _vsp.GDEV_COUNTER
        r""" Custom GUI Counter"""
        self.GDEV_CHOICE = _vsp.GDEV_CHOICE
        r""" Custom GUI Choice"""
        self.GDEV_ADD_CHOICE_ITEM = _vsp.GDEV_ADD_CHOICE_ITEM
        r""" Add item to custom GUI Choice"""
        self.GDEV_SLIDER_INPUT = _vsp.GDEV_SLIDER_INPUT
        r""" Custom GUI SliderInput"""
        self.GDEV_SLIDER_ADJ_RANGE_INPUT = _vsp.GDEV_SLIDER_ADJ_RANGE_INPUT
        r""" Custom GUI SliderAdjRangeInput"""
        self.GDEV_SLIDER_ADJ_RANGE_TWO_INPUT = _vsp.GDEV_SLIDER_ADJ_RANGE_TWO_INPUT
        r""" Custom GUI SliderAdjRangeInput with two inputs (NOT IMPLEMENTED)"""
        self.GDEV_FRACT_PARM_SLIDER = _vsp.GDEV_FRACT_PARM_SLIDER
        r""" Custom GUI FractParmSlider"""
        self.GDEV_STRING_INPUT = _vsp.GDEV_STRING_INPUT
        r""" Custom GUI StringInput"""
        self.GDEV_INDEX_SELECTOR = _vsp.GDEV_INDEX_SELECTOR
        r""" Custom GUI IndexSelector"""
        self.GDEV_COLOR_PICKER = _vsp.GDEV_COLOR_PICKER
        r""" Custom GUI ColorPicker"""
        self.GDEV_YGAP = _vsp.GDEV_YGAP
        r""" Custom GUI Y gap"""
        self.GDEV_DIVIDER_BOX = _vsp.GDEV_DIVIDER_BOX
        r""" Custom GUI divider box"""
        self.GDEV_BEGIN_SAME_LINE = _vsp.GDEV_BEGIN_SAME_LINE
        r""" Set begin same line flag for custom GUI"""
        self.GDEV_END_SAME_LINE = _vsp.GDEV_END_SAME_LINE
        r""" Set end same line flag for custom GUI"""
        self.GDEV_FORCE_WIDTH = _vsp.GDEV_FORCE_WIDTH
        r""" Set forced width for custom GUI"""
        self.GDEV_SET_FORMAT = _vsp.GDEV_SET_FORMAT
        r""" Set format label for custom GUI"""
        self.NUM_GDEV_TYPES = _vsp.NUM_GDEV_TYPES
        r""" Number of GDEV types"""
        self.ALL_GDEV_TYPES = _vsp.ALL_GDEV_TYPES
        r""" Flag for all GDEV types"""
        self.GEAR_SUSPENSION_NOMINAL = _vsp.GEAR_SUSPENSION_NOMINAL
        r""" Gear suspension at nominal extension"""
        self.GEAR_SUSPENSION_COMPRESSED = _vsp.GEAR_SUSPENSION_COMPRESSED
        r""" Gear suspension is compressed"""
        self.GEAR_SUSPENSION_EXTENDED = _vsp.GEAR_SUSPENSION_EXTENDED
        r""" Gear suspension is extended"""
        self.NUM_GEAR_SUSPENSION_MODES = _vsp.NUM_GEAR_SUSPENSION_MODES
        r""" Number of gear suspension choices"""
        self.MALE = _vsp.MALE
        r""" Male Human component"""
        self.FEMALE = _vsp.FEMALE
        r""" Female Human component"""
        self.EXTERNAL_INTERFERENCE = _vsp.EXTERNAL_INTERFERENCE
        r""" Interference between mutually external bodies"""
        self.PACKAGING_INTERFERENCE = _vsp.PACKAGING_INTERFERENCE
        r""" Interference when one body is internal to another"""
        self.EXTERNAL_SELF_INTERFERENCE = _vsp.EXTERNAL_SELF_INTERFERENCE
        r""" Interference between multiple surfaces of one Geom / Set"""
        self.PLANE_STATIC_DISTANCE_INTERFERENCE = _vsp.PLANE_STATIC_DISTANCE_INTERFERENCE
        r""" Interference between surfaces and a plane"""
        self.PLANE_2PT_ANGLE_INTERFERENCE = _vsp.PLANE_2PT_ANGLE_INTERFERENCE
        r""" Interference angle between surfaces and a plane"""
        self.GEAR_CG_TIPBACK_ANALYSIS = _vsp.GEAR_CG_TIPBACK_ANALYSIS
        r""" Calculate tipback angle"""
        self.PLANE_1PT_ANGLE_INTERFERENCE = _vsp.PLANE_1PT_ANGLE_INTERFERENCE
        r""" Interference roll angle between surfaces and a plane"""
        self.GEAR_WEIGHT_DISTRIBUTION_ANALYSIS = _vsp.GEAR_WEIGHT_DISTRIBUTION_ANALYSIS
        r""" Calculate distribution of weight across landing gear"""
        self.GEAR_TIPOVER_ANALYSIS = _vsp.GEAR_TIPOVER_ANALYSIS
        r""" Calculate tipover angle"""
        self.GEAR_TURN_ANALYSIS = _vsp.GEAR_TURN_ANALYSIS
        r""" Calculate ground manueveribility"""
        self.VISIBLE_FROM_POINT_ANALYSIS = _vsp.VISIBLE_FROM_POINT_ANALYSIS
        r""" Calculate az,el domain visible from a point"""
        self.CCE_INTERFERENCE = _vsp.CCE_INTERFERENCE
        r""" Interference with composite clearance envelope"""
        self.NUM_INTERFERENCE_TYPES = _vsp.NUM_INTERFERENCE_TYPES
        r""" Number of interference check types"""
        self.POD_GEOM_SCREEN = _vsp.POD_GEOM_SCREEN
        r""" Pod geom screen"""
        self.FUSELAGE_GEOM_SCREEN = _vsp.FUSELAGE_GEOM_SCREEN
        r""" Fuselage geom screen"""
        self.MS_WING_GEOM_SCREEN = _vsp.MS_WING_GEOM_SCREEN
        r""" Wing geom screen"""
        self.BLANK_GEOM_SCREEN = _vsp.BLANK_GEOM_SCREEN
        r""" Blank geom screen"""
        self.MESH_GEOM_SCREEN = _vsp.MESH_GEOM_SCREEN
        r""" Mesh geom screen"""
        self.NGON_MESH_GEOM_SCREEN = _vsp.NGON_MESH_GEOM_SCREEN
        r""" NGon Mesh geom screen"""
        self.STACK_GEOM_SCREEN = _vsp.STACK_GEOM_SCREEN
        r""" Stack geom screen"""
        self.CUSTOM_GEOM_SCREEN = _vsp.CUSTOM_GEOM_SCREEN
        r""" Custom geom screen"""
        self.PT_CLOUD_GEOM_SCREEN = _vsp.PT_CLOUD_GEOM_SCREEN
        r""" Point cloud geom screen"""
        self.PROP_GEOM_SCREEN = _vsp.PROP_GEOM_SCREEN
        r""" Propeller geom screen"""
        self.HINGE_GEOM_SCREEN = _vsp.HINGE_GEOM_SCREEN
        r""" Hinge geom screen"""
        self.MULT_GEOM_SCREEN = _vsp.MULT_GEOM_SCREEN
        r""" Multiple geom screen"""
        self.CONFORMAL_SCREEN = _vsp.CONFORMAL_SCREEN
        r""" Conformal geom screen"""
        self.ELLIPSOID_GEOM_SCREEN = _vsp.ELLIPSOID_GEOM_SCREEN
        r""" Ellipsoid geom screen"""
        self.BOR_GEOM_SCREEN = _vsp.BOR_GEOM_SCREEN
        r""" Body of revolution geom screen"""
        self.WIRE_FRAME_GEOM_SCREEN = _vsp.WIRE_FRAME_GEOM_SCREEN
        r""" Wireframe geom screen"""
        self.HUMAN_GEOM_SCREEN = _vsp.HUMAN_GEOM_SCREEN
        r""" Human geom screen"""
        self.ROUTING_GEOM_SCREEN = _vsp.ROUTING_GEOM_SCREEN
        r""" Routing geom screen"""
        self.AUXILIARY_GEOM_SCREEN = _vsp.AUXILIARY_GEOM_SCREEN
        r""" Auxiliary geom screen"""
        self.GEAR_GEOM_SCREEN = _vsp.GEAR_GEOM_SCREEN
        r""" Gear geom screen"""
        self.NUM_GEOM_SCREENS = _vsp.NUM_GEOM_SCREENS
        r""" Number of geom screens"""
        self.ALL_GEOM_SCREENS = _vsp.ALL_GEOM_SCREENS
        r""" All geom screens"""
        self.VSP_ADV_LINK_SCREEN = _vsp.VSP_ADV_LINK_SCREEN
        r""" Advanced linking screen"""
        self.VSP_ADV_LINK_VAR_RENAME_SCREEN = _vsp.VSP_ADV_LINK_VAR_RENAME_SCREEN
        r""" Advanced link variable rename screen"""
        self.VSP_AERO_STRUCT_SCREEN = _vsp.VSP_AERO_STRUCT_SCREEN
        r""" Aero / structural analysis screen"""
        self.VSP_AIRFOIL_CURVES_EXPORT_SCREEN = _vsp.VSP_AIRFOIL_CURVES_EXPORT_SCREEN
        r""" Airfoil curves export screen"""
        self.VSP_AIRFOIL_POINTS_EXPORT_SCREEN = _vsp.VSP_AIRFOIL_POINTS_EXPORT_SCREEN
        r""" Airfoil points screen"""
        self.VSP_ATTRIBUTE_EXPLORER_SCREEN = _vsp.VSP_ATTRIBUTE_EXPLORER_SCREEN
        r""" Attribute details screen"""
        self.VSP_BACKGROUND_SCREEN = _vsp.VSP_BACKGROUND_SCREEN
        r""" Background control screen"""
        self.VSP_BACKGROUND3D_SCREEN = _vsp.VSP_BACKGROUND3D_SCREEN
        r""" Background3D control screen"""
        self.VSP_BACKGROUND3D_PREVIEW_SCREEN = _vsp.VSP_BACKGROUND3D_PREVIEW_SCREEN
        r""" Background3D preview screen"""
        self.VSP_BEM_OPTIONS_SCREEN = _vsp.VSP_BEM_OPTIONS_SCREEN
        r""" Blade element method options screen"""
        self.VSP_CFD_MESH_SCREEN = _vsp.VSP_CFD_MESH_SCREEN
        r""" CFD Mesh screen"""
        self.VSP_CLIPPING_SCREEN = _vsp.VSP_CLIPPING_SCREEN
        r""" Clipping screen"""
        self.VSP_COMP_GEOM_SCREEN = _vsp.VSP_COMP_GEOM_SCREEN
        r""" CompGeom screen"""
        self.VSP_COR_SCREEN = _vsp.VSP_COR_SCREEN
        r""" Center of rotation screen"""
        self.VSP_CURVE_EDIT_SCREEN = _vsp.VSP_CURVE_EDIT_SCREEN
        r""" Curve edit screen"""
        self.VSP_DEGEN_GEOM_SCREEN = _vsp.VSP_DEGEN_GEOM_SCREEN
        r""" Degen geom screen"""
        self.VSP_DESIGN_VAR_SCREEN = _vsp.VSP_DESIGN_VAR_SCREEN
        r""" Design variables screen"""
        self.VSP_DXF_OPTIONS_SCREEN = _vsp.VSP_DXF_OPTIONS_SCREEN
        r""" DXF options screen"""
        self.VSP_EXPORT_SCREEN = _vsp.VSP_EXPORT_SCREEN
        r""" Export screen"""
        self.VSP_FEA_PART_EDIT_SCREEN = _vsp.VSP_FEA_PART_EDIT_SCREEN
        r""" FEA Part edit screen"""
        self.VSP_FEA_XSEC_SCREEN = _vsp.VSP_FEA_XSEC_SCREEN
        r""" FEA XSec screen"""
        self.VSP_FIT_MODEL_SCREEN = _vsp.VSP_FIT_MODEL_SCREEN
        r""" Fit model screen"""
        self.VSP_IGES_OPTIONS_SCREEN = _vsp.VSP_IGES_OPTIONS_SCREEN
        r""" IGES options screen"""
        self.VSP_IGES_STRUCTURE_OPTIONS_SCREEN = _vsp.VSP_IGES_STRUCTURE_OPTIONS_SCREEN
        r""" IGES structure options screen"""
        self.VSP_EXPORT_CUSTOM_SCRIPT = _vsp.VSP_EXPORT_CUSTOM_SCRIPT
        r""" Custom geom export screen"""
        self.VSP_GEOMETRY_ANALYSIS_SCREEN = _vsp.VSP_GEOMETRY_ANALYSIS_SCREEN
        r""" Geometry analysis screen"""
        self.VSP_IMPORT_SCREEN = _vsp.VSP_IMPORT_SCREEN
        r""" Import screen"""
        self.VSP_LIGHTING_SCREEN = _vsp.VSP_LIGHTING_SCREEN
        r""" Lighting screen"""
        self.VSP_MANAGE_GEOM_SCREEN = _vsp.VSP_MANAGE_GEOM_SCREEN
        r""" Manage geom screen"""
        self.VSP_MANAGE_TEXTURE_SCREEN = _vsp.VSP_MANAGE_TEXTURE_SCREEN
        r""" Texture mapping screen"""
        self.VSP_MASS_PROP_SCREEN = _vsp.VSP_MASS_PROP_SCREEN
        r""" Mass properties screen"""
        self.VSP_MATERIAL_EDIT_SCREEN = _vsp.VSP_MATERIAL_EDIT_SCREEN
        r""" Material edit screen"""
        self.VSP_MEASURE_SCREEN = _vsp.VSP_MEASURE_SCREEN
        r""" Measure screen"""
        self.VSP_MODE_EDITOR_SCREEN = _vsp.VSP_MODE_EDITOR_SCREEN
        r""" Mode editor screen"""
        self.VSP_NERF_MANAGE_GEOM_SCREEN = _vsp.VSP_NERF_MANAGE_GEOM_SCREEN
        r""" NERF'ed (limited to make safe) Manage geom screen"""
        self.VSP_SNAP_TO_SCREEN = _vsp.VSP_SNAP_TO_SCREEN
        r""" Snap to screen"""
        self.VSP_PARASITE_DRAG_SCREEN = _vsp.VSP_PARASITE_DRAG_SCREEN
        r""" Parasite drg screen"""
        self.VSP_PARM_DEBUG_SCREEN = _vsp.VSP_PARM_DEBUG_SCREEN
        r""" Parameter debug screen"""
        self.VSP_PARM_LINK_SCREEN = _vsp.VSP_PARM_LINK_SCREEN
        r""" Parameter linking screen"""
        self.VSP_PARM_SCREEN = _vsp.VSP_PARM_SCREEN
        r""" Parameter screen"""
        self.VSP_PICK_SET_SCREEN = _vsp.VSP_PICK_SET_SCREEN
        r""" Pick set screen"""
        self.VSP_PREFERENCES_SCREEN = _vsp.VSP_PREFERENCES_SCREEN
        r""" Preferences screen"""
        self.VSP_PROJECTION_SCREEN = _vsp.VSP_PROJECTION_SCREEN
        r""" Projected area screen"""
        self.VSP_PSLICE_SCREEN = _vsp.VSP_PSLICE_SCREEN
        r""" Planar slicing screen"""
        self.VSP_RESULTS_VIEWER_SCREEN = _vsp.VSP_RESULTS_VIEWER_SCREEN
        r""" Results viewing screen"""
        self.VSP_SCREENSHOT_SCREEN = _vsp.VSP_SCREENSHOT_SCREEN
        r""" Screenshot screen"""
        self.VSP_SELECT_FILE_SCREEN = _vsp.VSP_SELECT_FILE_SCREEN
        r""" Select file screen"""
        self.VSP_SET_EDITOR_SCREEN = _vsp.VSP_SET_EDITOR_SCREEN
        r""" Set editor screen"""
        self.VSP_STEP_OPTIONS_SCREEN = _vsp.VSP_STEP_OPTIONS_SCREEN
        r""" STEP options screen"""
        self.VSP_STEP_STRUCTURE_OPTIONS_SCREEN = _vsp.VSP_STEP_STRUCTURE_OPTIONS_SCREEN
        r""" STEP structure options screen"""
        self.VSP_STL_OPTIONS_SCREEN = _vsp.VSP_STL_OPTIONS_SCREEN
        r""" STL options screen"""
        self.VSP_STRUCT_SCREEN = _vsp.VSP_STRUCT_SCREEN
        r""" Structure definition screen"""
        self.VSP_STRUCT_ASSEMBLY_SCREEN = _vsp.VSP_STRUCT_ASSEMBLY_SCREEN
        r""" Structure assembly screen"""
        self.VSP_SURFACE_INTERSECTION_SCREEN = _vsp.VSP_SURFACE_INTERSECTION_SCREEN
        r""" Surface intersection screen"""
        self.VSP_SVG_OPTIONS_SCREEN = _vsp.VSP_SVG_OPTIONS_SCREEN
        r""" SVG options screen"""
        self.VSP_USER_PARM_SCREEN = _vsp.VSP_USER_PARM_SCREEN
        r""" User parameter screen"""
        self.VSP_VAR_PRESET_SCREEN = _vsp.VSP_VAR_PRESET_SCREEN
        r""" Variable presets editor screen"""
        self.VSP_VEH_NOTES_SCREEN = _vsp.VSP_VEH_NOTES_SCREEN
        r""" Vehicle notes screen"""
        self.VSP_VEH_SCREEN = _vsp.VSP_VEH_SCREEN
        r""" Veh geom screen"""
        self.VSP_VIEW_SCREEN = _vsp.VSP_VIEW_SCREEN
        r""" Adjust viewpoint screen"""
        self.VSP_VSPAERO_PLOT_SCREEN = _vsp.VSP_VSPAERO_PLOT_SCREEN
        r""" VSPAERO results manager screen"""
        self.VSP_VSPAERO_SCREEN = _vsp.VSP_VSPAERO_SCREEN
        r""" VSPAERO screen"""
        self.VSP_XSEC_SCREEN = _vsp.VSP_XSEC_SCREEN
        r""" XSec screen"""
        self.VSP_WAVEDRAG_SCREEN = _vsp.VSP_WAVEDRAG_SCREEN
        r""" Wave drag screen"""
        self.VSP_MAIN_SCREEN = _vsp.VSP_MAIN_SCREEN
        r""" Main screen"""
        self.VSP_NUM_SCREENS = _vsp.VSP_NUM_SCREENS
        r""" Number of screens"""
        self.VSP_ALL_SCREENS = _vsp.VSP_ALL_SCREENS
        r""" Flag for all screens"""
        self.EDIT_XSEC_CIRCLE = _vsp.EDIT_XSEC_CIRCLE
        r""" Circle initialized as cubic Bezier type"""
        self.EDIT_XSEC_ELLIPSE = _vsp.EDIT_XSEC_ELLIPSE
        r""" Ellipse initialized as PCHIP type"""
        self.EDIT_XSEC_RECTANGLE = _vsp.EDIT_XSEC_RECTANGLE
        r""" Rectangle initialized as linear type"""
        self.NUM_INIT_EDIT_XSEC_TYPES = _vsp.NUM_INIT_EDIT_XSEC_TYPES
        r""" Number of initializable edit curve types"""
        self.IMPORT_STL = _vsp.IMPORT_STL
        r""" Stereolith (*.stl) import"""
        self.IMPORT_NASCART = _vsp.IMPORT_NASCART
        r""" NASCART (*.dat) import"""
        self.IMPORT_CART3D_TRI = _vsp.IMPORT_CART3D_TRI
        r""" Cart3D (*.try) import"""
        self.IMPORT_XSEC_MESH = _vsp.IMPORT_XSEC_MESH
        r""" XSec as Tri Mesh (*.hrm) import"""
        self.IMPORT_PTS = _vsp.IMPORT_PTS
        r""" Point Cloud (*.pts) import"""
        self.IMPORT_V2 = _vsp.IMPORT_V2
        r""" OpenVSP v2 (*.vsp) import"""
        self.IMPORT_BEM = _vsp.IMPORT_BEM
        r""" Blade Element (*.bem) import"""
        self.IMPORT_XSEC_WIRE = _vsp.IMPORT_XSEC_WIRE
        r""" XSec as Wireframe (*.hrm) import"""
        self.IMPORT_P3D_WIRE = _vsp.IMPORT_P3D_WIRE
        r""" Plot3D as Wireframe (*.p3d) import"""
        self.INTERSECT_SRF_FILE_NAME = _vsp.INTERSECT_SRF_FILE_NAME
        r""" SRF intersection file type"""
        self.INTERSECT_CURV_FILE_NAME = _vsp.INTERSECT_CURV_FILE_NAME
        r""" CURV intersection file type"""
        self.INTERSECT_PLOT3D_FILE_NAME = _vsp.INTERSECT_PLOT3D_FILE_NAME
        r""" PLOT3D intersection file type"""
        self.INTERSECT_IGES_FILE_NAME = _vsp.INTERSECT_IGES_FILE_NAME
        r""" IGES intersection file type"""
        self.INTERSECT_STEP_FILE_NAME = _vsp.INTERSECT_STEP_FILE_NAME
        r""" STEP intersection file type"""
        self.INTERSECT_NUM_FILE_NAMES = _vsp.INTERSECT_NUM_FILE_NAMES
        r""" Number of surface intersection file types"""
        self.LEN_MM = _vsp.LEN_MM
        r""" Millimeter"""
        self.LEN_CM = _vsp.LEN_CM
        r""" Centimeter"""
        self.LEN_M = _vsp.LEN_M
        r""" Meter"""
        self.LEN_IN = _vsp.LEN_IN
        r""" Inch"""
        self.LEN_FT = _vsp.LEN_FT
        r""" Feet"""
        self.LEN_YD = _vsp.LEN_YD
        r""" Yard"""
        self.LEN_UNITLESS = _vsp.LEN_UNITLESS
        r""" Unitless"""
        self.NUM_LEN_UNIT = _vsp.NUM_LEN_UNIT
        r""" Number of length unit types"""
        self.MASS_UNIT_G = _vsp.MASS_UNIT_G
        r""" Gram"""
        self.MASS_UNIT_KG = _vsp.MASS_UNIT_KG
        r""" Kilogram"""
        self.MASS_UNIT_TONNE = _vsp.MASS_UNIT_TONNE
        r""" Tonne"""
        self.MASS_UNIT_LBM = _vsp.MASS_UNIT_LBM
        r""" Pound-mass"""
        self.MASS_UNIT_SLUG = _vsp.MASS_UNIT_SLUG
        r""" Slug"""
        self.MASS_LBFSEC2IN = _vsp.MASS_LBFSEC2IN
        r""" lbf*sec^2/in"""
        self.NUM_MASS_UNIT = _vsp.NUM_MASS_UNIT
        r""" Number of mass unit types"""
        self.NO_REASON = _vsp.NO_REASON
        r""" No reason determined."""
        self.MAX_LEN_CONSTRAINT = _vsp.MAX_LEN_CONSTRAINT
        r""" Maximum edge length."""
        self.CURV_GAP = _vsp.CURV_GAP
        r""" Maximum gap curvature based criteria."""
        self.CURV_NCIRCSEG = _vsp.CURV_NCIRCSEG
        r""" Minimum number of segments to define a circle curvature based criteria."""
        self.SOURCES = _vsp.SOURCES
        r""" Mesh sources."""
        self.MIN_LEN_CONSTRAINT = _vsp.MIN_LEN_CONSTRAINT
        r""" Minimum edge length."""
        self.MIN_LEN_CONSTRAINT_CURV_GAP = _vsp.MIN_LEN_CONSTRAINT_CURV_GAP
        r""" Maximum gap constrained by minimum length."""
        self.MIN_LEN_CONSTRAINT_CURV_NCIRCSEG = _vsp.MIN_LEN_CONSTRAINT_CURV_NCIRCSEG
        r""" Number of segments to define a circle constrained by minimum length."""
        self.MIN_LEN_CONSTRAINT_SOURCES = _vsp.MIN_LEN_CONSTRAINT_SOURCES
        r""" Mesh sources constrained by minimum length (not applied)."""
        self.GROW_LIMIT_MAX_LEN_CONSTRAINT = _vsp.GROW_LIMIT_MAX_LEN_CONSTRAINT
        r""" Maximum growth limit from maximum edge length (not used, growth limited small to large)."""
        self.GROW_LIMIT_CURV_GAP = _vsp.GROW_LIMIT_CURV_GAP
        r""" Maximum growth limit from maximum gap."""
        self.GROW_LIMIT_CURV_NCIRCSEG = _vsp.GROW_LIMIT_CURV_NCIRCSEG
        r""" Maximum growth limit from number of segments to define a circle."""
        self.GROW_LIMIT_SOURCES = _vsp.GROW_LIMIT_SOURCES
        r""" Maximum growth limit from mesh sources."""
        self.GROW_LIMIT_MIN_LEN_CONSTRAINT = _vsp.GROW_LIMIT_MIN_LEN_CONSTRAINT
        r""" Maximum growth limit from minimum length constraint."""
        self.GROW_LIMIT_MIN_LEN_CONSTRAINT_CURV_GAP = _vsp.GROW_LIMIT_MIN_LEN_CONSTRAINT_CURV_GAP
        r""" Maximum growth limit from maximum gap constrained by minimum length."""
        self.GROW_LIMIT_MIN_LEN_CONSTRAINT_CURV_NCIRCSEG = _vsp.GROW_LIMIT_MIN_LEN_CONSTRAINT_CURV_NCIRCSEG
        r""" Maximum growth limit from number of segments to define a circle constrained by minimum length."""
        self.GROW_LIMIT_MIN_LEN_CONSTRAINT_SOURCES = _vsp.GROW_LIMIT_MIN_LEN_CONSTRAINT_SOURCES
        r""" Maximum growth limit from sources constrained by minimum length."""
        self.NUM_MESH_REASON = _vsp.NUM_MESH_REASON
        r""" Number of reasons that can set the mesh local minimum edge length."""
        self.MIN_LEN_INCREMENT = _vsp.MIN_LEN_INCREMENT
        r""" Reason increment when adding minimum length constraint."""
        self.GROW_LIMIT_INCREMENT = _vsp.GROW_LIMIT_INCREMENT
        r""" Reason increment when adding growth limit constraint."""
        self.MIN_GROW_LIMIT = _vsp.MIN_GROW_LIMIT
        r""" Reason marker for minimum reason to apply growth limit."""
        self.ID_LENGTH_PRESET_GROUP = _vsp.ID_LENGTH_PRESET_GROUP
        r""" ID for Var Preset Groups are length 5"""
        self.ID_LENGTH_PRESET_SETTING = _vsp.ID_LENGTH_PRESET_SETTING
        r""" ID for Var Preset Settings are length 6"""
        self.ID_LENGTH_ATTR = _vsp.ID_LENGTH_ATTR
        r""" ID for Attributes are length 8"""
        self.ID_LENGTH_ATTRCOLL = _vsp.ID_LENGTH_ATTRCOLL
        r""" ID for Attribute Collections are length 9"""
        self.ID_LENGTH_PARMCONTAINER = _vsp.ID_LENGTH_PARMCONTAINER
        r""" ID for Parm Containers are length 10"""
        self.ID_LENGTH_PARM = _vsp.ID_LENGTH_PARM
        r""" ID for Parms are length 11"""
        self.TRI_MESH_TYPE = _vsp.TRI_MESH_TYPE
        r""" Triangle mesh"""
        self.QUAD_MESH_TYPE = _vsp.QUAD_MESH_TYPE
        r""" Quadrilateral mesh"""
        self.NGON_MESH_TYPE = _vsp.NGON_MESH_TYPE
        r""" N-gon mesh"""
        self.NUM_MESH_TYPE = _vsp.NUM_MESH_TYPE
        r""" Number of mesh types"""
        self.PARM_DOUBLE_TYPE = _vsp.PARM_DOUBLE_TYPE
        r""" Double Parm type (Parm)"""
        self.PARM_INT_TYPE = _vsp.PARM_INT_TYPE
        r""" Integer Parm type (IntParm)"""
        self.PARM_BOOL_TYPE = _vsp.PARM_BOOL_TYPE
        r""" Bool Parm type (BoolParm)"""
        self.PARM_FRACTION_TYPE = _vsp.PARM_FRACTION_TYPE
        r""" Fraction Parm type (FractionParm)"""
        self.PARM_LIMITED_INT_TYPE = _vsp.PARM_LIMITED_INT_TYPE
        r""" Limited integer Parm type (LimIntParm)"""
        self.PARM_NOTEQ_TYPE = _vsp.PARM_NOTEQ_TYPE
        r""" Not equal Parm type (NotEqParm)"""
        self.PARM_POWER_INT_TYPE = _vsp.PARM_POWER_INT_TYPE
        r""" Power integer Parm type (PowIntParm)"""
        self.PATCH_NONE = _vsp.PATCH_NONE
        r""" No patch"""
        self.PATCH_POINT = _vsp.PATCH_POINT
        r""" Point patch type"""
        self.PATCH_LINE = _vsp.PATCH_LINE
        r""" Line patch type"""
        self.PATCH_COPY = _vsp.PATCH_COPY
        r""" Copy patch type"""
        self.PATCH_HALFWAY = _vsp.PATCH_HALFWAY
        r""" Halfway patch type"""
        self.PATCH_NUM_TYPES = _vsp.PATCH_NUM_TYPES
        r""" Number of patch types"""
        self.LINEAR = _vsp.LINEAR
        r""" Linear curve type"""
        self.PCHIP = _vsp.PCHIP
        r""" Piecewise Cubic Hermite Interpolating Polynomial curve type"""
        self.CEDIT = _vsp.CEDIT
        r""" Cubic Bezier curve type"""
        self.APPROX_CEDIT = _vsp.APPROX_CEDIT
        r""" Approximate curve as Cubic Bezier"""
        self.NUM_PCURV_TYPE = _vsp.NUM_PCURV_TYPE
        r""" Number of curve types"""
        self.PRES_UNIT_PSF = _vsp.PRES_UNIT_PSF
        r""" Pounds per square foot"""
        self.PRES_UNIT_PSI = _vsp.PRES_UNIT_PSI
        r""" Pounds per square inch"""
        self.PRES_UNIT_BA = _vsp.PRES_UNIT_BA
        r""" Barye"""
        self.PRES_UNIT_PA = _vsp.PRES_UNIT_PA
        r""" Pascal"""
        self.PRES_UNIT_KPA = _vsp.PRES_UNIT_KPA
        r""" Kilopascal"""
        self.PRES_UNIT_MPA = _vsp.PRES_UNIT_MPA
        r""" Megapascal"""
        self.PRES_UNIT_INCHHG = _vsp.PRES_UNIT_INCHHG
        r""" Inch of mercury"""
        self.PRES_UNIT_MMHG = _vsp.PRES_UNIT_MMHG
        r""" Millimeter of mercury"""
        self.PRES_UNIT_MMH20 = _vsp.PRES_UNIT_MMH20
        r""" Millimeter of water"""
        self.PRES_UNIT_MB = _vsp.PRES_UNIT_MB
        r""" Millibar"""
        self.PRES_UNIT_ATM = _vsp.PRES_UNIT_ATM
        r""" Atmosphere"""
        self.NUM_PRES_UNIT = _vsp.NUM_PRES_UNIT
        r""" Number of pressure unit choices"""
        self.NO_BOUNDARY = _vsp.NO_BOUNDARY
        r""" No boundary"""
        self.SET_BOUNDARY = _vsp.SET_BOUNDARY
        r""" Set boundary"""
        self.GEOM_BOUNDARY = _vsp.GEOM_BOUNDARY
        r""" Geom boundary"""
        self.NUM_PROJ_BNDY_OPTIONS = _vsp.NUM_PROJ_BNDY_OPTIONS
        r""" Number of projected area boundary options"""
        self.X_PROJ = _vsp.X_PROJ
        r""" Project in X axis direction"""
        self.Y_PROJ = _vsp.Y_PROJ
        r""" Project in Y axis direction"""
        self.Z_PROJ = _vsp.Z_PROJ
        r""" Project in Z axis direction"""
        self.GEOM_PROJ = _vsp.GEOM_PROJ
        r""" Project toward a Geom"""
        self.VEC_PROJ = _vsp.VEC_PROJ
        r""" Project along a 3D vector"""
        self.NUM_PROJ_DIR_OPTIONS = _vsp.NUM_PROJ_DIR_OPTIONS
        r""" Number of Projected Area direction types"""
        self.SET_TARGET = _vsp.SET_TARGET
        r""" Set target type"""
        self.GEOM_TARGET = _vsp.GEOM_TARGET
        r""" Geom target type"""
        self.MODE_TARGET = _vsp.MODE_TARGET
        r""" Mode target type"""
        self.Z_TARGET = _vsp.Z_TARGET
        r""" Z plane target type"""
        self.XYZ_TARGET = _vsp.XYZ_TARGET
        r""" XYZ point target type"""
        self.NUM_PROJ_TGT_OPTIONS = _vsp.NUM_PROJ_TGT_OPTIONS
        r""" Number of Projected Area target types"""
        self.PROP_AZI_UNIFORM = _vsp.PROP_AZI_UNIFORM
        r""" Propeller blades are uniformly spaced"""
        self.PROP_AZI_FREE = _vsp.PROP_AZI_FREE
        r""" Propeller blades are free to spaced arbitrarially"""
        self.PROP_AZI_BALANCED = _vsp.PROP_AZI_BALANCED
        r""" Propeller blade balance is enforced"""
        self.NUM_PROP_AZI = _vsp.NUM_PROP_AZI
        r""" Number of propeller blade azimuth modes"""
        self.RPM_PROP_DRIVER = _vsp.RPM_PROP_DRIVER
        r""" RPM driver"""
        self.CT_PROP_DRIVER = _vsp.CT_PROP_DRIVER
        r""" Thrust coefficient driver"""
        self.CP_PROP_DRIVER = _vsp.CP_PROP_DRIVER
        r""" Power coefficient driver"""
        self.T_PROP_DRIVER = _vsp.T_PROP_DRIVER
        r""" Thrust driver"""
        self.ETA_PROP_DRIVER = _vsp.ETA_PROP_DRIVER
        r""" Prop efficiency driver"""
        self.J_PROP_DRIVER = _vsp.J_PROP_DRIVER
        r""" Advance ratio driver"""
        self.P_PROP_DRIVER = _vsp.P_PROP_DRIVER
        r""" Power driver"""
        self.CQ_PROP_DRIVER = _vsp.CQ_PROP_DRIVER
        r""" Torque coefficient driver"""
        self.Q_PROP_DRIVER = _vsp.Q_PROP_DRIVER
        r""" Torque driver"""
        self.NUM_PROP_DRIVER = _vsp.NUM_PROP_DRIVER
        r""" Number of actuator disk drivers"""
        self.PROP_BLADES = _vsp.PROP_BLADES
        r""" Propeller Geom is defined by individual propeller blades"""
        self.PROP_BOTH = _vsp.PROP_BOTH
        r""" Propeller Geom is defined by blades and a disk together"""
        self.PROP_DISK = _vsp.PROP_DISK
        r""" Propeller Geom is defined by a flat circular disk"""
        self.PROP_CHORD = _vsp.PROP_CHORD
        r""" Chord parameterization"""
        self.PROP_TWIST = _vsp.PROP_TWIST
        r""" Twist parameterization"""
        self.PROP_RAKE = _vsp.PROP_RAKE
        r""" Rake parameterization"""
        self.PROP_SKEW = _vsp.PROP_SKEW
        r""" Skew parameterization"""
        self.PROP_SWEEP = _vsp.PROP_SWEEP
        r""" Sweep parameterization"""
        self.PROP_THICK = _vsp.PROP_THICK
        r""" Thickness parameterization"""
        self.PROP_CLI = _vsp.PROP_CLI
        r""" Induced lift coefficient parameterization"""
        self.PROP_AXIAL = _vsp.PROP_AXIAL
        r""" Axial parameterization"""
        self.PROP_TANGENTIAL = _vsp.PROP_TANGENTIAL
        r""" Tangential parameterization"""
        self.NUM_PROP_PCURVE = _vsp.NUM_PROP_PCURVE
        r""" Number of propeller blade curve parameterization options"""
        self.REORDER_MOVE_UP = _vsp.REORDER_MOVE_UP
        r""" Move up one position"""
        self.REORDER_MOVE_DOWN = _vsp.REORDER_MOVE_DOWN
        r""" Move down one position"""
        self.REORDER_MOVE_TOP = _vsp.REORDER_MOVE_TOP
        r""" Move to top"""
        self.REORDER_MOVE_BOTTOM = _vsp.REORDER_MOVE_BOTTOM
        r""" Move to bottom"""
        self.NUM_REORDER_TYPES = _vsp.NUM_REORDER_TYPES
        r""" Number reordering instructions"""
        self.MANUAL_REF = _vsp.MANUAL_REF
        r""" Manually specify the reference areas and lengths"""
        self.COMPONENT_REF = _vsp.COMPONENT_REF
        r""" Use a particular wing to calculate the reference area and lengths"""
        self.NUM_REF_TYPES = _vsp.NUM_REF_TYPES
        r""" Number of wing reference types"""
        self.INVALID_TYPE = _vsp.INVALID_TYPE
        r""" Invalid data type"""
        self.BOOL_DATA = _vsp.BOOL_DATA
        r""" Bool data type"""
        self.INT_DATA = _vsp.INT_DATA
        r""" Integer data type"""
        self.DOUBLE_DATA = _vsp.DOUBLE_DATA
        r""" Double data type"""
        self.STRING_DATA = _vsp.STRING_DATA
        r""" String data type"""
        self.VEC3D_DATA = _vsp.VEC3D_DATA
        r""" Vec3d data type"""
        self.INT_MATRIX_DATA = _vsp.INT_MATRIX_DATA
        r""" Int matrix data type"""
        self.DOUBLE_MATRIX_DATA = _vsp.DOUBLE_MATRIX_DATA
        r""" Double matrix data type"""
        self.ATTR_COLLECTION_DATA = _vsp.ATTR_COLLECTION_DATA
        r""" Attribute collection data type"""
        self.PARM_REFERENCE_DATA = _vsp.PARM_REFERENCE_DATA
        r""" Parm reference data type"""
        self.MESH_INDEXED_TRI = _vsp.MESH_INDEXED_TRI
        r""" Indexed triangulated mesh Geom type"""
        self.MESH_SLICE_TRI = _vsp.MESH_SLICE_TRI
        r""" Sliced Triangulated mesh Geom type"""
        self.GEOM_XSECS = _vsp.GEOM_XSECS
        r""" GeomXSec Geom type"""
        self.MESH_INDEX_AND_SLICE_TRI = _vsp.MESH_INDEX_AND_SLICE_TRI
        r""" Both indexed and sliced triangulated mesh Geom type"""
        self.RHO_UNIT_SLUG_FT3 = _vsp.RHO_UNIT_SLUG_FT3
        r""" Slug per cubic foot"""
        self.RHO_UNIT_G_CM3 = _vsp.RHO_UNIT_G_CM3
        r""" Gram per cubic centimeter"""
        self.RHO_UNIT_KG_M3 = _vsp.RHO_UNIT_KG_M3
        r""" Kilogram per cubic meter"""
        self.RHO_UNIT_TONNE_MM3 = _vsp.RHO_UNIT_TONNE_MM3
        r""" Tonne per cubic millimeter"""
        self.RHO_UNIT_LBM_FT3 = _vsp.RHO_UNIT_LBM_FT3
        r""" Pound-mass per cubic foot"""
        self.RHO_UNIT_LBFSEC2_IN4 = _vsp.RHO_UNIT_LBFSEC2_IN4
        r""" Pound-force-second squared per inch to the fourth"""
        self.RHO_UNIT_LBM_IN3 = _vsp.RHO_UNIT_LBM_IN3
        r""" Pound-mass per cubic inch"""
        self.NUM_RHO_UNIT = _vsp.NUM_RHO_UNIT
        r""" Number of density unit options"""
        self.ROUTE_PT_COMP = _vsp.ROUTE_PT_COMP
        r""" Routing point relative to parent body axes"""
        self.ROUTE_PT_UV = _vsp.ROUTE_PT_UV
        r""" Routing point relative to parent surface coordinate frame"""
        self.ROUTE_PT_RST = _vsp.ROUTE_PT_RST
        r""" Routing point relative to parent per-section volume coordinate frame"""
        self.ROUTE_PT_LMN = _vsp.ROUTE_PT_LMN
        r""" Routing point relative to parent uniform volume coordinate frame"""
        self.ROUTE_PT_EtaMN = _vsp.ROUTE_PT_EtaMN
        r""" Routing point relative to wing parent uniform eta volume coordinate frame"""
        self.ROUTE_PT_NUM_TYPES = _vsp.ROUTE_PT_NUM_TYPES
        r""" Number of routing point coordinate types"""
        self.ROUTE_PT_DELTA_XYZ = _vsp.ROUTE_PT_DELTA_XYZ
        r""" Routing point ofset in global axes"""
        self.ROUTE_PT_DELTA_COMP = _vsp.ROUTE_PT_DELTA_COMP
        r""" Routing point offset in parent body frame"""
        self.ROUTE_PT_DELTA_UVN = _vsp.ROUTE_PT_DELTA_UVN
        r""" Routing point offset in parent surface coordinate frame"""
        self.ROUTE_PT_DELTA_NUM_TYPES = _vsp.ROUTE_PT_DELTA_NUM_TYPES
        r""" Number of routing point offset coordinate types"""
        self.SCALE_WIDTH = _vsp.SCALE_WIDTH
        r""" Scale image to match desired width"""
        self.SCALE_HEIGHT = _vsp.SCALE_HEIGHT
        r""" Scale image to match desired height"""
        self.SCALE_WIDTH_HEIGHT = _vsp.SCALE_WIDTH_HEIGHT
        r""" Scale image to match desired width and height"""
        self.SCALE_RESOLUTION = _vsp.SCALE_RESOLUTION
        r""" Scale image to specified resolution"""
        self.NUM_SCALE_TYPES = _vsp.NUM_SCALE_TYPES
        r""" Number of ways to scale 3D background image."""
        self.SET_NONE = _vsp.SET_NONE
        r""" None set"""
        self.SET_ALL = _vsp.SET_ALL
        r""" All set"""
        self.SET_SHOWN = _vsp.SET_SHOWN
        r""" Shown set"""
        self.SET_NOT_SHOWN = _vsp.SET_NOT_SHOWN
        r""" Not shown set"""
        self.SET_FIRST_USER = _vsp.SET_FIRST_USER
        r""" First user-defined set"""
        self.MIN_NUM_USER = _vsp.MIN_NUM_USER
        r""" Minimum number of user sets"""
        self.MAX_NUM_SETS = _vsp.MAX_NUM_SETS
        r""" Maximum possible number of sets"""
        self.STEP_SHELL = _vsp.STEP_SHELL
        r""" Manifold shell surface STEP file representation"""
        self.STEP_BREP = _vsp.STEP_BREP
        r""" Manifold solid BREP STEP file representation"""
        self.SS_INC_TREAT_AS_PARENT = _vsp.SS_INC_TREAT_AS_PARENT
        r""" Treat the sub-surface the same as the parent"""
        self.SS_INC_SEPARATE_TREATMENT = _vsp.SS_INC_SEPARATE_TREATMENT
        r""" Treat the sub-surface separately from the parent"""
        self.SS_INC_ZERO_DRAG = _vsp.SS_INC_ZERO_DRAG
        r""" No drag contribution for the sub-surface"""
        self.INSIDE = _vsp.INSIDE
        r""" The interior of the sub-surface is its surface"""
        self.OUTSIDE = _vsp.OUTSIDE
        r""" The exterior of the sub-surface is its surface"""
        self.NONE = _vsp.NONE
        r""" No part of the parent surface belongs to the sub-surface"""
        self.CONST_U = _vsp.CONST_U
        r""" Constant U sub-surface"""
        self.CONST_W = _vsp.CONST_W
        r""" Constant W sub-surface"""
        self.SS_LINE = _vsp.SS_LINE
        r""" Line sub-surface type"""
        self.SS_RECTANGLE = _vsp.SS_RECTANGLE
        r""" Rectangle sub-surface type"""
        self.SS_ELLIPSE = _vsp.SS_ELLIPSE
        r""" Ellipse sub-surface type"""
        self.SS_CONTROL = _vsp.SS_CONTROL
        r""" Control sub-surface type"""
        self.SS_LINE_ARRAY = _vsp.SS_LINE_ARRAY
        r""" Line array sub-surface type"""
        self.SS_FINITE_LINE = _vsp.SS_FINITE_LINE
        r""" Finite line sub-surface type"""
        self.SS_XSEC_CURVE = _vsp.SS_XSEC_CURVE
        r""" XSecCurve based sub-surface type"""
        self.SS_NUM_TYPES = _vsp.SS_NUM_TYPES
        r""" Number of sub-surface types"""
        self.SYM_XY = _vsp.SYM_XY
        r""" XY planar symmetry."""
        self.SYM_XZ = _vsp.SYM_XZ
        r""" XZ planar symmetry."""
        self.SYM_YZ = _vsp.SYM_YZ
        r""" YZ planar symmetry."""
        self.SYM_ROT_X = _vsp.SYM_ROT_X
        r""" X rotational symmetry."""
        self.SYM_ROT_Y = _vsp.SYM_ROT_Y
        r""" Y rotational symmetry."""
        self.SYM_ROT_Z = _vsp.SYM_ROT_Z
        r""" Z rotational symmetry."""
        self.SYM_PLANAR_TYPES = _vsp.SYM_PLANAR_TYPES
        r""" Number of planar symmetry types."""
        self.SYM_NUM_TYPES = _vsp.SYM_NUM_TYPES
        r""" Number of symmetry types."""
        self.SYM_NONE = _vsp.SYM_NONE
        r""" No cross section symmetry."""
        self.SYM_RL = _vsp.SYM_RL
        r""" Right/left cross section symmetry."""
        self.SYM_TB = _vsp.SYM_TB
        r""" Top/bottom cross section symmetry."""
        self.SYM_ALL = _vsp.SYM_ALL
        r""" All cross section symmetry."""
        self.TEMP_UNIT_K = _vsp.TEMP_UNIT_K
        r""" Kelvin"""
        self.TEMP_UNIT_C = _vsp.TEMP_UNIT_C
        r""" Celsius"""
        self.TEMP_UNIT_F = _vsp.TEMP_UNIT_F
        r""" Fahrenheit"""
        self.TEMP_UNIT_R = _vsp.TEMP_UNIT_R
        r""" Rankine"""
        self.NUM_TEMP_UNIT = _vsp.NUM_TEMP_UNIT
        r""" Number of temperature unit choices"""
        self.TIRE_STATIC_LODED_CONTACT = _vsp.TIRE_STATIC_LODED_CONTACT
        r""" Tire static loaded radius"""
        self.TIRE_NOMINAL_CONTACT = _vsp.TIRE_NOMINAL_CONTACT
        r""" Tire nominal radius"""
        self.TIRE_GROWTH_CONTACT = _vsp.TIRE_GROWTH_CONTACT
        r""" Tire growth (spinning) radius"""
        self.TIRE_FLAT_CONTACT = _vsp.TIRE_FLAT_CONTACT
        r""" Tire flat tire radius"""
        self.NUM_TIRE_CONTACT_MODES = _vsp.NUM_TIRE_CONTACT_MODES
        r""" Number of tire radius modes"""
        self.TIRE_DIM_IN = _vsp.TIRE_DIM_IN
        r""" Tire dimensions in inches"""
        self.TIRE_DIM_MODEL = _vsp.TIRE_DIM_MODEL
        r""" Tire dimensions in model units"""
        self.TIRE_DIM_FRAC = _vsp.TIRE_DIM_FRAC
        r""" Tire dimensions as fractions"""
        self.NUM_TIRE_DIM_MODES = _vsp.NUM_TIRE_DIM_MODES
        r""" Number of tire dimension choices"""
        self.TIRE_TRA = _vsp.TIRE_TRA
        r""" Full TRA model"""
        self.TIRE_FAIR_FLANGE = _vsp.TIRE_FAIR_FLANGE
        r""" TRA with faired flange / flank"""
        self.TIRE_FAIR_WHEEL = _vsp.TIRE_FAIR_WHEEL
        r""" TRA with faired wheel"""
        self.TIRE_BALLOON = _vsp.TIRE_BALLOON
        r""" Balloon tire"""
        self.TIRE_BALLOON_WHEEL = _vsp.TIRE_BALLOON_WHEEL
        r""" Balloon tire with wheel"""
        self.TIRE_BALLOON_FAIR_WHEEL = _vsp.TIRE_BALLOON_FAIR_WHEEL
        r""" Balloon tire with faired wheel"""
        self.NUM_TIRE_MODES = _vsp.NUM_TIRE_MODES
        r""" Number of tire choices"""
        self.V_UNIT_FT_S = _vsp.V_UNIT_FT_S
        r""" Feet per second"""
        self.V_UNIT_M_S = _vsp.V_UNIT_M_S
        r""" Meter per second"""
        self.V_UNIT_MPH = _vsp.V_UNIT_MPH
        r""" Mile per hour"""
        self.V_UNIT_KM_HR = _vsp.V_UNIT_KM_HR
        r""" Kilometer per hour"""
        self.V_UNIT_KEAS = _vsp.V_UNIT_KEAS
        r""" Knots equivalent airspeed"""
        self.V_UNIT_KTAS = _vsp.V_UNIT_KTAS
        r""" Knots true airspeed"""
        self.V_UNIT_MACH = _vsp.V_UNIT_MACH
        r""" Mach"""
        self.VIEW_1 = _vsp.VIEW_1
        r""" One 2D view"""
        self.VIEW_2HOR = _vsp.VIEW_2HOR
        r""" Two horizontal 2D views"""
        self.VIEW_2VER = _vsp.VIEW_2VER
        r""" Two vertical 2D views"""
        self.VIEW_4 = _vsp.VIEW_4
        r""" Four 2D views"""
        self.ROT_0 = _vsp.ROT_0
        r""" No rotation"""
        self.ROT_90 = _vsp.ROT_90
        r""" 90 degree rotation"""
        self.ROT_180 = _vsp.ROT_180
        r""" 180 degree rotation"""
        self.ROT_270 = _vsp.ROT_270
        r""" 270 degree rotation"""
        self.VIEW_LEFT = _vsp.VIEW_LEFT
        r""" Left 2D view type"""
        self.VIEW_RIGHT = _vsp.VIEW_RIGHT
        r""" Right 2D view type"""
        self.VIEW_TOP = _vsp.VIEW_TOP
        r""" Top 2D view type"""
        self.VIEW_BOTTOM = _vsp.VIEW_BOTTOM
        r""" Bottom 2D view type"""
        self.VIEW_FRONT = _vsp.VIEW_FRONT
        r""" Front 2D view type"""
        self.VIEW_REAR = _vsp.VIEW_REAR
        r""" Rear 2D view type"""
        self.VIEW_NONE = _vsp.VIEW_NONE
        r""" No 2D view type"""
        self.VIEW_NUM_TYPES = _vsp.VIEW_NUM_TYPES
        r""" Number of 2D view types"""
        self.NOISE_FLYBY = _vsp.NOISE_FLYBY
        r""" Set up fly by noise analysis in VSPAERO for PSU-WOPWOP"""
        self.NOISE_FOOTPRINT = _vsp.NOISE_FOOTPRINT
        r""" Set up footprint noise analysis in VSPAERO for PSU-WOPWOP"""
        self.NOISE_STEADY = _vsp.NOISE_STEADY
        r""" Set up steady state noise analysis in VSPAERO for PSU-WOPWOP"""
        self.NOISE_SI = _vsp.NOISE_SI
        r""" Assume geometry and VSPAERO inputs in SI (m N kg s) for PSU-WOPWOP"""
        self.NOISE_ENGLISH = _vsp.NOISE_ENGLISH
        r""" Assume geometry and VSPAERO inputs in english (ft lbf slug s) units, will convert to SI (m N kg s) for PSU-WOPWOP"""
        self.VSPAERO_PROP_STATIC = _vsp.VSPAERO_PROP_STATIC
        r""" Model propellers as static, non-rotating blades -- i.e. used as a wing."""
        self.VSPAERO_PROP_UNSTEADY = _vsp.VSPAERO_PROP_UNSTEADY
        r""" Model propellers as unsteady rotating blades"""
        self.VSPAERO_PROP_PSEUDO_STEADY = _vsp.VSPAERO_PROP_PSEUDO_STEADY
        r""" Model propellers with pseudo steady model"""
        self.VSPAERO_PROP_NUM_MODES = _vsp.VSPAERO_PROP_NUM_MODES
        r""" Number of ways to model propeller blades in VSPAERO"""
        self.STABILITY_OFF = _vsp.STABILITY_OFF
        r""" No stability analysis (off)"""
        self.STABILITY_DEFAULT = _vsp.STABILITY_DEFAULT
        r""" Steady 6DOF stability analysis"""
        self.STABILITY_P_ANALYSIS = _vsp.STABILITY_P_ANALYSIS
        r""" Unsteady roll stability analysis"""
        self.STABILITY_Q_ANALYSIS = _vsp.STABILITY_Q_ANALYSIS
        r""" Unsteady pitch stability analysis"""
        self.STABILITY_R_ANALYSIS = _vsp.STABILITY_R_ANALYSIS
        r""" Unsteady yaw stability analysis"""
        self.STABILITY_PITCH = _vsp.STABILITY_PITCH
        r""" Simplified pitch stability analysis"""
        self.STABILITY_ADJOINT = _vsp.STABILITY_ADJOINT
        r""" Steady 6DOF stability analysis using adjoint"""
        self.STABILITY_NUM_TYPES = _vsp.STABILITY_NUM_TYPES
        r""" Number of stability analysis types"""
        self.STALL_OFF = _vsp.STALL_OFF
        r""" Stall modeling off"""
        self.STALL_ON = _vsp.STALL_ON
        r""" Stall modeling on"""
        self.CFD_NORMAL = _vsp.CFD_NORMAL
        r""" Normal CFD Mesh surface"""
        self.CFD_NEGATIVE = _vsp.CFD_NEGATIVE
        r""" Negative volume CFD Mesh surface"""
        self.CFD_TRANSPARENT = _vsp.CFD_TRANSPARENT
        r""" Transparent CFD Mesh surface"""
        self.CFD_STRUCTURE = _vsp.CFD_STRUCTURE
        r""" FEA structure CFD Mesh surface"""
        self.CFD_STIFFENER = _vsp.CFD_STIFFENER
        r""" FEA stiffener CFD Mesh surface"""
        self.CFD_MEASURE_DUCT = _vsp.CFD_MEASURE_DUCT
        r""" Measure duct cross sectional area surface"""
        self.CFD_NUM_TYPES = _vsp.CFD_NUM_TYPES
        r""" Number of CFD Mesh surface types"""
        self.NORMAL_SURF = _vsp.NORMAL_SURF
        r""" Normal VSP surface"""
        self.WING_SURF = _vsp.WING_SURF
        r""" Wing VSP surface"""
        self.DISK_SURF = _vsp.DISK_SURF
        r""" Disk VSP surface"""
        self.NUM_SURF_TYPES = _vsp.NUM_SURF_TYPES
        r""" Number of VSP surface types"""
        self.W_RIGHT_0 = _vsp.W_RIGHT_0
        r""" Chevron start/ends at right (W = 0) of cross section"""
        self.W_BOTTOM = _vsp.W_BOTTOM
        r""" Chevron start/ends at bottom of cross section"""
        self.W_LEFT = _vsp.W_LEFT
        r""" Chevron start/ends at left of cross section"""
        self.W_TOP = _vsp.W_TOP
        r""" Chevron start/ends at top of cross section"""
        self.W_RIGHT_1 = _vsp.W_RIGHT_1
        r""" Chevron start/ends at right (W = 1) of cross section"""
        self.W_FREE = _vsp.W_FREE
        r""" Chevron start/ends at user specified point on cross section"""
        self.BLEND_FREE = _vsp.BLEND_FREE
        r""" Free blending"""
        self.BLEND_ANGLES = _vsp.BLEND_ANGLES
        r""" Blend based on angles (sweep & dihedral)"""
        self.BLEND_MATCH_IN_LE_TRAP = _vsp.BLEND_MATCH_IN_LE_TRAP
        r""" Match inboard leading edge trapezoid"""
        self.BLEND_MATCH_IN_TE_TRAP = _vsp.BLEND_MATCH_IN_TE_TRAP
        r""" Match inboard trailing edge trapezoid"""
        self.BLEND_MATCH_OUT_LE_TRAP = _vsp.BLEND_MATCH_OUT_LE_TRAP
        r""" Match outboard leading edge trapezoid"""
        self.BLEND_MATCH_OUT_TE_TRAP = _vsp.BLEND_MATCH_OUT_TE_TRAP
        r""" Match outboard trailing edge trapezoid"""
        self.BLEND_MATCH_IN_ANGLES = _vsp.BLEND_MATCH_IN_ANGLES
        r""" Match inboard angles"""
        self.BLEND_MATCH_LE_ANGLES = _vsp.BLEND_MATCH_LE_ANGLES
        r""" Match leading edge angles"""
        self.BLEND_NUM_TYPES = _vsp.BLEND_NUM_TYPES
        r""" Number of blending types"""
        self.AR_WSECT_DRIVER = _vsp.AR_WSECT_DRIVER
        r""" Aspect ratio driver"""
        self.SPAN_WSECT_DRIVER = _vsp.SPAN_WSECT_DRIVER
        r""" Span driver"""
        self.AREA_WSECT_DRIVER = _vsp.AREA_WSECT_DRIVER
        r""" Area driver"""
        self.TAPER_WSECT_DRIVER = _vsp.TAPER_WSECT_DRIVER
        r""" Taper driver"""
        self.AVEC_WSECT_DRIVER = _vsp.AVEC_WSECT_DRIVER
        r""" Average chord driver"""
        self.ROOTC_WSECT_DRIVER = _vsp.ROOTC_WSECT_DRIVER
        r""" Root chord driver"""
        self.TIPC_WSECT_DRIVER = _vsp.TIPC_WSECT_DRIVER
        r""" Tip chord driver"""
        self.SECSWEEP_WSECT_DRIVER = _vsp.SECSWEEP_WSECT_DRIVER
        r""" Section sweep driver"""
        self.NUM_WSECT_DRIVER = _vsp.NUM_WSECT_DRIVER
        r""" Number of wing section drivers"""
        self.SWEEP_WSECT_DRIVER = _vsp.SWEEP_WSECT_DRIVER
        self.SWEEPLOC_WSECT_DRIVER = _vsp.SWEEPLOC_WSECT_DRIVER
        self.SECSWEEPLOC_WSECT_DRIVER = _vsp.SECSWEEPLOC_WSECT_DRIVER
        self.XDDM_VAR = _vsp.XDDM_VAR
        r""" Variable XDDM type"""
        self.XDDM_CONST = _vsp.XDDM_CONST
        r""" Constant XDDM type"""
        self.CLOSE_NONE = _vsp.CLOSE_NONE
        r""" No closure"""
        self.CLOSE_SKEWLOW = _vsp.CLOSE_SKEWLOW
        r""" Skew lower closure"""
        self.CLOSE_SKEWUP = _vsp.CLOSE_SKEWUP
        r""" Skew upper closure"""
        self.CLOSE_SKEWBOTH = _vsp.CLOSE_SKEWBOTH
        r""" Skew both closure"""
        self.CLOSE_EXTRAP = _vsp.CLOSE_EXTRAP
        r""" Extrapolate closure"""
        self.CLOSE_NUM_TYPES = _vsp.CLOSE_NUM_TYPES
        r""" Number of XSec closure types"""
        self.XS_UNDEFINED = _vsp.XS_UNDEFINED
        self.XS_POINT = _vsp.XS_POINT
        r""" Point XSec"""
        self.XS_CIRCLE = _vsp.XS_CIRCLE
        r""" Circle XSec"""
        self.XS_ELLIPSE = _vsp.XS_ELLIPSE
        r""" Ellipse XSec"""
        self.XS_SUPER_ELLIPSE = _vsp.XS_SUPER_ELLIPSE
        r""" Super ellipse XSec"""
        self.XS_ROUNDED_RECTANGLE = _vsp.XS_ROUNDED_RECTANGLE
        r""" Rounded rectangle XSec"""
        self.XS_GENERAL_FUSE = _vsp.XS_GENERAL_FUSE
        r""" General fuselage XSec"""
        self.XS_FILE_FUSE = _vsp.XS_FILE_FUSE
        r""" Fuselage file XSec"""
        self.XS_FOUR_SERIES = _vsp.XS_FOUR_SERIES
        r""" Four series XSec"""
        self.XS_SIX_SERIES = _vsp.XS_SIX_SERIES
        r""" Six series XSec"""
        self.XS_BICONVEX = _vsp.XS_BICONVEX
        r""" Biconvex XSec"""
        self.XS_WEDGE = _vsp.XS_WEDGE
        r""" Wedge XSec"""
        self.XS_EDIT_CURVE = _vsp.XS_EDIT_CURVE
        r""" Generic Edit Curve XSec"""
        self.XS_FILE_AIRFOIL = _vsp.XS_FILE_AIRFOIL
        r""" Airfoil file XSec"""
        self.XS_CST_AIRFOIL = _vsp.XS_CST_AIRFOIL
        r""" CST airfoil XSec"""
        self.XS_VKT_AIRFOIL = _vsp.XS_VKT_AIRFOIL
        r""" VKT airfoil XSec"""
        self.XS_FOUR_DIGIT_MOD = _vsp.XS_FOUR_DIGIT_MOD
        r""" Four digit modified XSec"""
        self.XS_FIVE_DIGIT = _vsp.XS_FIVE_DIGIT
        r""" Five digit XSec"""
        self.XS_FIVE_DIGIT_MOD = _vsp.XS_FIVE_DIGIT_MOD
        r""" Five digit modified XSec"""
        self.XS_ONE_SIX_SERIES = _vsp.XS_ONE_SIX_SERIES
        r""" One six series XSec"""
        self.XS_AC25_773 = _vsp.XS_AC25_773
        r""" FAA AC 25.773 pilot view requirement"""
        self.XS_NUM_TYPES = _vsp.XS_NUM_TYPES
        r""" Number of XSec types"""
        self.WIDTH_XSEC_DRIVER = _vsp.WIDTH_XSEC_DRIVER
        r""" Width driver"""
        self.AREA_XSEC_DRIVER = _vsp.AREA_XSEC_DRIVER
        r""" Area driver"""
        self.HEIGHT_XSEC_DRIVER = _vsp.HEIGHT_XSEC_DRIVER
        r""" Height driver"""
        self.HWRATIO_XSEC_DRIVER = _vsp.HWRATIO_XSEC_DRIVER
        r""" Height/width ratio driver"""
        self.NUM_XSEC_DRIVER = _vsp.NUM_XSEC_DRIVER
        r""" Number of XSec drivers"""
        self.CIRCLE_NUM_XSEC_DRIVER = _vsp.CIRCLE_NUM_XSEC_DRIVER
        self.FLAP_NONE = _vsp.FLAP_NONE
        r""" No flap"""
        self.FLAP_PLAIN = _vsp.FLAP_PLAIN
        r""" Plain flap"""
        self.FLAP_NUM_TYPES = _vsp.FLAP_NUM_TYPES
        r""" Number of flap types"""
        self.XSEC_BOTH_SIDES = _vsp.XSEC_BOTH_SIDES
        r""" Both sides"""
        self.XSEC_LEFT_SIDE = _vsp.XSEC_LEFT_SIDE
        r""" Left side"""
        self.XSEC_RIGHT_SIDE = _vsp.XSEC_RIGHT_SIDE
        r""" Right side"""
        self.TRIM_NONE = _vsp.TRIM_NONE
        r""" No trimming"""
        self.TRIM_X = _vsp.TRIM_X
        r""" Trim XSec by X"""
        self.TRIM_THICK = _vsp.TRIM_THICK
        r""" Trim XSec by thickness"""
        self.TRIM_NUM_TYPES = _vsp.TRIM_NUM_TYPES
        r""" Number of trimming types"""
        self.XSEC_FUSE = _vsp.XSEC_FUSE
        r""" Fuselage XSec Geom"""
        self.XSEC_STACK = _vsp.XSEC_STACK
        r""" Stack XSec Geom"""
        self.XSEC_WING = _vsp.XSEC_WING
        r""" Wing XSec Geom"""
        self.XSEC_CUSTOM = _vsp.XSEC_CUSTOM
        r""" Custom XSec Geom"""
        self.XSEC_PROP = _vsp.XSEC_PROP
        r""" Propeller XSec Geom"""
        self.XSEC_NUM_TYPES = _vsp.XSEC_NUM_TYPES
        r""" Number of XSec types"""
        self.XS_SHIFT_LE = _vsp.XS_SHIFT_LE
        r""" Shift leading edge"""
        self.XS_SHIFT_MID = _vsp.XS_SHIFT_MID
        self.XS_SHIFT_TE = _vsp.XS_SHIFT_TE
        # Register ErrorObj in _vsp:
        # Register ErrorMgrSingleton in _vsp:
        
    @client_wrap
    def VSPCheckSetup(self, ):
        r"""
        Check if OpenVSP has been initialized successfully. If not, the OpenVSP instance will be exited. This call should be placed at the
        beginning of all API scripts.
    
    
        .. code-block:: python
    
    
            VSPCheckSetup()
    
            # Continue to do things...
    
    
    
        """
        return _vsp.VSPCheckSetup()
    
    @client_wrap
    def VSPRenew(self, ):
        r"""
        Clear and reinitialize OpenVSP to all default settings
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            SetParmVal( pod_id, "Y_Rel_Location", "XForm", 2.0 )
    
            VSPRenew()
    
            if  len(FindGeoms()) != 0 : print( "ERROR: VSPRenew" )
    
    
        """
        return _vsp.VSPRenew()
    
    @client_wrap
    def Update(self, update_managers=True):
        r"""
        Update the entire vehicle and all lower level children. An input, which is true by default, is available to specify
        if managers should be updated as well. The managers are typically updated by their respective GUI, so must be
        updated through the API as well to avoid unexpected behavior.
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf
    
            num_xsecs = GetNumXSec( xsec_surf )
    
            #==== Set Tan Angles At Nose/Tail
            SetXSecTanAngles( GetXSec( xsec_surf, 0 ), XSEC_BOTH_SIDES, 90, -1.0e12, -1.0e12, -1.0e12 )
            SetXSecTanAngles( GetXSec( xsec_surf, num_xsecs - 1 ), XSEC_BOTH_SIDES, -90, -1.0e12, -1.0e12, -1.0e12 )
    
            Update()       # Force Surface Update
    
    
        :type update_managers: boolean, optional
        :param update_managers: Flag to indicate if managers should be updated
        """
        return _vsp.Update(update_managers)
    
    @client_wrap
    def VSPExit(self, error_code):
        r"""
        Exit the program with a specific error code
        :param [in]: error_code Error code
        """
        return _vsp.VSPExit(error_code)
    
    @client_wrap
    def VSPCrash(self, crash_type):
        r"""
        Cause OpenVSP to crash in a variety of ways.
        :param [in]: crash_type int Type of crash to attempt.
        """
        return _vsp.VSPCrash(crash_type)
    
    @client_wrap
    def GetAndResetUpdateCount(self, ):
        r"""
        Return the OpenVSP update count and also reset it to zero.
    
        The OpenVSP update count tracks how many times the GUI has been told to update screens (set to dirty).  It
        provides a simple means of testing whether the OpenVSP state has possibly changed (non-zero returned).
    
        :rtype: int
        :return: int OpenVSP update count
        """
        return _vsp.GetAndResetUpdateCount()
    
    @client_wrap
    def GetVSPVersion(self, ):
        r"""
        Get the version of the OpenVSP instance currently running
    
    
        .. code-block:: python
    
            print( "The current OpenVSP version is: ", False )
    
            print( GetVSPVersion() )
    
    
        :rtype: string
        :return: OpenVSP version string (i.e. "OpenVSP 3.17.1")
        """
        return _vsp.GetVSPVersion()
    
    @client_wrap
    def GetVSPVersionMajor(self, ):
        r"""
        Get the major version of the OpenVSP instance currently running as an integer
    
    
        .. code-block:: python
    
            print( "The current OpenVSP version is: ", False )
    
            major = GetVSPVersionMajor()
            minor = GetVSPVersionMinor()
            change = GetVSPVersionChange()
    
            print( f"{major}.{minor}.{change}" )
    
    
        :rtype: int
        :return: OpenVSP major version number (i.e. 3 in 3.X.Y)
        """
        return _vsp.GetVSPVersionMajor()
    
    @client_wrap
    def GetVSPVersionMinor(self, ):
        r"""
        Get the minor version of the OpenVSP instance currently running as an integer
    
    
        .. code-block:: python
    
            print( "The current OpenVSP version is: ", False )
    
            major = GetVSPVersionMajor()
            minor = GetVSPVersionMinor()
            change = GetVSPVersionChange()
    
            print( f"{major}.{minor}.{change}" )
    
    
        :rtype: int
        :return: OpenVSP minor version number (i.e. X in 3.X.Y)
        """
        return _vsp.GetVSPVersionMinor()
    
    @client_wrap
    def GetVSPVersionChange(self, ):
        r"""
        Get the change version of the OpenVSP instance currently running as an integer
    
    
        .. code-block:: python
    
            print( "The current OpenVSP version is: ", False )
    
            major = GetVSPVersionMajor()
            minor = GetVSPVersionMinor()
            change = GetVSPVersionChange()
    
            print( f"{major}.{minor}.{change}" )
    
    
        :rtype: int
        :return: OpenVSP change version number (i.e. Y in 3.X.Y)
        """
        return _vsp.GetVSPVersionChange()
    
    @client_wrap
    def GetVSPExePath(self, ):
        r"""
        Get the path to the OpenVSP executable. OpenVSP will assume that the VSPAERO, VSPSLICER, and VSPVIEWER are in the same directory unless
        instructed otherwise.
    
    
        .. code-block:: python
    
            print( "The current VSP executable path is: ", False )
    
            print( GetVSPExePath() )
    
    
        See also: SetVSPAEROPath, CheckForVSPAERO, GetVSPAEROPath
        :rtype: string
        :return: Path to the OpenVSP executable
        """
        return _vsp.GetVSPExePath()
    
    @client_wrap
    def SetVSPAEROPath(self, path):
        r"""
        Set the path to the VSPAERO executables (Solver, Viewer, and Slicer). By default, OpenVSP will assume that the VSPAERO executables are in the
        same directory as the VSP executable. However, this may need to be changed when using certain API languages like MATLAB and Python. For example,
        Python may treat the location of the Python executable as the VSP executable path, so either the VSPAERO executable needs to be moved to the same
        directory or this function can be called to tell Python where to look for VSPAERO.
    
    
        .. code-block:: python
    
            if  not CheckForVSPAERO( GetVSPExePath() ) :
                vspaero_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5"
                SetVSPAEROPath( vspaero_path )
    
    
        See also: GetVSPExePath, CheckForVSPAERO, GetVSPAEROPath
        :param [in]: path Absolute path to directory containing VSPAERO executable
        :rtype: boolean
        :return: Flag that indicates whether or not the path was set correctly
        """
        return _vsp.SetVSPAEROPath(path)
    
    @client_wrap
    def GetVSPAEROPath(self, ):
        r"""
        Get the path that OpenVSP will use to look for all VSPAERO executables (Solver, Slicer, and Viewer) when attempting to execute
        VSPAERO. If the VSPAERO executables are not in this location, they must either be copied there or the VSPAERO path must be set
        using SetVSPAEROPath.
    
    
        .. code-block:: python
    
            if  not CheckForVSPAERO( GetVSPAEROPath() ) :
                print( "VSPAERO is not where OpenVSP thinks it is. I should move the VSPAERO executable or call SetVSPAEROPath." )
    
    
        See also: GetVSPExePath, CheckForVSPAERO, SetVSPAEROPath
        :rtype: string
        :return: Path OpenVSP will look for VSPAERO
        """
        return _vsp.GetVSPAEROPath()
    
    @client_wrap
    def CheckForVSPAERO(self, path):
        r"""
        Check if all VSPAERO executables (Solver, Viewer, and Slicer) are in a given directory. Note that this function will return false
        if only one or two VSPAERO executables are found. An error message will indicate the executables that are missing. This may be
        acceptable, as only the Solver is needed in all cases. The Viewer and Slicer may not be needed.
    
    
        .. code-block:: python
    
            vspaero_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5"
    
            if  CheckForVSPAERO( vspaero_path ) :
                SetVSPAEROPath( vspaero_path )
    
    
        See also: GetVSPExePath, GetVSPAEROPath, SetVSPAEROPath
        :param [in]: path Absolute path to check for VSPAERO executables
        :rtype: boolean
        :return: Flag that indicates if all VSPAERO executables are found or not
        """
        return _vsp.CheckForVSPAERO(path)
    
    @client_wrap
    def SetVSPHelpPath(self, path):
        r"""
        Set the path to the OpenVSP help files. By default, OpenVSP will assume that the OpenVSP help directory is in the
        same directory as the VSP executable. However, this may need to be changed when using certain API languages like MATLAB and Python. For example,
        Python may treat the location of the Python executable as the VSP executable path, so either the VSPAERO executable needs to be moved to the same
        directory or this function can be called to tell Python where to look for help.
    
    
        .. code-block:: python
    
            if  not CheckForVSPHelp( GetVSPExePath() ) :
                vsphelp_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5/help"
                SetVSPHelpPath( vsphelp_path )
    
    
        See also: GetVSPExePath, CheckForVSPHelp, GetVSPHelpPath
        :param [in]: path Absolute path to directory containing OpenVSP help files
        :rtype: boolean
        :return: Flag that indicates whether or not the path was set correctly
        """
        return _vsp.SetVSPHelpPath(path)
    
    @client_wrap
    def GetVSPHelpPath(self, ):
        r"""
        Get the path that OpenVSP will use to look for all OpenVSP help files. If the OpenVSP help files are not in this location,
        they must either be copied there or the VSPHelp path must be set using SetVSPHelpPath.
    
    
        .. code-block:: python
    
            if  not CheckForVSPHelp( GetVSPHelpPath() ) :
                print( "VSPAERO is not where OpenVSP thinks it is. I should move the VSPAERO executable or call SetVSPAEROPath." )
    
    
        See also: GetVSPExePath, CheckForVSPHelp, SetVSPHelpPath
        :rtype: string
        :return: Path OpenVSP will look for help files
        """
        return _vsp.GetVSPHelpPath()
    
    @client_wrap
    def CheckForVSPHelp(self, path):
        r"""
        Check if all OpenVSP help files are in a given directory.
    
    
        .. code-block:: python
    
            vsphelp_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5/help"
    
            if  CheckForVSPHelp( vsphelp_path ) :
                SetVSPHelpPath( vsphelp_path )
    
    
        See also: GetVSPExePath, GetVSPAEROPath, SetVSPHelpPath
        :param [in]: path Absolute path to check for VSPAERO executables
        :rtype: boolean
        :return: Flag that indicates if OpenVSP help files are found or not
        """
        return _vsp.CheckForVSPHelp(path)
    
    @client_wrap
    def RegisterCFDMeshAnalyses(self, ):
        r"""RegisterCFDMeshAnalyses()"""
        return _vsp.RegisterCFDMeshAnalyses()
    
    @client_wrap
    def ReadVSPFile(self, file_name):
        r"""
        Load an OpenVSP project from a VSP3 file
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            fname = "example_fuse.vsp3"
    
            SetVSP3FileName( fname )
    
            Update()
    
            #==== Save Vehicle to File ====//
            print( "\tSaving vehicle file to: ", False )
    
            print( fname )
    
            WriteVSPFile( GetVSPFileName(), SET_ALL )
    
            #==== Reset Geometry ====//
            print( "--->Resetting VSP model to blank slate\n" )
    
            ClearVSPModel()
    
            ReadVSPFile( fname )
    
    
        :param [in]: file_name *.vsp3 file name
        """
        return _vsp.ReadVSPFile(file_name)
    
    @client_wrap
    def WriteVSPFile(self, *args):
        r"""
        Save the current OpenVSP project to a VSP3 file
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            fname = "example_fuse.vsp3"
    
            SetVSP3FileName( fname )
    
            Update()
    
            #==== Save Vehicle to File ====//
            print( "\tSaving vehicle file to: ", False )
    
            print( fname )
    
            WriteVSPFile( GetVSPFileName(), SET_ALL )
    
            #==== Reset Geometry ====//
            print( "--->Resetting VSP model to blank slate\n" )
    
            ClearVSPModel()
    
            ReadVSPFile( fname )
    
    
        :param [in]: file_name *.vsp3 file name
        :param [in]: set Set index to write (i.e. SET_ALL)
        """
        return _vsp.WriteVSPFile(*args)
    
    @client_wrap
    def SetVSP3FileName(self, file_name):
        r"""
        Set the file name of a OpenVSP project
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            fname = "example_fuse.vsp3"
    
            SetVSP3FileName( fname )
    
            Update()
    
            #==== Save Vehicle to File ====//
            print( "\tSaving vehicle file to: ", False )
    
            print( fname )
    
            WriteVSPFile( GetVSPFileName(), SET_ALL )
    
            #==== Reset Geometry ====//
            print( "--->Resetting VSP model to blank slate\n" )
    
            ClearVSPModel()
    
            ReadVSPFile( fname )
    
    
        :param [in]: file_name File name
        """
        return _vsp.SetVSP3FileName(file_name)
    
    @client_wrap
    def GetVSPFileName(self, ):
        r"""
        Get the file name of the current OpenVSP project
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            fname = "example_fuse.vsp3"
    
            SetVSP3FileName( fname )
    
            Update()
    
            #==== Save Vehicle to File ====//
            print( "\tSaving vehicle file to: ", False )
    
            print( fname )
    
            WriteVSPFile( GetVSPFileName(), SET_ALL )
    
    
        :rtype: string
        :return: File name for the current OpenVSP project
        """
        return _vsp.GetVSPFileName()
    
    @client_wrap
    def ClearVSPModel(self, ):
        r"""
        Clear the current OpenVSP model
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            #==== Reset Geometry ====//
            print( "--->Resetting VSP model to blank slate\n" )
            ClearVSPModel()
    
    
        """
        return _vsp.ClearVSPModel()
    
    @client_wrap
    def InsertVSPFile(self, file_name, parent_geom_id):
        r"""
        Insert an external OpenVSP project into the current project. All Geoms in the external project are placed as children of the specified parent.
        If no parent or an invalid parent is given, the Geoms are inserted at the top level.
        :param [in]: file_name string *.vsp3 filename
        :param [in]: parent_geom_id string Parent geom ID (ignored with empty string)
        """
        return _vsp.InsertVSPFile(file_name, parent_geom_id)
    
    @client_wrap
    def ExportFile(self, *args):
        r"""
        Export a file from OpenVSP. Many formats are available, such as STL, IGES, and SVG. If a mesh is generated for a particular export,
        the ID of the MeshGeom will be returned. If no mesh is generated an empty string will be returned.
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING" )             # Add Wing
    
            ExportFile( "Airfoil_Metadata.csv", SET_ALL, EXPORT_SELIG_AIRFOIL )
    
            mesh_id = ExportFile( "Example_Mesh.msh", SET_ALL, EXPORT_GMSH )
            DeleteGeom( mesh_id ) # Delete the mesh generated by the GMSH export
    
    
        See also: EXPORT_TYPE
        :param [in]: file_name Export file name
        :param [in]: thick_set Set index to export (i.e. SET_ALL)
        :param [in]: file_type File type enum (i.e. EXPORT_IGES)
        :param [in]: subsFlag Flag to tag subsurfaces if MeshGeom is created
        :param [in]: thin_set Set index to export as degenerate geometry (i.e. SET_NONE)
        :param [in]: useMode bool Flag determine if mode is used instead of sets
        :param [in]: modeID string ID of Mode to use
        :rtype: string
        :return: Mesh Geom ID if the export generates a mesh
        """
        return _vsp.ExportFile(*args)
    
    @client_wrap
    def ImportFile(self, file_name, file_type, parent):
        r"""
        Import a file into OpenVSP. Many formats are available, such as NASCART, V2, and BEM). The imported Geom, mesh, or other object is inserted
        as a child of the specified parent. If no parent or an invalid parent is given, the import will be done at the top level.
        See also: IMPORT_TYPE
        :param [in]: file_name Import file name
        :param [in]: file_type File type enum (i.e. IMPORT_PTS)
        :param [in]: parent Parent Geom ID (ignored with empty string)
        """
        return _vsp.ImportFile(file_name, file_type, parent)
    
    @client_wrap
    def SetBEMPropID(self, prop_id):
        r"""
        Set the ID of the propeller to be exported to a BEM file. Call this function before ExportFile.
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            SetBEMPropID( prop_id )
    
            ExportFile( "ExampleBEM.bem", SET_ALL, EXPORT_BEM )
    
    
        See also: EXPORT_TYPE, ExportFile
        :param [in]: prop_id Propeller Geom ID
        """
        return _vsp.SetBEMPropID(prop_id)
    
    @client_wrap
    def ReadApplyDESFile(self, file_name):
        r"""
        Read in and apply a design file (*.des) to the current OpenVSP project
        :param [in]: file_name *.des input file
        """
        return _vsp.ReadApplyDESFile(file_name)
    
    @client_wrap
    def WriteDESFile(self, file_name):
        r"""
        Write all design variables to a design file (*.des)
        :param [in]: file_name *.des output file
        """
        return _vsp.WriteDESFile(file_name)
    
    @client_wrap
    def ReadApplyXDDMFile(self, file_name):
        r"""
        Read in and apply a Cart3D XDDM file (*.xddm) to the current OpenVSP project
        :param [in]: file_name *.xddm input file
        """
        return _vsp.ReadApplyXDDMFile(file_name)
    
    @client_wrap
    def WriteXDDMFile(self, file_name):
        r"""
        Write all design variables to a Cart3D XDDM file (*.xddm)
        :param [in]: file_name *.xddm output file
        """
        return _vsp.WriteXDDMFile(file_name)
    
    @client_wrap
    def GetNumDesignVars(self, ):
        r"""
        Get the number of design variables
        :rtype: int
        :return: int Number of design variables
        """
        return _vsp.GetNumDesignVars()
    
    @client_wrap
    def AddDesignVar(self, parm_id, type):
        r"""
        Add a design variable
        See also: XDDM_QUANTITY_TYPE
        :param [in]: parm_id string Parm ID
        :param [in]: type XDDM type enum (XDDM_VAR or XDDM_CONST)
        """
        return _vsp.AddDesignVar(parm_id, type)
    
    @client_wrap
    def DeleteAllDesignVars(self, ):
        r"""    Delete all design variables"""
        return _vsp.DeleteAllDesignVars()
    
    @client_wrap
    def GetDesignVar(self, index):
        r"""
        Get the Parm ID of the specified design variable
        :param [in]: index Index of design variable
        :rtype: string
        :return: Parm ID
        """
        return _vsp.GetDesignVar(index)
    
    @client_wrap
    def GetDesignVarType(self, index):
        r"""
        Get the XDDM type of the specified design variable
        See also: XDDM_QUANTITY_TYPE
        :param [in]: index Index of design variable
        :rtype: int
        :return: XDDM type enum (XDDM_VAR or XDDM_CONST)
        """
        return _vsp.GetDesignVarType(index)
    
    @client_wrap
    def SetComputationFileName(self, file_type, file_name):
        r"""
        Get the file name of a specified file type. Note, this function cannot be used to set FEA Mesh file names.
    
    
        .. code-block:: python
    
            #==== Set File Name ====//
            SetComputationFileName( DEGEN_GEOM_CSV_TYPE, "TestDegenScript.csv" )
    
            #==== Run Degen Geom ====//
            ComputeDegenGeom( SET_ALL, DEGEN_GEOM_CSV_TYPE )
    
    
        See also: COMPUTATION_FILE_TYPE, SetFeaMeshFileName
        :param [in]: file_type File type enum (i.e. CFD_TRI_TYPE, COMP_GEOM_TXT_TYPE)
        :param [in]: file_name File name
        """
        return _vsp.SetComputationFileName(file_type, file_name)
    
    @client_wrap
    def ComputeMassProps(self, set, num_slices, idir):
        r"""
        Compute mass properties for the components in the set. Alternatively can be run through the Analysis Manager with 'MassProp'.
    
    
        .. code-block:: python
    
            #==== Test Mass Props ====//
            pid = AddGeom( "POD", "" )
    
            mesh_id = ComputeMassProps( SET_ALL, 20, X_DIR )
    
            mass_res_id = FindLatestResultsID( "Mass_Properties" )
    
            double_arr = GetDoubleResults( mass_res_id, "Total_Mass" )
    
            if  len(double_arr) != 1 : print( "---> Error: API ComputeMassProps" )
    
    
        See also: SetAnalysisInputDefaults, PrintAnalysisInputs, ExecAnalysis
        :param [in]: set Set index (i.e. SET_ALL)
        :param [in]: num_slices Number of slices
        :param [in]: idir Direction of slicing for integration
        :rtype: string
        :return: MeshGeom ID
        """
        return _vsp.ComputeMassProps(set, num_slices, idir)
    
    @client_wrap
    def ComputeCompGeom(self, set, half_mesh, file_export_types):
        r"""
        Mesh, intersect, and trim components in the set. Alternatively can be run through the Analysis Manager with 'CompGeom'.
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            #==== Run CompGeom And Get Results ====//
            mesh_id = ComputeCompGeom( SET_ALL, False, 0 )                      # Half Mesh false and no file export
    
            comp_res_id = FindLatestResultsID( "Comp_Geom" )                    # Find Results ID
    
            double_arr = GetDoubleResults( comp_res_id, "Wet_Area" )    # Extract Results
    
    
        See also: SetAnalysisInputDefaults, PrintAnalysisInputs, ExecAnalysis, COMPUTATION_FILE_TYPE
        :param [in]: set Set index (i.e. SET_ALL)
        :param [in]: half_mesh Flag to ignore surfaces on the negative side of the XZ plane (e.g. symmetry)
        :param [in]: file_export_types CompGeom file type to export (supports XOR i.e. COMP_GEOM_CSV_TYPE & COMP_GEOM_TXT_TYPE )
        :rtype: string
        :return: MeshGeom ID
        """
        return _vsp.ComputeCompGeom(set, half_mesh, file_export_types)
    
    @client_wrap
    def ComputePlaneSlice(self, set, num_slices, norm, auto_bnd, start_bnd=0, end_bnd=0, measureduct=False):
        r"""
        Slice and mesh the components in the set. Alternatively can be run through the Analysis Manager with 'PlanarSlice'.
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            #==== Test Plane Slice ====//
            slice_mesh_id = ComputePlaneSlice( 0, 6, vec3d( 0.0, 0.0, 1.0 ), True )
    
            pslice_results = FindLatestResultsID( "Slice" )
    
            double_arr = GetDoubleResults( pslice_results, "Slice_Area" )
    
            if  len(double_arr) != 6 : print( "---> Error: API ComputePlaneSlice" )
    
    
        See also: SetAnalysisInputDefaults, PrintAnalysisInputs, ExecAnalysis
        :param [in]: set Set index (i.e. SET_ALL)
        :param [in]: num_slices Number of slices
        :param [in]: norm Normal axis for all slices
        :param [in]: auto_bnd Flag to automatically set the start and end bound locations
        :param [in]: start_bnd Location of the first slice along the normal axis (default: 0.0)
        :param [in]: end_bnd Location of the last slice along the normal axis (default: 0.0)
        :param [in]: measureduct Flag to measure negative area inside positive area (default: false)
        :rtype: string
        :return: MeshGeom ID
        """
        return _vsp.ComputePlaneSlice(set, num_slices, norm, auto_bnd, start_bnd, end_bnd, measureduct)
    
    @client_wrap
    def ComputeDegenGeom(self, set, file_export_types):
        r"""
        Compute the degenerate geometry representation for the components in the set. Alternatively can be run through the Analysis Manager with 'DegenGeom' or 'VSPAERODegenGeom'.
    
    
        .. code-block:: python
    
            #==== Set File Name ====//
            SetComputationFileName( DEGEN_GEOM_CSV_TYPE, "TestDegenScript.csv" )
    
            #==== Run Degen Geom ====//
            ComputeDegenGeom( SET_ALL, DEGEN_GEOM_CSV_TYPE )
    
    
        See also: SetAnalysisInputDefaults, PrintAnalysisInputs, ExecAnalysis, COMPUTATION_FILE_TYPE
        :param [in]: set int Set index (i.e. SET_ALL)
        :param [in]: file_export_types int DegenGeom file type to export (supports XOR i.e DEGEN_GEOM_M_TYPE & DEGEN_GEOM_CSV_TYPE)
        """
        return _vsp.ComputeDegenGeom(set, file_export_types)
    
    @client_wrap
    def ComputeCFDMesh(self, set, degenset, file_export_types):
        r"""
        Create a CFD Mesh for the components in the set. This analysis cannot be run through the Analysis Manager.
    
    
        .. code-block:: python
    
            #==== CFDMesh Method Facet Export =====//
            SetComputationFileName( CFD_FACET_TYPE, "TestCFDMeshFacet_API.facet" )
    
           print( "\tComputing CFDMesh..." )
    
            ComputeCFDMesh( SET_ALL, SET_NONE, CFD_FACET_TYPE )
    
    
        See also: COMPUTATION_FILE_TYPE
        :param [in]: set int Set index (i.e. SET_ALL)
        :param [in]: degenset int DegenSet index (i.e. SET_NONE)
        :param [in]: file_export_types int CFD Mesh file type to export (supports XOR i.e CFD_SRF_TYPE & CFD_STL_TYPE)
        """
        return _vsp.ComputeCFDMesh(set, degenset, file_export_types)
    
    @client_wrap
    def SetCFDMeshVal(self, type, val):
        r"""
        Set the value of a specific CFD Mesh option
    
    
        .. code-block:: python
    
            SetCFDMeshVal( CFD_MIN_EDGE_LEN, 1.0 )
    
    
        See also: CFD_CONTROL_TYPE
        :param [in]: type int CFD Mesh control type enum (i.e. CFD_GROWTH_RATIO)
        :param [in]: val double Value to set
        """
        return _vsp.SetCFDMeshVal(type, val)
    
    @client_wrap
    def SetCFDWakeFlag(self, geom_id, flag):
        r"""
        Activate or deactivate the CFD Mesh wake for a particular Geom. Note, the wake flag is only applicable for wing-type surfaces.
        Also, this function is simply an alternative to setting the value of the Parm with the available Parm setting API functions.
    
    
        .. code-block:: python
    
            #==== Add Wing Geom ====//
            wid = AddGeom( "WING", "" )
    
            SetCFDWakeFlag( wid, True )
            # This is equivalent to SetParmValUpdate( wid, "Wake", "Shape", 1.0 )
            # To change the scale: SetParmValUpdate( wid, "WakeScale", "WakeSettings", 10.0 )
            # To change the angle: SetParmValUpdate( wid, "WakeAngle", "WakeSettings", -5.0 )
    
    
        See also: SetParmVal, SetParmValUpdate
        :param [in]: geom_id string Geom ID
        :param [in]: flag True to activate, false to deactivate
        """
        return _vsp.SetCFDWakeFlag(geom_id, flag)
    
    @client_wrap
    def DeleteAllCFDSources(self, ):
        r"""
        Delete all CFD Mesh sources for all Geoms
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            AddCFDSource( POINT_SOURCE, pid, 0, 0.25, 2.0, 0.5, 0.5 )      # Add A Point Source
    
            DeleteAllCFDSources()
    
    
        """
        return _vsp.DeleteAllCFDSources()
    
    @client_wrap
    def AddDefaultSources(self, ):
        r"""
        Add default CFD Mesh sources for all Geoms
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            AddDefaultSources() # 3 Sources: Def_Fwd_PS, Def_Aft_PS, Def_Fwd_Aft_LS
    
    
        """
        return _vsp.AddDefaultSources()
    
    @client_wrap
    def AddCFDSource(self, type, geom_id, surf_index, l1, r1, u1, w1, l2=0, r2=0, u2=0, w2=0):
        r"""
        Add a CFD Mesh default source for the indicated Geom. Note, certain input params may not be used depending on the source type
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            AddCFDSource( POINT_SOURCE, pid, 0, 0.25, 2.0, 0.5, 0.5 )      # Add A Point Source
    
    
        See also: CFD_MESH_SOURCE_TYPE
        :param [in]: type CFD Mesh source type( i.e.BOX_SOURCE )
        :param [in]: geom_id string Geom ID
        :param [in]: surf_index Main surface index
        :param [in]: l1 Source first edge length
        :param [in]: r1 Source first radius
        :param [in]: u1 Source first U location
        :param [in]: w1 Source first W location
        :param [in]: l2 Source second edge length
        :param [in]: r2 Source second radius
        :param [in]: u2 Source second U location
        :param [in]: w2 Source second W location
        """
        return _vsp.AddCFDSource(type, geom_id, surf_index, l1, r1, u1, w1, l2, r2, u2, w2)
    
    @client_wrap
    def GetVSPAERORefWingID(self, ):
        r"""
        Get ID of the current VSPAERO reference Geom
        :rtype: string
        :return: Reference Geom ID
        """
        return _vsp.GetVSPAERORefWingID()
    
    @client_wrap
    def SetVSPAERORefWingID(self, geom_id):
        r"""
        Set the current VSPAERO reference Geom ID
    
    
        .. code-block:: python
    
            #==== Add Wing Geom and set some parameters =====//
            wing_id = AddGeom( "WING" )
    
            SetGeomName( wing_id, "MainWing" )
    
            #==== Add Vertical tail and set some parameters =====//
            vert_id = AddGeom( "WING" )
    
            SetGeomName( vert_id, "Vert" )
    
            SetParmValUpdate( vert_id, "TotalArea", "WingGeom", 10.0 )
            SetParmValUpdate( vert_id, "X_Rel_Location", "XForm", 8.5 )
            SetParmValUpdate( vert_id, "X_Rel_Rotation", "XForm", 90 )
    
            #==== Set VSPAERO Reference lengths & areas ====//
            SetVSPAERORefWingID( wing_id ) # Set as reference wing for VSPAERO
    
            print( "VSPAERO Reference Wing ID: ", False )
    
            print( GetVSPAERORefWingID() )
    
    
        :param [in]: geom_id Reference Geom ID
        """
        return _vsp.SetVSPAERORefWingID(geom_id)
    
    @client_wrap
    def GetNumAnalysis(self, ):
        r"""
        Get the number of analysis types available in the Analysis Manager
    
    
        .. code-block:: python
    
            nanalysis = GetNumAnalysis()
    
            print( f"Number of registered analyses: {nanalysis}" )
    
    
        :rtype: int
        :return: Number of analyses
        """
        return _vsp.GetNumAnalysis()
    
    @client_wrap
    def ListAnalysis(self, ):
        r"""
        Get the name of every available analysis in the Analysis Manager
    
    
        .. code-block:: python
    
            analysis_array = ListAnalysis()
    
            print( "List of Available Analyses: " )
    
            for i in range(int( len(analysis_array) )):
    
                print( "    " + analysis_array[i] )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of analysis names
        """
        return _vsp.ListAnalysis()
    
    @client_wrap
    def GetAnalysisInputNames(self, analysis):
        r"""
        Get the name of every available input for a particular analysis
    
    
        .. code-block:: python
    
            analysis_name = "VSPAEROComputeGeometry"
    
            in_names =  GetAnalysisInputNames( analysis_name )
    
            print("Analysis Inputs: ")
    
            for i in range(int( len(in_names) )):
    
                print( ( "\t" + in_names[i] + "\n" ) )
    
    
        :param [in]: analysis Analysis name
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of input names
        """
        return _vsp.GetAnalysisInputNames(analysis)
    
    @client_wrap
    def GetAnalysisDoc(self, analysis):
        r"""
        Get the analysis documentation string
    
    
        .. code-block:: python
    
            analysis_name = "VSPAEROComputeGeometry"
    
            doc = GetAnalysisDoc( analysis_name )
    
    
        :param [in]: analysis Analysis name
        :rtype: string
        :return: Documentation string
        """
        return _vsp.GetAnalysisDoc(analysis)
    
    @client_wrap
    def GetAnalysisInputDoc(self, analysis, name):
        r"""
        Get the documentation string for the particular analysis and input
    
    
    
    
        :param [in]: analysis Analysis name
        :param [in]: name Input name
        :rtype: string
        :return: Documentation string
        """
        return _vsp.GetAnalysisInputDoc(analysis, name)
    
    @client_wrap
    def ExecAnalysis(self, analysis):
        r"""
        Execute an analysis through the Analysis Manager
    
    
        .. code-block:: python
    
            analysis_name = "VSPAEROComputeGeometry"
    
            res_id = ExecAnalysis( analysis_name )
    
    
        :param [in]: analysis Analysis name
        :rtype: string
        :return: Result ID
        """
        return _vsp.ExecAnalysis(analysis)
    
    @client_wrap
    def GetNumAnalysisInputData(self, analysis, name):
        r"""
        Get the documentation string for the particular analysis and input
        :param [in]: analysis Analysis name
        :param [in]: name Input name
        :rtype: int
        :return: Documentation string
        """
        return _vsp.GetNumAnalysisInputData(analysis, name)
    
    @client_wrap
    def GetAnalysisInputType(self, analysis, name):
        r"""
        Get the data type for a particulat analysis type and input
    
    
        .. code-block:: python
    
            analysis = "VSPAEROComputeGeometry"
    
            inp_array = GetAnalysisInputNames( analysis )
    
            for j in range(int( len(inp_array) )):
    
                typ = GetAnalysisInputType( analysis, inp_array[j] )
    
    
        See also: RES_DATA_TYPE
        :param [in]: analysis Analysis name
        :param [in]: name Input name
        :rtype: int
        :return: int Data type enum (i.e. DOUBLE_DATA)
        """
        return _vsp.GetAnalysisInputType(analysis, name)
    
    @client_wrap
    def GetIntAnalysisInput(self, analysis, name, index=0):
        r"""
        Get the current integer values for the particular analysis, input, and data index
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # Set to panel method
            thick_set = GetIntAnalysisInput( analysis_name, "GeomSet" )
            thin_set = GetIntAnalysisInput( analysis_name, "ThinGeomSet" )
    
            thick_set = [vsp.SET_NONE]
            thin_set = [vsp.SET_ALL]
    
            SetIntAnalysisInput( analysis_name, "GeomSet", thick_set )
            SetIntAnalysisInput( analysis_name, "ThinGeomSet", thin_set )
    
    
        See also: RES_DATA_TYPE, SetIntAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: index int Data index
        :rtype: std::vector< int,std::allocator< int > >
        :return: vector<int> Array of analysis input values
        """
        return _vsp.GetIntAnalysisInput(analysis, name, index)
    
    @client_wrap
    def GetDoubleAnalysisInput(self, analysis, name, index=0):
        r"""
        Get the current double values for the particular analysis, input, and data index
    
    
        .. code-block:: python
    
            vinfFCinput = list( GetDoubleAnalysisInput( "ParasiteDrag", "Vinf" ) )
    
            vinfFCinput[0] = 629
    
            SetDoubleAnalysisInput( "ParasiteDrag", "Vinf", vinfFCinput )
    
    
        See also: RES_DATA_TYPE, SetDoubleAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: index int Data index
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Array of analysis input values
        """
        return _vsp.GetDoubleAnalysisInput(analysis, name, index)
    
    @client_wrap
    def GetStringAnalysisInput(self, analysis, name, index=0):
        r"""
        Get the current string values for the particular analysis, input, and data index
    
    
        .. code-block:: python
    
            fileNameInput = GetStringAnalysisInput( "ParasiteDrag", "FileName" )
    
            fileNameInput = ["ParasiteDragExample"]
    
            SetStringAnalysisInput( "ParasiteDrag", "FileName", fileNameInput )
    
    
        See also: RES_DATA_TYPE, SetStringAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: index int Data index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Array of analysis input values
        """
        return _vsp.GetStringAnalysisInput(analysis, name, index)
    
    @client_wrap
    def GetVec3dAnalysisInput(self, analysis, name, index=0):
        r"""
        Get the current vec3d values for the particular analysis, input, and data index
    
    
        .. code-block:: python
    
            # PlanarSlice
            norm = GetVec3dAnalysisInput( "PlanarSlice", "Norm" )
    
            norm[0].set_xyz( 0.23, 0.6, 0.15 )
    
            SetVec3dAnalysisInput( "PlanarSlice", "Norm", norm )
    
    
        See also: RES_DATA_TYPE, SetVec3dAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: index int Data index
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Array of analysis input values
        """
        return _vsp.GetVec3dAnalysisInput(analysis, name, index)
    
    @client_wrap
    def SetAnalysisInputDefaults(self, analysis):
        r"""
        Set all input values to their defaults for a specific analysis
    
    
         .. code-block:: python
    
             #==== Analysis: VSPAero Compute Geometry ====//
             analysis_name = "VSPAEROComputeGeometry"
    
             # Set defaults
             SetAnalysisInputDefaults( analysis_name )
    
    
         :param [in]: analysis Analysis name
        """
        return _vsp.SetAnalysisInputDefaults(analysis)
    
    @client_wrap
    def SetIntAnalysisInput(self, analysis, name, indata, index=0):
        r"""
        Set the value of a particular analysis input of integer type
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # Set to panel method
            thick_set = GetIntAnalysisInput( analysis_name, "GeomSet" )
            thin_set = GetIntAnalysisInput( analysis_name, "ThinGeomSet" )
    
            thick_set = [vsp.SET_NONE]
            thin_set = [vsp.SET_ALL]
    
            SetIntAnalysisInput( analysis_name, "GeomSet", thick_set )
            SetIntAnalysisInput( analysis_name, "ThinGeomSet", thin_set )
    
    
        See also: GetIntAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: indata vector<int> Array of integer values to set the input to
        :param [in]: index int Data index
        """
        return _vsp.SetIntAnalysisInput(analysis, name, indata, index)
    
    @client_wrap
    def SetDoubleAnalysisInput(self, analysis, name, indata, index=0):
        r"""
        Set the value of a particular analysis input of double type
    
    
        .. code-block:: python
    
            #==== Analysis: CpSlicer ====//
            analysis_name = "CpSlicer"
    
            # Setup cuts
            ycuts = []
            ycuts.append( 2.0 )
            ycuts.append( 4.5 )
            ycuts.append( 8.0 )
    
            SetDoubleAnalysisInput( analysis_name, "YSlicePosVec", ycuts, 0 )
    
    
        See also: GetDoubleAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: indata vector<double> Array of double values to set the input to
        :param [in]: index int Data index
        """
        return _vsp.SetDoubleAnalysisInput(analysis, name, indata, index)
    
    @client_wrap
    def SetStringAnalysisInput(self, analysis, name, indata, index=0):
        r"""
        Set the value of a particular analysis input of string type
    
    
        .. code-block:: python
    
            fileNameInput = GetStringAnalysisInput( "ParasiteDrag", "FileName" )
    
            fileNameInput = ["ParasiteDragExample"]
    
            SetStringAnalysisInput( "ParasiteDrag", "FileName", fileNameInput )
    
    
        See also: GetStringAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: indata vector<string> Array of string values to set the input to
        :param [in]: index int Data index
        """
        return _vsp.SetStringAnalysisInput(analysis, name, indata, index)
    
    @client_wrap
    def SetVec3dAnalysisInput(self, analysis, name, indata, index=0):
        r"""
        Set the value of a particular analysis input of vec3d type
    
    
        .. code-block:: python
    
            # PlanarSlice
            norm = GetVec3dAnalysisInput( "PlanarSlice", "Norm" )
    
            norm[0].set_xyz( 0.23, 0.6, 0.15 )
    
            SetVec3dAnalysisInput( "PlanarSlice", "Norm", norm )
    
    
        See also: GetVec3dAnalysisInput
        :param [in]: analysis string Analysis name
        :param [in]: name string Input name
        :param [in]: indata vector<vec3d> Array of vec3d values to set the input to
        :param [in]: index int Data index
        """
        return _vsp.SetVec3dAnalysisInput(analysis, name, indata, index)
    
    @client_wrap
    def PrintAnalysisInputs(self, analysis_name):
        r"""
        Print to stdout all current input values for a specific analysis
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # list inputs, type, and current values
            PrintAnalysisInputs( analysis_name )
    
    
        :param [in]: analysis_name string Name of analysis
        """
        return _vsp.PrintAnalysisInputs(analysis_name)
    
    @client_wrap
    def PrintAnalysisDocs(self, analysis_name):
        r"""
        Print to stdout all current input documentation for a specific analysis
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # list inputs, type, and documentation
            PrintAnalysisDocs( analysis_name )
    
    
        :param [in]: analysis_name string Name of analysis
        """
        return _vsp.PrintAnalysisDocs(analysis_name)
    
    @client_wrap
    def SummarizeAttributes(self, ):
        r"""
        Print a tab-delimited summary of all Attributes in the vehicle, denoting Name, Type, Data, Description, and path from Root of vehicle to Attribute
    
    
        .. code-block:: python
    
            ##==== Attributes: SummarizeAttributes ====##
            SummaryText = SummarizeAttributes()
            print( SummaryText )
    
    
        :rtype: string
        :return: Tab-delimited summary of all Attributes in vehicle
        """
        return _vsp.SummarizeAttributes()
    
    @client_wrap
    def SummarizeAttributesAsTree(self, ):
        r"""
        Print a plain-text tree summary of all Attribute in the vehicle, each branch node showing the name and ID of the VSP object in the path to the attribute
    
    
        .. code-block:: python
    
            ##==== Attributes: SummarizeAttributesAsTree ====##
            SummaryTextTree = SummarizeAttributesAsTree();
            print( SummaryTextTree )
    
    
        :rtype: string
        :return: Plain-text attribute tree of vehicle
        """
        return _vsp.SummarizeAttributesAsTree()
    
    @client_wrap
    def FindAllAttributes(self, ):
        r"""
        Returns a vector of string IDs for all Attributes in the vehicle
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAllAttributes ====##
            AttrIDs = FindAllAttributes()
            for AttrID in AttrIDs:
                print( AttrID )
    
    
        :rtype: vector< string >
        :return: Vector of All Attribute IDs
        """
        return _vsp.FindAllAttributes()
    
    @client_wrap
    def FindAttributesByName(self, search_str):
        r"""
        Returns all attributes that contain the string search_str within their name, case insensitive
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributesByName ====##
            AttrIDs = FindAttributesByName( "Watermark" )
            for AttrID in AttrIDs:
                print( AttrID )
    
    
        :rtype: vector< string >
        :return: Vector of string IDs of matching Attributes
        :param [in]: search_str string for filtering attributes in model
        """
        return _vsp.FindAttributesByName(search_str)
    
    @client_wrap
    def FindAttributeByName(self, search_str, index):
        r"""
        Searches all attributes that contain the search string, case insensitive, and returns the user-specified index
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributeByName ====##
            AttrID = FindAttributeByName( "Watermark", 0 )
            print( AttrID )
    
    
        :rtype: string
        :return: Returns a StringID of the attribute indexed/searched by user, if found
        :param [in]: search_str string for filtering attributes in model
        :param [in]: index int for indexing which of the vector of found attributes to select
        """
        return _vsp.FindAttributeByName(search_str, index)
    
    @client_wrap
    def FindAttributeInCollection(self, obj_id, search_str, index):
        r"""
        Searches all attributes in an OpenVSP object or AttributeCollection that contain the search string, case insensitive, and returns the user-specified index.
        Works either with the ID of an object that contains an attributeCollection or just the ID of an attributeCollection.
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributeInCollection ====##
            VehID = GetVehicleID()
            AttrID = FindAttributeInCollection( VehID, 'Watermark', 0 )
            print( AttrID )
    
    
        :rtype: string
        :return: Returns a StringID of the attribute indexed/searched by user, if found
        :param [in]: obj_id id of object to search within for attributes
        :param [in]: search_str string for filtering attributes in object
        :param [in]: index int for indexing which of the vector of found attributes to select
        """
        return _vsp.FindAttributeInCollection(obj_id, search_str, index)
    
    @client_wrap
    def FindAttributeNamesInCollection(self, collID):
        r"""
        Return a list of all attribute Names within an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributeNamesInCollection ====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrNames = FindAttributeNamesInCollection( CollID )
            for AttrName in AttrNames:
                print( AttrName )
    
    
        :rtype: vector< string >
        :return: Array of result names
        :param [in]: collID string ID of an attribute collection
        """
        return _vsp.FindAttributeNamesInCollection(collID)
    
    @client_wrap
    def FindAttributesInCollection(self, collID):
        r"""
        Get all attribute IDs within a single AttributeCollection, referenced by collID
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributesInCollection ====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrIDs = FindAttributesInCollection( CollID )
            for AttrID in AttrIDs:
                print( AttrID )
    
    
        :rtype: vector< string >
        :return: Vector of attribute IDs in an attribute collection.
        :param [in]: collID string ID of an attribute collection
        """
        return _vsp.FindAttributesInCollection(collID)
    
    @client_wrap
    def FindAttributedObjects(self, ):
        r"""
        Get array of IDs of all OpenVSP entities that have populated attributeCollections
        Includes attributeGroups
    
    
        .. code-block:: python
    
            ##==== Attributes: FindAttributedObjects ====##
            AttachIDs = FindAttributedObjects()
            for AttachID in AttachIDs:
                print( AttachID )
    
    
        :rtype: vector< string >
        :return: Array of IDs of entities in OpenVSP that contain populated attribute collections
        """
        return _vsp.FindAttributedObjects()
    
    @client_wrap
    def GetObjectType(self, attachID):
        r"""
        Get the type of an OpenVSP Entity by ID
    
    
        .. code-block:: python
    
            ##==== Attributes: GetObjectType ====##
            AttachIDs = FindAttributedObjects()
            for AttachID in AttachIDs:
                ObjType = GetObjectType( AttachID )
                print( ObjType )
    
    
        :rtype: int
        :return: return string of object name
        :param [in]: attachID string ID of an OpenVSP object
        """
        return _vsp.GetObjectType(attachID)
    
    @client_wrap
    def GetObjectTypeName(self, attachID):
        r"""
        Get the named type of an OpenVSP Entity by ID
    
    
        .. code-block:: python
    
            AttachIDs = FindAttributedObjects()
            for AttachID in AttachIDs:
                ObjTypeName = GetObjectTypeName( AttachID )
                print( ObjTypeName )
    
    
        :rtype: string
        :return: return string of object name
        :param [in]: attachID string ID of an OpenVSP object
        """
        return _vsp.GetObjectTypeName(attachID)
    
    @client_wrap
    def GetObjectName(self, attachID):
        r"""
        Get the name of an OpenVSP Entity by ID
    
    
        .. code-block:: python
    
            ##==== Attributes: GetObjectName ====##
            AttachIDs = FindAttributedObjects()
            for AttachID in AttachIDs:
                ObjName = GetObjectName( AttachID )
                print( ObjName )
    
    
        :rtype: string
        :return: return string of object name
        :param [in]: attachID string ID of an OpenVSP object
        """
        return _vsp.GetObjectName(attachID)
    
    @client_wrap
    def GetObjectParent(self, id):
        r"""
        Get the string ID of the entity's parent
        Attributes -> Attribute Collections
        Attribute Collections -> Objects that contain attribute Collections
        Geoms->Parent Geoms
        Parms->ParmContainers
        etc.
    
    
        .. code-block:: python
    
            ##==== Attributes: GetObjectParent ====##
    
            WingID = AddGeom( "WING" )
            PodID = AddGeom( "POD", WingID )
            ParentID = GetObjectParent( PodID )
    
            if ParentID == WingID:
                print( "Parent of Pod is Wing")
    
            #Get first attribute in vehicle as an example
            AttrID = FindAllAttributes()[0]
            CollID = GetObjectParent( AttrID )
            CollParentObjID = GetObjectParent( CollID )
            print( CollParentObjID )
    
    
        :rtype: string
        :return: string ID of object parent
        """
        return _vsp.GetObjectParent(id)
    
    @client_wrap
    def GetChildCollection(self, attachID):
        r"""
        Get collection ID from any OpenVSP object
        If ID is an attribute collection, return the same ID back
        If ID is an attribute group, return its nested collection
    
    
        .. code-block:: python
    
            ##==== Attributes: GetChildCollection =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            print( CollID )
    
    
    
        :rtype: string
        :return: String ID of attribute collection associated with the attachID
        :param [in]: attachID string ID of an OpenVSP object
        """
        return _vsp.GetChildCollection(attachID)
    
    @client_wrap
    def GetGeomSetCollection(self, index):
        r"""
        Get collection ID from a vehicle's GeomSet
    
    
        .. code-block:: python
    
            ##==== Attributes: GetGeomSetCollection =====##
            CollID = GetGeomSetCollection( 0 )
            print( CollID )
    
    
        :rtype: string
        :return: String ID of attribute collection associated with the geom set
        :param [in]: index int Geom set
        """
        return _vsp.GetGeomSetCollection(index)
    
    @client_wrap
    def GetAttributeName(self, attrID):
        r"""
        Return the name of an attribute by its ID
    
    
        .. code-block:: python
    
            ##==== Attributes: GetAttributeName =====##
    
            AttrIDs = FindAllAttributes()
    
            for AttrID in AttrIDs:
                AttrName = GetAttributeName( AttrID )
                print( AttrName )
    
    
        :param [in]: attrID string ID of an attribute
        :rtype: string
        :return: string name of attribute
        """
        return _vsp.GetAttributeName(attrID)
    
    @client_wrap
    def GetAttributeID(self, collID, attributeName, index):
        r"""
        Return the ID of an attribute by its name and collection ID
    
    
        .. code-block:: python
    
            ##==== Attributes: GetAttributeID =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrNames = FindAttributeNamesInCollection( CollID )
            for AttrName in AttrNames:
                AttrID = GetAttributeID( CollID, AttrName, 0 )
                print( AttrID )
    
    
    
        :rtype: string
        :return: String ID of attribute based on collectionID and name
        :param [in]: collID string ID of an attribute collection
        :param [in]: attributeName string name of an attribute in that collection
        :param [in]: index int index of attribute in collection
        """
        return _vsp.GetAttributeID(collID, attributeName, index)
    
    @client_wrap
    def GetAttributeDoc(self, attrID):
        r"""
        Return string doc of attribute by its ID
    
    
        .. code-block:: python
    
            ##==== Attributes: GetAttributeDoc =====##
            AttrID = FindAllAttributes()[0]
            AttrDoc = GetAttributeDoc(AttrID)
            print( AttrDoc )
    
    
        :rtype: string
        :return: Return string doc of attribute by its ID
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeDoc(attrID)
    
    @client_wrap
    def GetAttributeType(self, attrID):
        r"""
        Get int enum type of attribute by ID
        Use in conjunction with GetAttributeTypeName for getting strings or with the following enums
            BOOL_DATA
            INT_DATA
            DOUBLE_DATA
            STRING_DATA
            VEC3D_DATA
            INT_MATRIX_DATA
            DOUBLE_MATRIX_DATA
            NAMEVAL_COLLECTION_DATA
            ATTR_COLLECTION_DATA
    
    
        .. code-block:: python
    
            ##==== Attributes: GetAttributeType =====##
            AttrID = FindAllAttributes()[0]
            AttrType = GetAttributeType( AttrID )
            print( AttrType )
    
    
        :rtype: int
        :return: Int type of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeType(attrID)
    
    @client_wrap
    def GetAttributeTypeName(self, attrID):
        r"""
        Get the attribute's type as a string
    
    
        .. code-block:: python
    
            ##==== Attributes: GetAttributeTypeName =====##
            AttrID = FindAllAttributes()[0]
            AttributeTypeName = GetAttributeTypeName( AttrID )
            print( AttributeTypeName )
    
    
    
        :rtype: string
        :return: Type of attribute as string
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeTypeName(attrID)
    
    @client_wrap
    def GetAttributeBoolVal(self, attrID):
        r"""
        Get the boolean value of a bool-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeBoolVal  =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = True
            AttrID = AddAttributeBool( CollID, "TestBoolAttr", InitVal )
    
            GetVal = GetAttributeBoolVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Got matching Bool Value from Attribute" )
            else:
                print( "GetAttributeBoolVal error!" )
    
    
        :rtype: vector< int >
        :return: Bool value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeBoolVal(attrID)
    
    @client_wrap
    def GetAttributeIntVal(self, attrID):
        r"""
        Get the integer value of an int-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeIntVal  =====//
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = 55
            AttrID = AddAttributeInt( CollID, "TestIntAttr", InitVal )
    
            GetVal = GetAttributeIntVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Got matching Int Value from Attribute" )
            else:
                print( "GetAttributeIntVal error!" )
    
    
        :rtype: vector< int >
        :return: Int value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeIntVal(attrID)
    
    @client_wrap
    def GetAttributeDoubleVal(self, attrID):
        r"""
        Get the double value of a double-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeDoubleVal  =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = 3.14159
            AttrID = AddAttributeDouble( CollID, "TestDoubleAttr", InitVal )
    
            GetVal = GetAttributeDoubleVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Got matching Double Value from Attribute" )
            else:
                print( "GetAttributeDoubleVal error!" )
    
    
        :rtype: vector< double >
        :return: Double value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeDoubleVal(attrID)
    
    @client_wrap
    def GetAttributeStringVal(self, attrID):
        r"""
        Get the string value of a string-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeStringVal  =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = "Hello_World_of_Attributes"
            AttrID = AddAttributeString( CollID, "TestStringAttr", InitVal )
    
            GetVal = GetAttributeStringVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Got matching String Value from Attribute" )
            else:
                print( "GetAttributeStringVal error!" )
    
    
        :rtype: vector< string >
        :return: String value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeStringVal(attrID)
    
    @client_wrap
    def GetAttributeParmID(self, attrID):
        r"""
        Get the parm value of a parm-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeParmID  =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
    
            PodID = AddGeom( "POD", "" )
            print( "---> Test Get Parm Val" )
            ParmArray = GetGeomParmIDs( PodID )
    
            ParmID = ParmArray[0]
            AttrID = AddAttributeParm( CollID, "TestParmAttr", ParmID )
    
            GetID = GetAttributeParmID( AttrID )
    
            if GetID[0] == ParmID:
                print( "Got matching Parm ID from Attribute" )
            else:
                print( "GetAttributeParmID error!" )
    
    
        :rtype: vector< string >
        :return: Parm value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeParmID(attrID)
    
    @client_wrap
    def GetAttributeParmVal(self, attrID):
        r"""
        Get the parm value of a parm-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeParmVal  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
    
            PodID = AddGeom( "POD", "" )
            print( "---> Test Get Parm Val" )
            ParmArray = GetGeomParmIDs( PodID )
    
            ParmID = ParmArray[0]
            AttrID = AddAttributeParm( CollID, "TestParmAttr", ParmID )
    
            InitVal = GetParmVal( ParmID )
            GetVal = GetAttributeParmVal( AttrID )
    
            if GetVal[0] == InitVal:
                print( "Got matching Parm Value from Attribute" )
            else:
                print( "GetAttributeParmVal error!" )
    
    
    
        :rtype: vector< double >
        :return: Parm value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeParmVal(attrID)
    
    @client_wrap
    def GetAttributeParmName(self, attrID):
        r"""
        Get the name of the referenced parm of a parm-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeParmName  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            PodID = AddGeom( "POD", "" )
            print( "---> Test Get Parm Val" )
            ParmArray = GetGeomParmIDs( PodID )
            AttrName = 'Example_Parm_Attr'
            ParmID = ParmArray[0]
            AddAttributeParm( CollID, AttrName, ParmID )
            AttrID = GetAttributeID( CollID, AttrName, 0 )
            ParmName = GetAttributeParmName( AttrID )[0]
            if ParmName == GetParmName( ParmID ):
                print( "Got matching Parm Name from Attribute" )
            else:
                print( "GetAttributeParmName error!" )
    
    
    
        :rtype: vector< string >
        :return: Parm name of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeParmName(attrID)
    
    @client_wrap
    def GetAttributeVec3dVal(self, attrID):
        r"""
        Get the vec3d value of a string-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeVec3dVal  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = vec3d([1., 0.5, -4.])
            AttrID = AddAttributeVec3d( CollID, "TestVec3dAttr", [InitVal] )
    
            Vec3dVal = GetAttributeVec3dVal( AttrID )
            if ( Vec3dVal[0].x() == InitVal.x() ) and ( Vec3dVal[0].y() == InitVal.y() ) and ( Vec3dVal[0].z() == InitVal.z() ):
                print( "Got matching Vec3d Value from Attribute" )
            else:
                print( "GetAttributeVec3dVal error!" )
    
    
        :rtype: vector< vec3d >
        :return: Vec3d value of attribute
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeVec3dVal(attrID)
    
    @client_wrap
    def GetAttributeIntMatrixVal(self, attrID):
        r"""
        Get the Int Matrix of an Int-matrix-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeIntMatrixVal  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = [[0, 1,],[-4, -1000]]
            AttrID = AddAttributeIntMatrix( CollID, "TestIntMatrixAttr", InitVal )
    
            IntMatrixVal = GetAttributeIntMatrixVal( AttrID )
            IntMatrixVal = [list(row) for row in IntMatrixVal]
    
            if IntMatrixVal == InitVal:
                print( "Got matching IntMatrix Value from Attribute" )
            else:
                print( "GetAttributeIntMatrixVal error!" )
    
    
    
        :rtype: vector< vector< int > >
        :return: Int Matrix value of attribute as vector < vector < int > >
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeIntMatrixVal(attrID)
    
    @client_wrap
    def GetAttributeDoubleMatrixVal(self, attrID):
        r"""
        Get the Double Matrix of an Double-matrix-type attribute
    
    
        .. code-block:: python
    
            ##==== Attribute: GetAttributeDoubleMatrixVal  =====##
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = [[0., 1.,],[-4., -1000.]]
            AttrID = AddAttributeDoubleMatrix( CollID, "TestDoubleMatrixAttr", InitVal )
    
            DblMatrixVal = GetAttributeDoubleMatrixVal( AttrID )
            DblMatrixVal = [list(row) for row in DblMatrixVal]
    
            if DblMatrixVal == InitVal:
                print( "Got matching Double Matrix Value from Attribute" )
            else:
                print( "GetAttributeDoubleMatrixVal error!" )
    
    
        :rtype: vector< vector< double > >
        :return: Double Matrix value of attribute as vector < vector < Double > >
        :param [in]: attrID string ID of attribute
        """
        return _vsp.GetAttributeDoubleMatrixVal(attrID)
    
    @client_wrap
    def SetAttributeName(self, attrID, name):
        r"""
        Set the name of an Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeName  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = "Hello_World_of_Attributes"
            AttrID = AddAttributeString( CollID, "TestStringAttr", InitVal )
    
            NameString = 'NewName_Example'
            SetAttributeName( AttrID, NameString )
            AttrName = GetAttributeName( AttrID )
            if NameString == AttrName:
                print( "Got matching name from Attribute")
            else:
                print( "SetAttributeName error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: name string name for attribute
        """
        return _vsp.SetAttributeName(attrID, name)
    
    @client_wrap
    def SetAttributeDoc(self, attrID, doc):
        r"""
        Set the docstring of an Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeDoc  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = "Hello_World_of_Attributes"
            AttrID = AddAttributeString( CollID, "TestStringAttr", InitVal )
    
            DocString = 'New_docstring_for_attribute'
    
            SetAttributeDoc( AttrID, DocString )
            NewDocString = GetAttributeDoc( AttrID )
            if NewDocString == DocString:
                print( "Got matching DocString from Attribute")
            else:
                print( "SetAttributeDoc error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: doc string of documentation for attribute
        """
        return _vsp.SetAttributeDoc(attrID, doc)
    
    @client_wrap
    def SetAttributeBool(self, attrID, value):
        r"""
        Set the Bool value of a bool-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeBool  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = True
            AttrID = AddAttributeBool( CollID, "TestBoolAttr", InitVal )
    
            SetVal = False
            SetAttributeBool( AttrID, SetVal )
    
            GetVal = GetAttributeBoolVal( AttrID )
            if GetVal[0] == SetVal:
                print( "Set matching Bool Value from Attribute" )
            else:
                print( "SetAttributeBoolVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value boolean value for attribute
        """
        return _vsp.SetAttributeBool(attrID, value)
    
    @client_wrap
    def SetAttributeInt(self, attrID, value):
        r"""
        Set the Int value of an int-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeInt  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = 55
            AttrID = AddAttributeInt( CollID, "TestIntAttr", InitVal )
    
            NewIntVal = -55
    
            SetAttributeInt( AttrID, NewIntVal )
            GetVal = GetAttributeIntVal( AttrID )
            if GetVal[0] == NewIntVal:
                print( "Set matching Int Value from Attribute" )
            else:
                print( "SetAttributeIntVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value int value for attribute
        """
        return _vsp.SetAttributeInt(attrID, value)
    
    @client_wrap
    def SetAttributeDouble(self, attrID, value):
        r"""
        Set the Double value of a double-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeDouble  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = 3.14159
            AttrID = AddAttributeDouble( CollID, "TestDoubleAttr", InitVal )
    
            DoubleVal = 3.15
    
            SetAttributeDouble( AttrID, DoubleVal )
    
            GetVal = GetAttributeDoubleVal( AttrID )
            if GetVal[0] == DoubleVal:
                print( "Set matching Double Value from Attribute" )
            else:
                print( "SetAttributeDoubleVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value double value for attribute
        """
        return _vsp.SetAttributeDouble(attrID, value)
    
    @client_wrap
    def SetAttributeString(self, attrID, value):
        r"""
        Set the String value of a string-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeString  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = "Hello_World_of_Attributes"
            AttrID = AddAttributeString( CollID, "TestStringAttr", InitVal )
    
            StringVal = "Du bist supergeil!"
            SetAttributeString( AttrID, StringVal )
    
            GetVal = GetAttributeStringVal( AttrID )
            if GetVal[0] == StringVal:
                print( "Got matching String Value from Attribute" )
            else:
                print( "GetAttributeStringVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value string value for attribute
        """
        return _vsp.SetAttributeString(attrID, value)
    
    @client_wrap
    def SetAttributeParmID(self, attrID, value):
        r"""
        Set the ParmID value of a Parm-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeParmID  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
    
            PodID = AddGeom( "POD", "" )
            print( "---> Test Get Parm Val" )
            ParmArray = GetGeomParmIDs( PodID )
    
            ParmID = ParmArray[0]
            AttrID = AddAttributeParm( CollID, "TestParmAttr", ParmID )
    
            NewParmID = ParmArray[1]
            SetAttributeParmID( AttrID, NewParmID )
            GetID = GetAttributeParmID( AttrID )
    
            if GetID[0] == NewParmID:
                print( "Set matching Parm ID from Attribute" )
            else:
                print( "SetAttributeParmID error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value string value for attribute
        """
        return _vsp.SetAttributeParmID(attrID, value)
    
    @client_wrap
    def SetAttributeVec3d(self, attrID, value):
        r"""
        Set the Vec3d value of a Vec3d-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeVec3d  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = vec3d([1., 0.5, -4.])
            AttrID = AddAttributeVec3d( CollID, "TestVec3dAttr", [InitVal] )
    
            Vec3dVal = vec3d([0.5, 0.75, -0.4])
            SetAttributeVec3d( AttrID, [Vec3dVal] )
    
            GetVal = GetAttributeVec3dVal( AttrID )
            if ( GetVal[0].x() == Vec3dVal.x() ) and ( GetVal[0].y() == Vec3dVal.y() ) and ( GetVal[0].z() == Vec3dVal.z() ):
                print( "Set matching Vec3d Value from Attribute" )
            else:
                print( "SetAttributeVec3dVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value vec3d value for attribute
        """
        return _vsp.SetAttributeVec3d(attrID, value)
    
    @client_wrap
    def SetAttributeIntMatrix(self, attrID, value):
        r"""
            Set the int matrix of a int-matrix-type Attribute by ID
    
            .. code-block:: c++
    
            ==== Write Some Fake Test Results =====//
            not implemented
        ==== Attribute: SetAttributeIntMatrix  =====//
    
            string VehID = GetVehicleID();
            string CollID = GetChildCollection( VehID );
            array < array < int > > InitVal = {{0, 1},{-4, -1000}};
            string AttrID = AddAttributeIntMatrix( CollID, "TestIntMatrixAttr", InitVal );
    
            array < array < int > > NewImatVal = [[1,5],[-8,0]];
            SetAttributeIntMatrix( AttrID, NewImatVal );
    
            array < array < int > > IntMatrixVal = GetAttributeIntMatrixVal( AttrID );
    
            if ( IntMatrixVal == NewImatVal )
            {
                Print( "Set matching IntMatrix Value from Attribute" );
            }
            else
            {
                Print( "SetAttributeIntMatrixVal error!" );
                __failure++;
            }
    
            .. code-block:: python
    
                ##==== Attribute: SetAttributeIntMatrix  =====##
    
                VehID = GetVehicleID()
                CollID = GetChildCollection( VehID )
                InitVal = [[0, 1,],[-4, -1000]]
                AttrID = AddAttributeIntMatrix( CollID, "TestIntMatrixAttr", InitVal )
    
                ImatVal = [[1,5],[-8,0]]
                SetAttributeIntMatrix( AttrID, ImatVal )
    
                IntMatrixVal = GetAttributeIntMatrixVal( AttrID )
                IntMatrixVal = [list(row) for row in IntMatrixVal]
    
                if IntMatrixVal == ImatVal:
                    print( "Set matching IntMatrix Value from Attribute" )
                else:
                    print( "SetAttributeIntMatrixVal error!" )
    
    
            :param [in]: attrID string of attribute ID
            :param [in]: value int matrix value for attribute
        """
        return _vsp.SetAttributeIntMatrix(attrID, value)
    
    @client_wrap
    def SetAttributeDoubleMatrix(self, attrID, value):
        r"""
        Set the double matrix of a double-matrix-type Attribute by ID
    
    
        .. code-block:: python
    
            ##==== Attribute: SetAttributeDoubleMatrix  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = [[0., 1.,],[-4., -1000.]]
            AttrID = AddAttributeDoubleMatrix( CollID, "TestDoubleMatrixAttr", InitVal )
    
            NewDmatVal = [[0.,1.5],[8.4,1.1566]]
            SetAttributeDoubleMatrix( AttrID, NewDmatVal )
    
            DblMatrixVal = GetAttributeDoubleMatrixVal( AttrID )
            DblMatrixVal = [list(row) for row in DblMatrixVal]
    
            if DblMatrixVal == NewDmatVal:
                print( "Got matching Double Matrix Value from Attribute" )
            else:
                print( "GetAttributeDoubleMatrixVal error!" )
    
    
        :param [in]: attrID string of attribute ID
        :param [in]: value double matrix value for attribute
        """
        return _vsp.SetAttributeDoubleMatrix(attrID, value)
    
    @client_wrap
    def DeleteAttribute(self, attrID):
        r"""
        Delete attribute by attribute ID
    
    
        .. code-block:: python
    
            ##==== Attribute: DeleteAttribute  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = "This_Attribute_Will_Be_Deleted"
            AttrID = AddAttributeString( CollID, "TestStringAttr", InitVal )
    
    
            AttrIDs = FindAllAttributes()
            AttrAdded = AttrID in AttrIDs
    
            DeleteAttribute( AttrID )
            NewAttrIDs = FindAllAttributes()
            AttrDeleted = AttrID not in NewAttrIDs
    
            if AttrAdded and AttrDeleted:
                print( "Attribute successfully deleted" )
            else:
                print( "DeleteAttribute error!" )
    
    
        :param [in]: attrID string of attribute ID
        """
        return _vsp.DeleteAttribute(attrID)
    
    @client_wrap
    def AddAttributeBool(self, collID, attributeName, value):
        r"""
        Add a boolean attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeBool  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = True
            AttrID = AddAttributeBool( CollID, "TestBoolAttr", InitVal )
    
            GetVal = GetAttributeBoolVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Added Bool Attribute" )
            else:
                print( "AddAttributeBool error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value boolean value of new attribute
        """
        return _vsp.AddAttributeBool(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeInt(self, collID, attributeName, value):
        r"""
        Add a integer attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeInt  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            InitVal = 55
            AttrID = AddAttributeInt( CollID, "TestIntAttr", InitVal )
    
            GetVal = GetAttributeIntVal( AttrID )
            if GetVal[0] == InitVal:
                print( "Added Int Attribute" )
            else:
                print( "AddAttributeInt error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value integer value of new attribute
        """
        return _vsp.AddAttributeInt(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeDouble(self, collID, attributeName, value):
        r"""
        Add a double attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeDouble  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_Double_Attr'
            DoubleValue = 3.14159
            AttrID = AddAttributeDouble( CollID, AttrName, DoubleValue )
    
            GetVal = GetAttributeDoubleVal( AttrID )
            if GetVal[0] == DoubleValue:
                print( "Added Double Attribute" )
            else:
                print( "AddAttributeDouble error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value double value of new attribute
        """
        return _vsp.AddAttributeDouble(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeString(self, collID, attributeName, value):
        r"""
        Add a string attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeString  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_String_Attr'
            StringValue = 'Example_String_Attr_DataVal'
            AttrID = AddAttributeString( CollID, AttrName, StringValue )
    
            GetVal = GetAttributeStringVal( AttrID )
            if GetVal[0] == StringValue:
                print( "Added String Attribute" )
            else:
                print( "AddAttributeString error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value string value of new attribute
        """
        return _vsp.AddAttributeString(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeParm(self, collID, attributeName, parmID):
        r"""
        Add a parm attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeParm  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            pid = AddGeom( "POD", "" )
            print( "---> Test Add Parm Attr" )
            parm_array = GetGeomParmIDs( pid )
            AttrName = 'Example_Parm_Attr'
            ParmID = parm_array[0]
            AttrID = AddAttributeParm( CollID, AttrName, ParmID )
    
            GetVal = GetAttributeParmID( AttrID )
            if GetVal[0] == ParmID:
                print( "Added Parm Attribute" )
            else:
                print( "AddAttributeParm error!" )
    
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: parmID string Parm ID to add to attribute
        """
        return _vsp.AddAttributeParm(collID, attributeName, parmID)
    
    @client_wrap
    def AddAttributeVec3d(self, collID, attributeName, value):
        r"""
        Add a Vec3d attribute by name to an attribute collection
        use vec3d() to create a vec3d object to pass into the args!
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeVec3d  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_Vec3D_Attr'
            Vec3dVal = vec3d( 0.5, 0.75, -0.4 )
            AttrID = AddAttributeVec3d( CollID, AttrName, [Vec3dVal] )
    
            GetVal = GetAttributeVec3dVal( AttrID )
            if ( GetVal[0].x() == Vec3dVal.x() ) and ( GetVal[0].y() == Vec3dVal.y() ) and ( GetVal[0].z() == Vec3dVal.z() ):
                print( "Added Vec3d Attribute" )
            else:
                print( "AddAttributeVec3d error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value Vec3d value of new attribute
        """
        return _vsp.AddAttributeVec3d(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeIntMatrix(self, collID, attributeName, value):
        r"""
        Add an Int Matrix attribute by name to an attribute collection
        use nested vectors/arrays of ints for matrix argument
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeIntMatrix  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_IntMatrix_Attr'
            IntMatrix = [[1,5],[-8,0]]
            AttrID = AddAttributeIntMatrix( CollID, AttrName, IntMatrix )
    
            IntMatrixVal = GetAttributeIntMatrixVal( AttrID )
            IntMatrixVal = [list(row) for row in IntMatrixVal]
    
            if IntMatrixVal == IntMatrix:
                print( "Added IntMatrix Attribute" )
            else:
                print( "AddAttributeIntMatrix error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value int matrix value of new attribute
        """
        return _vsp.AddAttributeIntMatrix(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeDoubleMatrix(self, collID, attributeName, value):
        r"""
        Add an Double Matrix attribute by name to an attribute collection
        use nested vectors/arrays of ints for matrix argument
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeDoubleMatrix  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_DoubleMat_Attr'
            DoubleMatrix = [[0.,1.5],[8.4,1.1566]]
            AttrID = AddAttributeDoubleMatrix( CollID, AttrName, DoubleMatrix )
    
            DoubleMatrixVal = GetAttributeDoubleMatrixVal( AttrID )
            DoubleMatrixVal = [list(row) for row in DoubleMatrixVal]
    
            if DoubleMatrixVal == DoubleMatrix:
                print( "Added DoubleMatrix Attribute" )
            else:
                print( "AddAttributeDoubleMatrix error!" )
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute
        :param [in]: value Double matrix value of new attribute
        """
        return _vsp.AddAttributeDoubleMatrix(collID, attributeName, value)
    
    @client_wrap
    def AddAttributeGroup(self, collID, attributeName):
        r"""
        Add an empty Attribute Group-type attribute by name to an attribute collection
    
    
        .. code-block:: python
    
            ##==== Attribute: AddAttributeGroup  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_Attr_Group'
            AttrID = AddAttributeGroup( CollID, AttrName )
            if GetAttributeType( AttrID ) == ATTR_COLLECTION_DATA:
                print( "Added Attribute Group" )
            else:
                print( "AddAttributeGroup error!" )
    
    
    
        :param [in]: collID string ID of attribute collection
        :param [in]: attributeName string name of new attribute group
        """
        return _vsp.AddAttributeGroup(collID, attributeName)
    
    @client_wrap
    def CopyAttribute(self, attrID):
        r"""
        Copy an attribute to the clipboard by attributeID
    
    
        .. code-block:: python
    
            ##==== Attribute: CopyAttribute  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_String_Attr'
            StringValue = 'Example_String_Attr_DataVal'
            AttrID = AddAttributeString( CollID, AttrName, StringValue )
            CopyError = CopyAttribute( AttrID )
            if not CopyError:
                print("Successfully copied Attribute")
            else:
                print("CopyAttribute Error!")
    
        :param [in]: attrID string ID of attribute to be copied
        """
        return _vsp.CopyAttribute(attrID)
    
    @client_wrap
    def CutAttribute(self, attrID):
        r"""
        Cut an attribute from its collection to the clipboard by attributeID
    
    
        .. code-block:: python
    
            ##==== Attribute: CopyAttribute  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_String_Attr'
            StringValue = 'Example_String_Attr_DataVal'
            AttrID = AddAttributeString( CollID, AttrName, StringValue )
            CutAttribute( AttrID )
    
            NewCollID = GetChildCollection( "_AttrWMGroup" )
            NewAttrIDs = PasteAttribute( NewCollID )
    
            MatchIDs = NewAttrIDs[0] == AttrID
            Attr_Cut_Check = AttrID not in FindAttributesInCollection( CollID )
            if MatchIDs and Attr_Cut_Check:
                print("Successfully cut Attribute")
            else:
                print("CutAttribute Error!")
    
    
        :param [in]: attrID string ID of attribute to be copied
        """
        return _vsp.CutAttribute(attrID)
    
    @client_wrap
    def PasteAttribute(self, coll_id):
        r"""
        Paste the attribute clipboard to the specified objectID
        ObjectID can be any OpenVSP entity that contains a AttributeCollection or simply the attributeCollectionID
        Returns a vector of pasted attributes IDs, if any
    
    
        .. code-block:: python
    
            ##==== Attribute: PasteAttribute  =====##
    
            VehID = GetVehicleID()
            CollID = GetChildCollection( VehID )
            AttrName = 'Example_String_Attr'
            StringValue = 'Example_String_Attr_DataVal'
            AttrID = AddAttributeString( CollID, AttrName, StringValue )
            CutAttribute( AttrID )
    
            NewCollID = GetChildCollection( "_AttrWMGroup" )
            NewAttrIDs = PasteAttribute( NewCollID )
    
            MatchIDs = NewAttrIDs[0] == AttrID
            Attr_Cut_Check = AttrID not in FindAttributesInCollection( CollID )
            Attr_Paste_Check = AttrID in FindAttributesInCollection( NewCollID )
            if MatchIDs and Attr_Cut_Check and Attr_Paste_Check:
                print("Successfully pasted Attribute")
            else:
                print("PasteAttribute Error!")
    
    
        :param [in]: coll_id string ID of destination for pasting attribute into
        """
        return _vsp.PasteAttribute(coll_id)
    
    @client_wrap
    def GetAllResultsNames(self, ):
        r"""
        Get the name of all results in the Results Manager
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            results_array = GetAllResultsNames()
    
            for i in range(int( len(results_array) )):
    
                resid = FindLatestResultsID( results_array[i] )
                PrintResults( resid )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of result names
        """
        return _vsp.GetAllResultsNames()
    
    @client_wrap
    def GetAllDataNames(self, results_id):
        r"""
        Get all data names for a particular result
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            data_names = GetAllDataNames( res_id )
    
            if  len(data_names) != 5 : print( "---> Error: API GetAllDataNames" )
    
    
        :param [in]: results_id Result ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of result names
        """
        return _vsp.GetAllDataNames(results_id)
    
    @client_wrap
    def GetNumResults(self, name):
        r"""
        Get the number of results for a particular result name
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            if ( GetNumResults( "Test_Results" ) != 2 ): print( "---> Error: API GetNumResults" )
    
    
        :param [in]: name Input name
        :rtype: int
        :return: Number of results
        """
        return _vsp.GetNumResults(name)
    
    @client_wrap
    def GetResultsName(self, results_id):
        r"""
        Get the name of a result given its ID
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # Set defaults
            SetAnalysisInputDefaults( analysis_name )
    
            res_id = ( ExecAnalysis( analysis_name ) )
    
            print( "Results Name: ", False )
    
            print( GetResultsName( res_id ) )
    
    
        :param [in]: results_id Result ID
        :rtype: string
        :return: Result name
        """
        return _vsp.GetResultsName(results_id)
    
    @client_wrap
    def GetResultsSetDoc(self, results_id):
        r"""
        Get the documentation string for a result given its ID
    
    
        .. code-block:: python
    
            #==== Analysis: VSPAero Compute Geometry ====//
            analysis_name = "VSPAEROComputeGeometry"
    
            # Set defaults
            SetAnalysisInputDefaults( analysis_name )
    
            res_id = ( ExecAnalysis( analysis_name ) )
    
            print( "Results doc: ", False )
    
            print( GetResultsSetDoc( res_id ) )
    
    
        :param [in]: results_id Result ID
        :rtype: string
        :return: Result documentation string
        """
        return _vsp.GetResultsSetDoc(results_id)
    
    @client_wrap
    def GetResultsEntryDoc(self, results_id, data_name):
        r"""GetResultsEntryDoc(std::string const & results_id, std::string const & data_name) -> std::string"""
        return _vsp.GetResultsEntryDoc(results_id, data_name)
    
    @client_wrap
    def FindResultsID(self, name, index=0):
        r"""
        Find a results ID given its name and index
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            if  len(res_id) == 0 : print( "---> Error: API FindResultsID" )
    
    
        :param [in]: name Result name
        :param [in]: index Result index
        :rtype: string
        :return: Result ID
        """
        return _vsp.FindResultsID(name, index)
    
    @client_wrap
    def FindLatestResultsID(self, name):
        r"""
        Find the latest results ID for particular result name
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            results_array = GetAllResultsNames()
    
            for i in range(int( len(results_array) )):
    
                resid = FindLatestResultsID( results_array[i] )
                PrintResults( resid )
    
    
        :param [in]: name Result name
        :rtype: string
        :return: Result ID
        """
        return _vsp.FindLatestResultsID(name)
    
    @client_wrap
    def GetNumData(self, results_id, data_name):
        r"""
        Get the number of data values for a given result ID and data name
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            if ( GetNumData( res_id, "Test_Int" ) != 2 ): print( "---> Error: API GetNumData " )
    
            int_arr = GetIntResults( res_id, "Test_Int", 0 )
    
            if  int_arr[0] != 1 : print( "---> Error: API GetIntResults" )
    
            int_arr = GetIntResults( res_id, "Test_Int", 1 )
    
            if  int_arr[0] != 2 : print( "---> Error: API GetIntResults" )
    
    
        :param [in]: results_id Result ID
        :param [in]: data_name Data name
        :rtype: int
        :return: Number of data values
        """
        return _vsp.GetNumData(results_id, data_name)
    
    @client_wrap
    def GetResultsType(self, results_id, data_name):
        r"""
        Get the data type for a given result ID and data name
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            res_array = GetAllDataNames( res_id )
    
            for j in range(int( len(res_array) )):
    
                typ = GetResultsType( res_id, res_array[j] )
    
    
        See also: RES_DATA_TYPE
        :param [in]: results_id Result ID
        :param [in]: data_name Data name
        :rtype: int
        :return: Data type enum (i.e. DOUBLE_DATA)
        """
        return _vsp.GetResultsType(results_id, data_name)
    
    @client_wrap
    def GetIntResults(self, id, name, index=0):
        r"""
        Get all integer values for a particular result, name, and index
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            if ( GetNumData( res_id, "Test_Int" ) != 2 ): print( "---> Error: API GetNumData " )
    
            int_arr = GetIntResults( res_id, "Test_Int", 0 )
    
            if  int_arr[0] != 1 : print( "---> Error: API GetIntResults" )
    
            int_arr = GetIntResults( res_id, "Test_Int", 1 )
    
            if  int_arr[0] != 2 : print( "---> Error: API GetIntResults" )
    
    
        :param [in]: id Result ID
        :param [in]: name Data name
        :param [in]: index Data index
        :rtype: std::vector< int,std::allocator< int > >
        :return: Array of data values
        """
        return _vsp.GetIntResults(id, name, index)
    
    @client_wrap
    def GetDoubleResults(self, id, name, index=0):
        r"""
        Get all double values for a particular result, name, and index
    
    
        .. code-block:: python
    
            #==== Add Pod Geom ====//
            pid = AddGeom( "POD", "" )
    
            #==== Run CompGeom And View Results ====//
            mesh_id = ComputeCompGeom( SET_ALL, False, 0 )                      # Half Mesh false and no file export
    
            comp_res_id = FindLatestResultsID( "Comp_Geom" )                    # Find Results ID
    
            double_arr = GetDoubleResults( comp_res_id, "Wet_Area" )    # Extract Results
    
    
        :param [in]: id Result ID
        :param [in]: name Data name
        :param [in]: index Data index
        :rtype: std::vector< double,std::allocator< double > >
        :return: Array of data values
        """
        return _vsp.GetDoubleResults(id, name, index)
    
    @client_wrap
    def GetDoubleMatResults(self, id, name, index=0):
        r"""
        Get all matrix (vector<vector<double>>) values for a particular result, name, and index
        :param [in]: id Result ID
        :param [in]: name Data name
        :param [in]: index Data index
        :rtype: std::vector< std::vector< double,std::allocator< double > >,std::allocator< std::vector< double,std::allocator< double > > > >
        :return: 2D array of data values
        """
        return _vsp.GetDoubleMatResults(id, name, index)
    
    @client_wrap
    def GetStringResults(self, id, name, index=0):
        r"""
        Get all string values for a particular result, name, and index
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            res_id = FindResultsID( "Test_Results" )
    
            str_arr = GetStringResults( res_id, "Test_String" )
    
            if ( str_arr[0] != "This Is A Test" ): print( "---> Error: API GetStringResults" )
    
    
        :param [in]: id Result ID
        :param [in]: name Data name
        :param [in]: index Data index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of data values
        """
        return _vsp.GetStringResults(id, name, index)
    
    @client_wrap
    def GetVec3dResults(self, id, name, index=0):
        r"""
        Get all vec3d values for a particular result, name, and index
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
    
            tol = 0.00001
    
            WriteTestResults()
    
            res_id = FindLatestResultsID( "Test_Results" )
    
            vec3d_vec = GetVec3dResults( res_id, "Test_Vec3d" )
    
            print( "X: ", False )
            print( vec3d_vec[0].x(), False )
    
            print( "\tY: ", False )
            print( vec3d_vec[0].y(), False )
    
            print( "\tZ: ", False )
            print( vec3d_vec[0].z() )
    
    
        :param [in]: id Result ID
        :param [in]: name Data name
        :param [in]: index Data index
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of data values
        """
        return _vsp.GetVec3dResults(id, name, index)
    
    @client_wrap
    def CreateGeomResults(self, geom_id, name):
        r"""
        Create a new result for a Geom
    
    
        .. code-block:: python
    
            #==== Test Comp Geom ====//
            gid1 = AddGeom( "POD", "" )
    
            mesh_id = ComputeCompGeom( 0, False, 0 )
    
            #==== Test Comp Geom Mesh Results ====//
            mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )
    
            int_arr = GetIntResults( mesh_geom_res_id, "Num_Tris" )
    
            if  int_arr[0] < 4 : print( "---> Error: API CreateGeomResults" )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: name Result name
        :rtype: string
        :return: Result ID
        """
        return _vsp.CreateGeomResults(geom_id, name)
    
    @client_wrap
    def DeleteAllResults(self, ):
        r"""
        Delete all results
    
    
        .. code-block:: python
    
            #==== Test Comp Geom ====//
            gid1 = AddGeom( "POD", "" )
    
            mesh_id = ComputeCompGeom( 0, False, 0 )
    
            #==== Test Comp Geom Mesh Results ====//
            mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )
    
            DeleteAllResults()
    
            if ( GetNumResults( "Comp_Mesh" ) != 0 ): print( "---> Error: API DeleteAllResults" )
    
    
        """
        return _vsp.DeleteAllResults()
    
    @client_wrap
    def DeleteResult(self, id):
        r"""
        Delete a particular result
    
    
        .. code-block:: python
    
            #==== Test Comp Geom ====//
            gid1 = AddGeom( "POD", "" )
    
            mesh_id = ComputeCompGeom( 0, False, 0 )
    
            #==== Test Comp Geom Mesh Results ====//
            mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )
    
            DeleteResult( mesh_geom_res_id )
    
            if ( GetNumResults( "Comp_Mesh" ) != 0 ): print( "---> Error: API DeleteResult" )
    
    
        :param [in]: id Result ID
        """
        return _vsp.DeleteResult(id)
    
    @client_wrap
    def WriteResultsCSVFile(self, id, file_name):
        r"""
        Export a result to CSV
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pid = AddGeom( "POD" )
    
            analysis_name = "VSPAEROComputeGeometry"
    
            rid = ExecAnalysis( analysis_name )
    
            WriteResultsCSVFile( rid, "CompGeomRes.csv" )
    
    
        :param [in]: id Rsult ID
        :param [in]: file_name CSV output file name
        """
        return _vsp.WriteResultsCSVFile(id, file_name)
    
    @client_wrap
    def PrintResults(self, results_id):
        r"""
        Print a result's name value pairs to stdout
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pid = AddGeom( "POD" )
    
            analysis_name = "VSPAEROComputeGeometry"
    
            rid = ExecAnalysis( analysis_name )
    
            # Get & Display Results
            PrintResults( rid )
    
    
        :param [in]: results_id string Result ID
        """
        return _vsp.PrintResults(results_id)
    
    @client_wrap
    def PrintResultsDocs(self, results_id):
        r"""
        Print a result's names and documentation to stdout
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pid = AddGeom( "POD" )
    
            analysis_name = "VSPAEROComputeGeometry"
    
            rid = ExecAnalysis( analysis_name )
    
            # Get & Display Results Docs
            PrintResultsDocs( rid )
    
    
        :param [in]: results_id string Result ID
        """
        return _vsp.PrintResultsDocs(results_id)
    
    @client_wrap
    def WriteTestResults(self, ):
        r"""
        Generate some example results for testing.
    
    
        .. code-block:: python
    
            #==== Write Some Fake Test Results =====//
            WriteTestResults()
    
            results_array = GetAllResultsNames()
    
            for i in range( len( results_array ) ):
                resid = FindLatestResultsID( results_array[i] )
                PrintResults( resid )
    
    
        """
        return _vsp.WriteTestResults()
    
    @client_wrap
    def InitGUI(self, ):
        r"""
        Low level routine that should be called to set up GUI before running StartGUI()
    
    
        .. code-block:: python
    
    
            InitGUI()
    
    
        """
        return _vsp.InitGUI()
    
    @client_wrap
    def StartGUI(self, ):
        r"""
        Launch the interactive OpenVSP GUI.  In a multi-threaded environment, this must be called from the main thread only.
        This starts the GUI event loop.  It will also show the main screen and screens displayed when StopGUI() was
        previously called.
    
    
        .. code-block:: python
    
    
            StartGUI()
    
    
        """
        return _vsp.StartGUI()
    
    @client_wrap
    def EnableStopGUIMenuItem(self, ):
        r"""
        Enable Stop GUI Menu Item from the OpenVSP GUI.
    
        Typically used for the blocking-mode OpenVSP GUI from the API.
    
        This will add a "Stop GUI" option to the file pulldown menu and will also cause the exit button on the
        window frame to have the same effect.  When selected, these options will stop the OpenVSP GUI event loop,
        returning control to the API program.  OpenVSP will not terminate, the model will remain in memory and will
        be responsive to subsequent API calls.
    
    
    
        .. code-block:: python
    
    
            EnableStopGUIMenuItem()
            StartGUI()
    
    
    
        See also: DisableStopGUIMenuItem
        """
        return _vsp.EnableStopGUIMenuItem()
    
    @client_wrap
    def DisableStopGUIMenuItem(self, ):
        r"""
        Disable Stop GUI Menu Item from the OpenVSP GUI.
    
        This reverses the operation of EnableStopGUIMenuItem.
    
    
    
        .. code-block:: python
    
    
            EnableStopGUIMenuItem()
            DisableStopGUIMenuItem()
            StartGUI()
    
    
    
        See also: EnableStopGUIMenuItem
        """
        return _vsp.DisableStopGUIMenuItem()
    
    @client_wrap
    def StopGUI(self, ):
        r"""
        Stop OpenVSP GUI event loop and hide screens.  Keep OpenVSP running and in memory.
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            StopGUI()
    
            StartGUI()
    
    
    
        See also: StartGUI
        """
        return _vsp.StopGUI()
    
    @client_wrap
    def PopupMsg(self, msg):
        r"""
        Cause OpenVSP to display a popup message.
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            PopupMsg( "This is a popup message." )
    
    
    
        :param [in]: msg string Message to display.
        """
        return _vsp.PopupMsg(msg)
    
    @client_wrap
    def UpdateGUI(self, ):
        r"""
        Tell OpenVSP that the GUI needs to be updated.
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            pod_id = AddGeom( "POD" )
    
            length = FindParm( pod_id, "Length", "Design" )
    
            SetParmVal( length, 13.0 )
    
            UpdateGUI()
    
    
    
        See also: StartGUI
        """
        return _vsp.UpdateGUI()
    
    @client_wrap
    def IsGUIBuild(self, ):
        r"""
        Test if the current OpenVSP build includes graphics capabilities.
    
    
        .. code-block:: python
    
    
            if ( IsGUIBuild() ):
                print( "OpenVSP build is graphics capable." )
            else:
                print( "OpenVSP build is not graphics capable." )
    
    
    
        :rtype: boolean
        :return: bool True if the current OpenVSP build includes graphics capabilities.  False otherwise.
        """
        return _vsp.IsGUIBuild()
    
    @client_wrap
    def Lock(self, ):
        r"""
        Obtain the lock on the OpenVSP GUI event loop.  This will prevent the interactive GUI from
        updating or accepting user input until the lock is released -- thereby allowing longer-time
        commands including analyses to execute without the chance of the OpenVSP state changing during
        execution.
    
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            pod_id = AddGeom( "POD" )
    
            Lock()
            rid = ExecAnalysis( "CompGeom" )
    
            mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )
    
            DeleteGeomVec( mesh_id_vec )
            Unlock()
    
    
    
        See also: Unlock
        """
        return _vsp.Lock()
    
    @client_wrap
    def Unlock(self, ):
        r"""
        Release the lock on the OpenVSP GUI event loop.
    
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            pod_id = AddGeom( "POD" )
    
            Lock()
            rid = ExecAnalysis( "CompGeom" )
    
            mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )
    
            DeleteGeomVec( mesh_id_vec )
            Unlock()
    
    
    
        See also: Lock
        """
        return _vsp.Unlock()
    
    @client_wrap
    def IsEventLoopRunning(self, ):
        r"""
        Test if the OpenVSP GUI event loop is running.
    
    
    
        .. code-block:: python
    
    
            StartGUI()
    
            if ( IsEventLoopRunning() ):
                print( "Event loop is running." )
    
    
        :rtype: boolean
        :return: bool True if the OpenVSP GUI event loop is running.  False otherwise.
        """
        return _vsp.IsEventLoopRunning()
    
    @client_wrap
    def ScreenGrab(self, fname, w, h, transparentBG, autocrop=False):
        r"""
        Capture the specified screen and save to file. Note, VSP_USE_FLTK must be defined
    
    
        .. code-block:: python
    
            screenw = 2000                                             # Set screenshot width and height
            screenh = 2000
    
            fname = "test_screen_grab.png"
    
            ScreenGrab( fname, screenw, screenh, True, True )                # Take PNG screenshot
    
    
        :param [in]: fname string Output file name
        :param [in]: w int Width of screen grab
        :param [in]: h int Height of screen grab
        :param [in]: transparentBG bool Transparent background flag
        :param [in]: autocrop bool Automatically crop transparent background flag
        """
        return _vsp.ScreenGrab(fname, w, h, transparentBG, autocrop)
    
    @client_wrap
    def SetViewAxis(self, vaxis):
        r"""
        Toggle viewing the axis
    
    
        .. code-block:: python
    
            SetViewAxis( False )                                           # Turn off axis marker in corner of viewscreen
    
    
        :param [in]: vaxis True to show the axis, false to hide the axis
        """
        return _vsp.SetViewAxis(vaxis)
    
    @client_wrap
    def SetShowBorders(self, brdr):
        r"""
        Toggle viewing the border frame
    
    
        .. code-block:: python
    
            SetShowBorders( False )                                        # Turn off red/black border on active window
    
    
        :param [in]: brdr True to show the border frame, false to hide the border frame
        """
        return _vsp.SetShowBorders(brdr)
    
    @client_wrap
    def SetGeomDrawType(self, geom_id, type):
        r"""
        Set the draw type of the specified geometry
    
    
        .. code-block:: python
    
            pid = AddGeom( "POD", "" )                             # Add Pod for testing
    
            SetGeomDrawType( pid, GEOM_DRAW_SHADE )                       # Make pod appear as shaded
    
    
        See also: DRAW_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: type Draw type enum (i.e. GEOM_DRAW_SHADE)
        """
        return _vsp.SetGeomDrawType(geom_id, type)
    
    @client_wrap
    def SetGeomWireColor(self, geom_id, r, g, b):
        r"""
        Set the wireframe color of the specified geometry
    
    
        .. code-block:: python
    
            pid = AddGeom( "POD", "" )
    
            SetGeomWireColor( pid, 0, 0, 255 )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: r int Red component of color [0, 255]
        :param [in]: g int Green component of color [0, 255]
        :param [in]: b int Blue component of color [0, 255]
        """
        return _vsp.SetGeomWireColor(geom_id, r, g, b)
    
    @client_wrap
    def SetGeomDisplayType(self, geom_id, type):
        r"""
        Set the display type of the specified geometry
    
    
        .. code-block:: python
    
            pid = AddGeom( "POD" )                             # Add Pod for testing
    
            SetGeomDisplayType( pid, DISPLAY_DEGEN_PLATE )                       # Make pod appear as Bezier plate (Degen Geom)
    
    
        See also: DISPLAY_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: type Display type enum (i.e. DISPLAY_BEZIER)
        """
        return _vsp.SetGeomDisplayType(geom_id, type)
    
    @client_wrap
    def SetGeomMaterialName(self, geom_id, name):
        r"""
        Set the visualization material the specified geometry
    
    
        .. code-block:: python
    
            pid = AddGeom( "POD" )
    
            SetGeomMaterialName( pid, "Ruby" )
    
        :param [in]: geom_id string Geom ID
        :param [in]: name string Material name
        """
        return _vsp.SetGeomMaterialName(geom_id, name)
    
    @client_wrap
    def AddMaterial(self, name, ambient, diffuse, specular, emissive, alpha, shininess):
        r"""
        Set the visualization material the specified geometry
    
    
        .. code-block:: python
    
            pid = AddGeom( "POD" )
    
            AddMaterial( "RedGlass", vec3d( 44, 2, 2 ), vec3d( 156, 10, 10 ), vec3d( 185, 159, 159 ), vec3d( 44, 2, 2 ), 30, 0.4 )
    
            SetGeomMaterialName( pid, "RedGlass" )
    
        :param [in]: name string Material name
        :param [in]: ambient vec3d Ambient color RGB triple on scale [0, 255]
        :param [in]: diffuse vec3d Diffuse color RGB triple on scale [0, 255]
        :param [in]: specular vec3d Specular color RGB triple on scale [0, 255]
        :param [in]: emissive vec3d Emissive color RGB triple on scale [0, 255]
        :param [in]: shininess double Shininess exponent on scale [0, 127]
        :param [in]: alpha double Transparency factor on scale [0, 1]
        """
        return _vsp.AddMaterial(name, ambient, diffuse, specular, emissive, alpha, shininess)
    
    @client_wrap
    def GetMaterialNames(self, ):
        r"""
        Get the names of all visualization materials
    
    
        .. code-block:: python
    
            mat_array = GetMaterialNames()
    
            for i in range(int( len(mat_array) )):
                print( mat_array[i] )
    
    
        :rtype: vector< string >
        :return: vector<string> Array of material names
        """
        return _vsp.GetMaterialNames()
    
    @client_wrap
    def SetBackground(self, r, g, b):
        r"""
        Set the background color
    
    
        .. code-block:: python
    
            SetBackground( 1.0, 1.0, 1.0 )                                 # Set background to bright white
    
    
        :param [in]: r Red 8-bit unsigned integer (range: 0-255)
        :param [in]: g Green 8-bit unsigned integer (range: 0-255)
        :param [in]: b Blue 8-bit unsigned integer (range: 0-255)
        """
        return _vsp.SetBackground(r, g, b)
    
    @client_wrap
    def SetAllViews(self, view):
        r"""
        Set the view of all viewports
    
    
        .. code-block:: python
    
            SetAllViews( CAM_CENTER )
    
    
        :param [in]: view int CAMERA_VIEW enum
        """
        return _vsp.SetAllViews(view)
    
    @client_wrap
    def SetView(self, viewport, view):
        r"""
        Set the view of a particular viewports
    
    
        .. code-block:: python
    
            SetView( 0, CAM_CENTER )
    
    
        :param [in]: viewport int Viewport to set view
        :param [in]: view int CAMERA_VIEW enum
        """
        return _vsp.SetView(viewport, view)
    
    @client_wrap
    def FitAllViews(self, ):
        r"""
        Fit contents to all viewports
    
    
        .. code-block:: python
    
            FitAllViews()
    
    
        """
        return _vsp.FitAllViews()
    
    @client_wrap
    def ResetViews(self, ):
        r"""
        Reset views of all viewports
    
    
        .. code-block:: python
    
            ResetViews()
    
    
        """
        return _vsp.ResetViews()
    
    @client_wrap
    def SetWindowLayout(self, r, c):
        r"""
        Set the rows and columns of the window layout
    
    
        .. code-block:: python
    
            SetWindowLayout( 2, 2 )
    
    
        :param [in]: r int Number of viewport rows
        :param [in]: c int Number of viewport columns
        """
        return _vsp.SetWindowLayout(r, c)
    
    @client_wrap
    def SetGUIElementDisable(self, e, state):
        r"""
        Set whether all instances of GUI device type are disabled
    
    
        .. code-block:: python
    
            SetGUIElementDisable( GDEV_INPUT, True )
    
        :param [in]: e int GDEV enum for GUI device type
        :param [in]: state bool True to disable GUI device type
        """
        return _vsp.SetGUIElementDisable(e, state)
    
    @client_wrap
    def SetGUIScreenDisable(self, s, state):
        r"""
        Set whether screen is disabled
    
    
        .. code-block:: python
    
            SetGUIScreenDisable( VSP_CFD_MESH_SCREEN, True )
    
        :param [in]: s int GUI_VSP_SCREEN enum for screen
        :param [in]: state bool True to disable screen
        """
        return _vsp.SetGUIScreenDisable(s, state)
    
    @client_wrap
    def SetGeomScreenDisable(self, s, state):
        r"""
        Set whether geom screen is disabled
    
    
        .. code-block:: python
    
            SetGeomScreenDisable( ALL_GEOM_SCREENS, True )
    
        :param [in]: s int GUI_GEOM_SCREEN enum for geom screen
        :param [in]: state bool True to disable geom screen
        """
        return _vsp.SetGeomScreenDisable(s, state)
    
    @client_wrap
    def HideScreen(self, s):
        r"""
        Hide an OpenVSP GUI screen
    
    
        .. code-block:: python
    
            HideScreen( VSP_INTERFERENCE_SCREEN )
    
        :param [in]: s int GUI_VSP_SCREEN enum for screen
        """
        return _vsp.HideScreen(s)
    
    @client_wrap
    def ShowScreen(self, s):
        r"""
        Show an OpenVSP GUI screen
    
    
        .. code-block:: python
    
            ShowScreen( VSP_INTERFERENCE_SCREEN )
    
        :param [in]: s int GUI_VSP_SCREEN enum for screen
        """
        return _vsp.ShowScreen(s)
    
    @client_wrap
    def GetGeomTypes(self, ):
        r"""
        Get an array of all Geom types (i.e FUSELAGE, POD, etc.)
    
    
        .. code-block:: python
    
            #==== Add Pod Geometries ====//
            pod1 = AddGeom( "POD", "" )
            pod2 = AddGeom( "POD", "" )
    
            type_array = GetGeomTypes()
    
            if ( type_array[0] != "POD" ): print( "---> Error: API GetGeomTypes  " )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Geom type names
        """
        return _vsp.GetGeomTypes()
    
    @client_wrap
    def AddGeom(self, *args):
        r"""
        Add a new Geom of given type as a child of the specified parent. If no parent or an invalid parent is given, the Geom is placed at the top level
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
    
        :param [in]: type Geom type (i.e FUSELAGE, POD, etc.)
        :param [in]: parent Parent Geom ID
        :rtype: string
        :return: Geom ID
        """
        return _vsp.AddGeom(*args)
    
    @client_wrap
    def UpdateGeom(self, geom_id):
        r"""
        Perform an update for the specified Geom
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            SetParmVal( pod_id, "X_Rel_Location", "XForm", 5.0 )
    
            UpdateGeom( pod_id ) # Faster than updating the whole vehicle
    
    
        See also: Update()
        :param [in]: geom_id string Geom ID
        """
        return _vsp.UpdateGeom(geom_id)
    
    @client_wrap
    def DeleteGeom(self, geom_id):
        r"""
        Delete a particular Geom
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            DeleteGeom( wing_id )
    
    
        :param [in]: geom_id string Geom ID
        """
        return _vsp.DeleteGeom(geom_id)
    
    @client_wrap
    def DeleteGeomVec(self, del_vec):
        r"""
        Delete multiple Geoms
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            rid = ExecAnalysis( "CompGeom" )
    
            mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )
    
            DeleteGeomVec( mesh_id_vec )
    
    
        :param [in]: del_vec vector<string> Vector of Geom IDs
        """
        return _vsp.DeleteGeomVec(del_vec)
    
    @client_wrap
    def CutGeomToClipboard(self, geom_id):
        r"""
        Cut Geom from current location and store on clipboard
    
    
        .. code-block:: python
    
            #==== Add Pod Geometries ====//
            pid1 = AddGeom( "POD", "" )
            pid2 = AddGeom( "POD", "" )
    
            CutGeomToClipboard( pid1 )
    
            PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2
    
            geom_ids = FindGeoms()
    
            if  len(geom_ids) != 2 : print( "---> Error: API Cut/Paste Geom  " )
    
    
        See also: PasteGeomClipboard
        :param [in]: geom_id string Geom ID
        """
        return _vsp.CutGeomToClipboard(geom_id)
    
    @client_wrap
    def CopyGeomToClipboard(self, geom_id):
        r"""
        Copy Geom from current location and store on clipboard
    
    
        .. code-block:: python
    
            #==== Add Pod Geometries ====//
            pid1 = AddGeom( "POD", "" )
            pid2 = AddGeom( "POD", "" )
    
            CopyGeomToClipboard( pid1 )
    
            PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2
    
            geom_ids = FindGeoms()
    
            if  len(geom_ids) != 3 : print( "---> Error: API Copy/Paste Geom  " )
    
    
        See also: PasteGeomClipboard
        :param [in]: geom_id string Geom ID
        """
        return _vsp.CopyGeomToClipboard(geom_id)
    
    @client_wrap
    def PasteGeomClipboard(self, *args):
        r"""
        Paste Geom from clipboard into the model. The Geom is pasted as a child of the specified parent, but will be placed at top level if no parent or an invalid one is provided.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometries ====//
            pid1 = AddGeom( "POD", "" )
            pid2 = AddGeom( "POD", "" )
    
            CutGeomToClipboard( pid1 )
    
            PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2
    
            geom_ids = FindGeoms()
    
            if  len(geom_ids) != 2 : print( "---> Error: API Cut/Paste Geom  " )
    
    
        :param [in]: parent string Parent Geom ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Vector of pasted Geom IDs
        """
        return _vsp.PasteGeomClipboard(*args)
    
    @client_wrap
    def FindGeoms(self, ):
        r"""
        Find and return all Geom IDs in the model
    
    
        .. code-block:: python
    
            #==== Add Pod Geometries ====//
            pod1 = AddGeom( "POD", "" )
            pod2 = AddGeom( "POD", "" )
    
            #==== There Should Be Two Geoms =====//
            geom_ids = FindGeoms()
    
            if  len(geom_ids) != 2 : print( "---> Error: API FindGeoms " )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of all Geom IDs
        """
        return _vsp.FindGeoms()
    
    @client_wrap
    def FindGeomsWithName(self, name):
        r"""
        Find and return all Geom IDs with the specified name
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            SetGeomName( pid, "ExamplePodName" )
    
            geom_ids = FindGeomsWithName( "ExamplePodName" )
    
            if  len(geom_ids) != 1 :
                print( "---> Error: API FindGeomsWithName " )
    
    
        See also: FindGeom
        :param [in]: name Geom name
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Geom IDs
        """
        return _vsp.FindGeomsWithName(name)
    
    @client_wrap
    def FindGeom(self, name, index):
        r"""
        Find and return the Geom ID with the specified name at given index. Equivalent to FindGeomsWithName( name )[index].
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            SetGeomName( pid, "ExamplePodName" )
    
            geom_id = FindGeom( "ExamplePodName", 0 )
    
            geom_ids = FindGeomsWithName( "ExamplePodName" )
    
            if  geom_ids[0] != geom_id :
                print( "---> Error: API FindGeom & FindGeomsWithName" )
    
    
        See also: FindGeomsWithName
        :param [in]: name Geom name
        :param [in]: index
        :rtype: string
        :return: Geom ID with name at specified index
        """
        return _vsp.FindGeom(name, index)
    
    @client_wrap
    def SetGeomName(self, geom_id, name):
        r"""
        Set the name of the specified Geom
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            SetGeomName( pid, "ExamplePodName" )
    
            geom_ids = FindGeomsWithName( "ExamplePodName" )
    
            if  len(geom_ids) != 1 :
                print( "---> Error: API FindGeomsWithName " )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: name Geom name
        """
        return _vsp.SetGeomName(geom_id, name)
    
    @client_wrap
    def GetGeomName(self, geom_id):
        r"""
        Get the name of a specific Geom
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            SetGeomName( pid, "ExamplePodName" )
    
            name_str = "Geom Name: " + GetGeomName( pid )
    
            print( name_str )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: string
        :return: Geom name
        """
        return _vsp.GetGeomName(geom_id)
    
    @client_wrap
    def GetGeomParmIDs(self, geom_id):
        r"""
        Get all Parm IDs associated with this Geom Parm container
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD", "" )
    
            print( "---> Test Get Parm Arrays" )
    
            parm_array = GetGeomParmIDs( pid )
    
            if  len(parm_array) < 1 : print( "---> Error: API GetGeomParmIDs " )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm IDs
        """
        return _vsp.GetGeomParmIDs(geom_id)
    
    @client_wrap
    def GetGeomTypeName(self, geom_id):
        r"""
        Get the type name of specified Geom (i.e. FUSELAGE)
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            print( "Geom Type Name: ", False )
    
            print( GetGeomTypeName( wing_id ) )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: string
        :return: Geom type name
        """
        return _vsp.GetGeomTypeName(geom_id)
    
    @client_wrap
    def GetParm(self, geom_id, name, group):
        r"""
        Get Parm ID
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            lenid = GetParm( pid, "Length", "Design" )
    
            if  not ValidParm( lenid ) : print( "---> Error: API GetParm  " )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: name string Parm name
        :param [in]: group string Parm group name
        :rtype: string
        :return: string Parm ID
        """
        return _vsp.GetParm(geom_id, name, group)
    
    @client_wrap
    def SetGeomParent(self, geom_id, parent_id):
        r"""
        Get the parent Geom ID for the input child Geom. "NONE" is returned if the Geom has no parent.
    
    
        .. code-block:: python
    
            #==== Reparent two PodGeoms ====#
            pod1 = AddGeom( "POD" )
            pod2 = AddGeom( "POD", pod1 )
            pod3 = AddGeom ("POD" )
    
            veh_id = GetVehicleID()
    
            SetGeomParent( pod2, veh_id )
            SetGeomParent( pod3, pod1 )
    
            pod2_parent = GetGeomParent( pod2 )
            pod3_parent = GetGeomParent( pod3 )
    
            if ( pod2_parent != "NONE" or pod3_parent != pod1 ):
                print( "SetGeomParent error!" )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: parent_id string Parent Geom ID
        """
        return _vsp.SetGeomParent(geom_id, parent_id)
    
    @client_wrap
    def GetGeomParent(self, geom_id):
        r"""
        Get the parent Geom ID for the input child Geom. "NONE" is returned if the Geom has no parent.
    
    
        .. code-block:: python
    
            #==== Add Parent and Child Geometry ====//
            pod1 = AddGeom( "POD" )
    
            pod2 = AddGeom( "POD", pod1 )
    
            print( "Parent ID of Pod #2: ", False )
    
            print( GetGeomParent( pod2 ) )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: string
        :return: string Parent Geom ID
        """
        return _vsp.GetGeomParent(geom_id)
    
    @client_wrap
    def GetGeomChildren(self, geom_id):
        r"""
        Get the IDs for each child of the input parent Geom.
    
    
        .. code-block:: python
    
            #==== Add Parent and Child Geometry ====//
            pod1 = AddGeom( "POD" )
    
            pod2 = AddGeom( "POD", pod1 )
    
            pod3 = AddGeom( "POD", pod2 )
    
            print( "Children of Pod #1: " )
    
            children = GetGeomChildren( pod1 )
    
            for i in range(int( len(children) )):
    
                print( "\t", False )
                print( children[i] )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Vector of child Geom IDs
        """
        return _vsp.GetGeomChildren(geom_id)
    
    @client_wrap
    def GetNumXSecSurfs(self, geom_id):
        r"""
        Get the number of XSecSurfs for the specified Geom
    
    
        .. code-block:: python
    
            #==== Add Fuselage Geometry ====//
            fuseid = AddGeom( "FUSELAGE", "" )
    
            num_xsec_surfs = GetNumXSecSurfs( fuseid )
    
            if  num_xsec_surfs != 1 : print( "---> Error: API GetNumXSecSurfs  " )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: int
        :return: int Number of XSecSurfs
        """
        return _vsp.GetNumXSecSurfs(geom_id)
    
    @client_wrap
    def GetNumMainSurfs(self, geom_id):
        r"""
        Get the number of main surfaces for the specified Geom. Multiple main surfaces may exist for CustoGeoms, propellors, etc., but
        does not include surfaces created due to symmetry.
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            num_surf = 0
    
            num_surf = GetNumMainSurfs( prop_id ) # Should be the same as the number of blades
    
            print( "Number of Propeller Surfaces: ", False )
    
            print( num_surf )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: int
        :return: int Number of main surfaces
        """
        return _vsp.GetNumMainSurfs(geom_id)
    
    @client_wrap
    def GetTotalNumSurfs(self, geom_id):
        r"""
        Get the total number of surfaces for the specified Geom. This is equivalent to the number of main surface multiplied
        by the number of symmetric copies.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            num_surf = 0
    
            num_surf = GetTotalNumSurfs( wing_id ) # Wings default with XZ symmetry on -> 2 surfaces
    
            print( "Total Number of Wing Surfaces: ", False )
    
            print( num_surf )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: int
        :return: Number of main surfaces
        """
        return _vsp.GetTotalNumSurfs(geom_id)
    
    @client_wrap
    def GetGeomVSPSurfType(self, geom_id, main_surf_ind=0):
        r"""
        Get the VSP surface type of the specified Geom
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            if  GetGeomVSPSurfType( wing_id ) != WING_SURF :
                print( "---> Error: API GetGeomVSPSurfType " )
    
    
        See also: VSP_SURF_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: main_surf_ind Main surface index
        :rtype: int
        :return: VSP surface type enum (i.e. DISK_SURF)
        """
        return _vsp.GetGeomVSPSurfType(geom_id, main_surf_ind)
    
    @client_wrap
    def GetGeomVSPSurfCfdType(self, geom_id, main_surf_ind=0):
        r"""
        Get the VSP surface CFD type of the specified Geom
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            if  GetGeomVSPSurfCfdType( wing_id ) != CFD_NORMAL :
                print( "---> Error: API GetGeomVSPSurfCfdType " )
    
    
        See also: VSP_SURF_CFD_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: main_surf_ind Main surface index
        :rtype: int
        :return: VSP surface CFD type enum (i.e. CFD_TRANSPARENT)
        """
        return _vsp.GetGeomVSPSurfCfdType(geom_id, main_surf_ind)
    
    @client_wrap
    def GetGeomBBoxMax(self, geom_id, main_surf_ind=0, ref_frame_is_absolute=True):
        r"""
        Get the the maximum coordinate of the bounding box of a Geom with given main surface index. The Geom bounding
        box may be specified in absolute or body reference frame.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            SetParmVal( FindParm( pid, "Y_Rotation", "XForm" ), 45 )
            SetParmVal( FindParm( pid, "Z_Rotation", "XForm" ), 25 )
    
            Update()
    
            max_pnt = GetGeomBBoxMax( pid, 0, False )
    
    
        See also: GetGeomBBoxMin
        :param [in]: geom_id string Geom ID
        :param [in]: main_surf_ind Main surface index
        :param [in]: ref_frame_is_absolute Flag to specify absolute or body reference frame
        :rtype: :py:class:`vec3d`
        :return: Maximum coordinate of the bounding box
        """
        return _vsp.GetGeomBBoxMax(geom_id, main_surf_ind, ref_frame_is_absolute)
    
    @client_wrap
    def GetGeomBBoxMin(self, geom_id, main_surf_ind=0, ref_frame_is_absolute=True):
        r"""
        Get the the minimum coordinate of the bounding box of a Geom with given main surface index. The Geom bounding
        box may be specified in absolute or body reference frame.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            SetParmVal( FindParm( pid, "Y_Rotation", "XForm" ), 45 )
            SetParmVal( FindParm( pid, "Z_Rotation", "XForm" ), 25 )
    
            Update()
    
            min_pnt = GetGeomBBoxMin( pid, 0, False )
    
    
        See also: GetGeomBBoxMax
        :param [in]: geom_id string Geom ID
        :param [in]: main_surf_ind Main surface index
        :param [in]: ref_frame_is_absolute Flag to specify absolute or body reference frame
        :rtype: :py:class:`vec3d`
        :return: Minimum coordinate of the bounding box
        """
        return _vsp.GetGeomBBoxMin(geom_id, main_surf_ind, ref_frame_is_absolute)
    
    @client_wrap
    def AddSubSurf(self, geom_id, type, surfindex=0):
        r"""
        Add a sub-surface to the specified Geom
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            # Note: Parm Group for SubSurfaces in the form: "SS_" + type + "_" + count (initialized at 1)
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
    
            SetParmVal( wid, "Const_Line_Value", "SubSurface_1", 0.4 )     # Change Location
    
    
        See also: SUBSURF_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: type Sub-surface type enum (i.e. SS_RECTANGLE)
        :param [in]: surfindex Main surface index (default: 0)
        :rtype: string
        :return: Sub-surface ID
        """
        return _vsp.AddSubSurf(geom_id, type, surfindex)
    
    @client_wrap
    def GetSubSurf(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Get the ID of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            ss_rec_1 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #1
    
            ss_rec_2 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #2
    
            print( ss_rec_2, False )
    
            print( " = ", False )
    
            print( GetSubSurf( wid, 1 ) )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: index Sub-surface index
        :rtype: string
        :return: Sub-surface ID
    
    
        |
    
        *Overload 2:*
    
    
    
        Get the ID of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            ss_rec_1 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #1
    
            ss_rec_2 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #2
    
            print( ss_rec_2, False )
    
            print( " = ", False )
    
            print( GetSubSurf( wid, 1 ) )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: name string Sub surface name
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Vector of sub-surface ID
        """
        return _vsp.GetSubSurf(*args)
    
    @client_wrap
    def DeleteSubSurf(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Delete the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            print("Delete SS_Line\n")
    
            DeleteSubSurf( wid, ss_line_id )
    
            num_ss = GetNumSubSurf( wid )
    
            num_str = f"Number of SubSurfaces: {num_ss}\n"
    
            print( num_str )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: sub_id string Sub-surface ID
    
    
        |
    
        *Overload 2:*
    
    
    
        Delete the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            print("Delete SS_Line\n")
    
            DeleteSubSurf( ss_line_id )
    
            num_ss = GetNumSubSurf( wid )
    
            num_str = f"Number of SubSurfaces: {num_ss}\n"
    
            print( num_str )
    
    
        :param [in]: sub_id string Sub-surface ID
        """
        return _vsp.DeleteSubSurf(*args)
    
    @client_wrap
    def SetSubSurfName(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Set the name of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            new_name = "New_SS_Rec_Name"
    
            SetSubSurfName( wid, ss_rec_id, new_name )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: sub_id string Sub-surface ID
        :param [in]: name string Sub-surface name
    
    
        |
    
        *Overload 2:*
    
    
    
        Set the name of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            new_name = "New_SS_Rec_Name"
    
            SetSubSurfName( ss_rec_id, new_name )
    
    
        :param [in]: sub_id string Sub-surface ID
        :param [in]: name string Sub-surface name
        """
        return _vsp.SetSubSurfName(*args)
    
    @client_wrap
    def GetSubSurfName(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Get the name of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            rec_name = GetSubSurfName( wid, ss_rec_id )
    
            name_str = "Current Name of SS_Rectangle: " + rec_name + "\n"
    
            print( name_str )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: sub_id string Sub-surface ID
        :rtype: string
        :return: Sub-surface name
    
    
        |
    
        *Overload 2:*
    
    
    
        Get the name of the specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            rec_name = GetSubSurfName( wid, ss_rec_id )
    
            name_str = "Current Name of SS_Rectangle: " + rec_name + "\n"
    
            print( name_str )
    
    
        :param [in]: sub_id string Sub-surface ID
        :rtype: string
        :return: string Sub-surface name
        """
        return _vsp.GetSubSurfName(*args)
    
    @client_wrap
    def GetSubSurfIndex(self, sub_id):
        r"""
        Get the index of the specified sub-surface in its parent Geom's sub-surface vector
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            ind = GetSubSurfIndex( ss_rec_id )
    
            ind_str = f"Index of SS_Rectangle: {ind}"
    
            print( ind_str )
    
    
        :param [in]: sub_id string Sub-surface ID
        :rtype: int
        :return: int Sub-surface index
        """
        return _vsp.GetSubSurfIndex(sub_id)
    
    @client_wrap
    def GetSubSurfIDVec(self, geom_id):
        r"""
        Get a vector of all sub-surface IDs for the specified geometry
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            id_vec = GetSubSurfIDVec( wid )
    
            id_type_str = "SubSurface IDs and Type Indexes -> "
    
            for i in range(len(id_vec)):
    
                id_type_str += id_vec[i]
    
                id_type_str += ": "
    
                id_type_str += f'{GetSubSurfType(id_vec[i])}'
    
                id_type_str += "\t"
    
            id_type_str += "\n"
    
            print( id_type_str )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<int> Array of sub-surface IDs
        """
        return _vsp.GetSubSurfIDVec(geom_id)
    
    @client_wrap
    def GetAllSubSurfIDs(self, ):
        r"""
        Get a vector of all sub-surface IDs for the entire model
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of sub-surface IDs
        """
        return _vsp.GetAllSubSurfIDs()
    
    @client_wrap
    def GetNumSubSurf(self, geom_id):
        r"""
        Get the number of sub-surfaces for the specified Geom
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            num_ss = GetNumSubSurf( wid )
    
            num_str = "Number of SubSurfaces: {num_ss}"
    
            print( num_str )
    
    
        :param [in]: geom_id string Geom ID
        :rtype: int
        :return: int Number of Sub-surfaces
        """
        return _vsp.GetNumSubSurf(geom_id)
    
    @client_wrap
    def GetSubSurfType(self, sub_id):
        r"""
        Get the type for the specified sub-surface (i.e. SS_RECTANGLE)
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
            ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle
    
            id_vec = GetSubSurfIDVec( wid )
    
            id_type_str = "SubSurface IDs and Type Indexes -> "
    
            for i in range(len(id_vec)):
    
                id_type_str += id_vec[i]
    
                id_type_str += ": "
    
                id_type_str += f'{GetSubSurfType(id_vec[i])}'
    
                id_type_str += "\t"
    
            id_type_str += "\n"
    
            print( id_type_str )
    
    
        See also: SUBSURF_TYPE
        :param [in]: sub_id string Sub-surface ID
        :rtype: int
        :return: int Sub-surface type enum (i.e. SS_RECTANGLE)
        """
        return _vsp.GetSubSurfType(sub_id)
    
    @client_wrap
    def GetSubSurfParmIDs(self, sub_id):
        r"""
        Get the vector of Parm IDs for specified sub-surface
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
    
            # Get and list all Parm info for SS_Line
            parm_id_vec = GetSubSurfParmIDs( ss_line_id )
    
            for i in range(len(parm_id_vec)):
    
                id_name_str = "\tName: " + GetParmName(parm_id_vec[i]) + ", Group: " + GetParmDisplayGroupName(parm_id_vec[i]) + ", ID: " + str(parm_id_vec[i]) + "\n"
    
    
                print( id_name_str )
    
    
        :param [in]: sub_id string Sub-surface ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Vector of Parm IDs
        """
        return _vsp.GetSubSurfParmIDs(sub_id)
    
    @client_wrap
    def AddFeaStruct(self, geom_id, init_skin=True, surfindex=0):
        r"""
        Add an FEA Structure to a specified Geom
        Warning: init_skin should ALWAYS be set to true.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: init_skin Flag to initialize the FEA Structure by creating an FEA Skin from the parent Geom's OML at surfindex
        :param [in]: surfindex Main surface index for the FEA Structure
        :rtype: int
        :return: FEA Structure index
        """
        return _vsp.AddFeaStruct(geom_id, init_skin, surfindex)
    
    @client_wrap
    def SetFeaMeshStructIndex(self, struct_index):
        r"""
        Sets FeaMeshMgr m_FeaMeshStructIndex member using passed in index of a FeaStructure
    
    
        .. code-block:: python
    
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            SetFeaMeshStructIndex( struct_ind )
    
            if  len(FindGeoms()) != 0 : print( "ERROR: VSPRenew" )
    
    
        """
        return _vsp.SetFeaMeshStructIndex(struct_index)
    
    @client_wrap
    def DeleteFeaStruct(self, geom_id, fea_struct_ind):
        r"""
        Delete an FEA Structure and all FEA Parts and FEA SubSurfaces associated with it
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind_1 = AddFeaStruct( pod_id )
    
            struct_ind_2 = AddFeaStruct( pod_id )
    
            DeleteFeaStruct( pod_id, struct_ind_1 )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        """
        return _vsp.DeleteFeaStruct(geom_id, fea_struct_ind)
    
    @client_wrap
    def GetFeaStructID(self, geom_id, fea_struct_ind):
        r"""
        Get the ID of an FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :rtype: string
        :return: FEA Structure ID
        """
        return _vsp.GetFeaStructID(geom_id, fea_struct_ind)
    
    @client_wrap
    def GetFeaStructIndex(self, struct_id):
        r"""
        Get the index of an FEA Structure in its Parent Geom's vector of Structures
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind_1 = AddFeaStruct( pod_id )
    
            struct_ind_2 = AddFeaStruct( pod_id )
    
            struct_id_2 = GetFeaStructID( pod_id, struct_ind_2 )
    
            DeleteFeaStruct( pod_id, struct_ind_1 )
    
            struct_ind_2_new = GetFeaStructIndex( struct_id_2 )
    
    
        :param [in]: struct_id FEA Structure ID
        :rtype: int
        :return: FEA Structure index
        """
        return _vsp.GetFeaStructIndex(struct_id)
    
    @client_wrap
    def GetFeaStructParentGeomID(self, struct_id):
        r"""
        Get the Parent Geom ID for an FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Get Parent Geom ID and Index ====//
            parent_id = GetFeaStructParentGeomID( struct_id )
    
    
        :param [in]: struct_id FEA Structure ID
        :rtype: string
        :return: Parent Geom ID
        """
        return _vsp.GetFeaStructParentGeomID(struct_id)
    
    @client_wrap
    def GetFeaStructName(self, geom_id, fea_struct_ind):
        r"""
        Get the name of an FEA Structure. The FEA Structure name functions as the the Parm Container name
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Get Structure Name ====//
            parm_container_name = GetFeaStructName( pod_id, struct_ind )
    
            display_name = "Current Structure Parm Container Name: " + parm_container_name + "\n"
    
            print( display_name )
    
    
        See also: FindContainer, SetFeaStructName
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :rtype: string
        :return: Name for the FEA Structure
        """
        return _vsp.GetFeaStructName(geom_id, fea_struct_ind)
    
    @client_wrap
    def SetFeaStructName(self, geom_id, fea_struct_ind, name):
        r"""
        Set the name of an FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Change the Structure Name ====//
            SetFeaStructName( pod_id, struct_ind, "Example_Struct" )
    
            parm_container_id = FindContainer( "Example_Struct", struct_ind )
    
            display_id = "New Structure Parm Container ID: " + parm_container_id + "\n"
    
            print( display_id )
    
    
        See also: GetFeaStructName
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: name New name for the FEA Structure
        """
        return _vsp.SetFeaStructName(geom_id, fea_struct_ind, name)
    
    @client_wrap
    def GetFeaStructIDVec(self, ):
        r"""
        Get the IDs of all FEA Structures in the vehicle
    
    
        .. code-block:: python
    
            #==== Add Geometries ====//
            pod_id = AddGeom( "POD" )
            wing_id = AddGeom( "WING" )
    
            #==== Add FeaStructures ====//
            pod_struct_ind = AddFeaStruct( pod_id )
            wing_struct_ind = AddFeaStruct( wing_id )
    
            struct_id_vec = GetFeaStructIDVec()
    
    
        See also: NumFeaStructures
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of FEA Structure IDs
        """
        return _vsp.GetFeaStructIDVec()
    
    @client_wrap
    def SetFeaPartName(self, part_id, name):
        r"""
        Set the name of an FEA Part
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add Bulkead ====//
            bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            SetFeaPartName( bulkhead_id, "Bulkhead" )
    
    
        See also: GetFeaPartName
        :param [in]: part_id FEA Part ID
        :param [in]: name New name for the FEA Part
        """
        return _vsp.SetFeaPartName(part_id, name)
    
    @client_wrap
    def AddFeaPart(self, geom_id, fea_struct_ind, type):
        r"""
        Add an FEA Part to a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add Bulkead ====//
            bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            SetParmVal( FindParm( bulkhead_id, "IncludedElements", "FeaPart" ), FEA_SHELL_AND_BEAM )
    
            SetParmVal( FindParm( bulkhead_id, "RelCenterLocation", "FeaPart" ), 0.15 )
    
    
        See also: FEA_PART_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: type FEA Part type enum (i.e. FEA_RIB)
        :rtype: string
        :return: FEA Part ID
        """
        return _vsp.AddFeaPart(geom_id, fea_struct_ind, type)
    
    @client_wrap
    def DeleteFeaPart(self, geom_id, fea_struct_ind, part_id):
        r"""
        Delete an FEA Part from a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add Bulkead ====//
            bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            #==== Add Fixed Point ====//
            fixed_id = AddFeaPart( pod_id, struct_ind, FEA_FIX_POINT )
    
            #==== Delete Bulkead ====//
            DeleteFeaPart( pod_id, struct_ind, bulkhead_id )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: part_id FEA Part ID
        """
        return _vsp.DeleteFeaPart(geom_id, fea_struct_ind, part_id)
    
    @client_wrap
    def GetFeaPartID(self, fea_struct_id, fea_part_index):
        r"""
        Get the Parm ID of an FEA Part, identified from a FEA Structure Parm ID and FEA Part index.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Add Bulkead ====//
            bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            Update()
    
            if  bulkhead_id != GetFeaPartID( struct_id, 1 ) : # These should be equivalent (index 0 is skin)
    
                print( "Error: GetFeaPartID" )
    
    
        :param [in]: fea_struct_id FEA Structure ID
        :param [in]: fea_part_index FEA Part index
        :rtype: string
        :return: FEA Part ID
        """
        return _vsp.GetFeaPartID(fea_struct_id, fea_part_index)
    
    @client_wrap
    def GetFeaPartName(self, part_id):
        r"""
        Get the name of an FEA Part
    
    
        .. code-block:: python
    
            #==== Add Fuselage Geometry ====//
            fuse_id = AddGeom( "FUSELAGE" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( fuse_id )
    
            #==== Add Bulkead ====//
            bulkhead_id = AddFeaPart( fuse_id, struct_ind, FEA_SLICE )
    
            name = "example_name"
            SetFeaPartName( bulkhead_id, name )
    
            if  name != GetFeaPartName( bulkhead_id ) : # These should be equivalent
    
                print( "Error: GetFeaPartName" )
    
    
        See also: SetFeaPartName
        :param [in]: part_id FEA Part ID
        :rtype: string
        :return: FEA Part name
        """
        return _vsp.GetFeaPartName(part_id)
    
    @client_wrap
    def GetFeaPartType(self, part_id):
        r"""
        Get the type of an FEA Part
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add Slice ====//
            slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            if  FEA_SLICE != GetFeaPartType( slice_id ) : # These should be equivalent
    
                print( "Error: GetFeaPartType" )
    
    
        See also: FEA_PART_TYPE
        :param [in]: part_id FEA Part ID
        :rtype: int
        :return: FEA Part type enum
        """
        return _vsp.GetFeaPartType(part_id)
    
    @client_wrap
    def GetFeaPartIDVec(self, fea_struct_id):
        r"""
        Get the IDs of all FEA Parts in the given FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Geometries ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Add FEA Parts ====//
            slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
            dome_id = AddFeaPart( pod_id, struct_ind, FEA_DOME )
    
            part_id_vec = GetFeaPartIDVec( struct_id ) # Should include slice_id & dome_id
    
    
        See also: NumFeaParts
        :param [in]: fea_struct_id FEA Structure ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of FEA Part IDs
        """
        return _vsp.GetFeaPartIDVec(fea_struct_id)
    
    @client_wrap
    def GetFeaSubSurfIDVec(self, fea_struct_id):
        r"""
        Get the IDs of all FEA SubSurfaces in the given FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Geometries ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Add SubSurfaces ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
            rectangle_id = AddFeaSubSurf( pod_id, struct_ind, SS_RECTANGLE )
    
            part_id_vec = GetFeaSubSurfIDVec( struct_id ) # Should include line_array_id & rectangle_id
    
    
        See also: NumFeaSubSurfs
        :param [in]: fea_struct_id FEA Structure ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of FEA Part IDs
        """
        return _vsp.GetFeaSubSurfIDVec(fea_struct_id)
    
    @client_wrap
    def SetFeaPartPerpendicularSparID(self, part_id, perpendicular_spar_id):
        r"""
        Set the ID of the perpendicular spar for an FEA Rib or Rib Array. Note, the FEA Rib or Rib Array should have "SPAR_NORMAL"
        set for the "PerpendicularEdgeType" Parm. If it is not, the ID will still be set, but the orientation of the Rib or Rib
        Array will not change.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add FeaStructure to Wing ====//
            struct_ind = AddFeaStruct( wing_id )
    
            #==== Add Rib ====//
            rib_id = AddFeaPart( wing_id, struct_ind, FEA_RIB )
    
            #==== Add Spars ====//
            spar_id_1 = AddFeaPart( wing_id, struct_ind, FEA_SPAR )
            spar_id_2 = AddFeaPart( wing_id, struct_ind, FEA_SPAR )
    
            SetParmVal( FindParm( spar_id_1, "RelCenterLocation", "FeaPart" ), 0.25 )
            SetParmVal( FindParm( spar_id_2, "RelCenterLocation", "FeaPart" ), 0.75 )
    
            #==== Set Perpendicular Edge type to SPAR ====//
            SetParmVal( FindParm( rib_id, "PerpendicularEdgeType", "FeaRib" ), SPAR_NORMAL )
    
            SetFeaPartPerpendicularSparID( rib_id, spar_id_2 )
    
            if  spar_id_2 != GetFeaPartPerpendicularSparID( rib_id ) :
                print( "Error: SetFeaPartPerpendicularSparID" )
    
    
        See also: FEA_RIB_NORMAL, GetFeaPartPerpendicularSparID
        :param [in]: part_id FEA Part ID (Rib or Rib Array Type)
        :param [in]: perpendicular_spar_id FEA Spar ID
        """
        return _vsp.SetFeaPartPerpendicularSparID(part_id, perpendicular_spar_id)
    
    @client_wrap
    def GetFeaPartPerpendicularSparID(self, part_id):
        r"""
        Get the ID of the perpendicular spar for an FEA Rib or Rib Array. Note, the FEA Rib or Rib Array doesn't have to have "SPAR_NORMAL"
        set for the "PerpendicularEdgeType" Parm for this function to still return a value.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add FeaStructure to Wing ====//
            struct_ind = AddFeaStruct( wing_id )
    
            #==== Add Rib ====//
            rib_id = AddFeaPart( wing_id, struct_ind, FEA_RIB )
    
            #==== Add Spars ====//
            spar_id_1 = AddFeaPart( wing_id, struct_ind, FEA_SPAR )
            spar_id_2 = AddFeaPart( wing_id, struct_ind, FEA_SPAR )
    
            SetParmVal( FindParm( spar_id_1, "RelCenterLocation", "FeaPart" ), 0.25 )
            SetParmVal( FindParm( spar_id_2, "RelCenterLocation", "FeaPart" ), 0.75 )
    
            #==== Set Perpendicular Edge type to SPAR ====//
            SetParmVal( FindParm( rib_id, "PerpendicularEdgeType", "FeaRib" ), SPAR_NORMAL )
    
            SetFeaPartPerpendicularSparID( rib_id, spar_id_2 )
    
            if  spar_id_2 != GetFeaPartPerpendicularSparID( rib_id ) :
                print( "Error: GetFeaPartPerpendicularSparID" )
    
    
        See also: FEA_RIB_NORMAL, SetFeaPartPerpendicularSparID
        :param [in]: part_id FEA Part ID (Rib or Rib Array Type)
        :rtype: string
        :return: Perpendicular FEA Spar ID
        """
        return _vsp.GetFeaPartPerpendicularSparID(part_id)
    
    @client_wrap
    def SetFeaSubSurfName(self, subsurf_id, name):
        r"""
        Set the name of an FEA SubSurface
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add LineArray ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
    
            SetFeaSubSurfName( line_array_id, "Stiffener_array" )
    
    
        :param [in]: subsurf_id FEA SubSurface ID
        :param [in]: name New name for the FEA SubSurface
        """
        return _vsp.SetFeaSubSurfName(subsurf_id, name)
    
    @client_wrap
    def GetFeaSubSurfName(self, subsurf_id):
        r"""
        Set the name of an FEA SubSurface
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add LineArray ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
    
            name = "example_name"
            SetFeaSubSurfName( line_array_id, name )
    
            if  name != GetFeaSubSurfName( line_array_id ) : # These should be equivalent
                print( "Error: GetFeaSubSurfName" )
    
    
        :param [in]: subsurf_id FEA SubSurface ID
        :rtype: string
        :return: FEA SubSurf name
        """
        return _vsp.GetFeaSubSurfName(subsurf_id)
    
    @client_wrap
    def AddFeaSubSurf(self, geom_id, fea_struct_ind, type):
        r"""
        Add an FEA SubSurface to a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add LineArray ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
    
            SetParmVal( FindParm( line_array_id, "ConstLineType", "SS_LineArray" ), 1 ) # Constant W
    
            SetParmVal( FindParm( line_array_id, "Spacing", "SS_LineArray" ), 0.25 )
    
    
        See also: SUBSURF_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: type FEA SubSurface type enum (i.e. SS_ELLIPSE)
        :rtype: string
        :return: FEA SubSurface ID
        """
        return _vsp.AddFeaSubSurf(geom_id, fea_struct_ind, type)
    
    @client_wrap
    def DeleteFeaSubSurf(self, geom_id, fea_struct_ind, ss_id):
        r"""
        Delete an FEA SubSurface from a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add LineArray ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
    
            #==== Add Rectangle ====//
            rect_id = AddFeaSubSurf( pod_id, struct_ind, SS_RECTANGLE )
    
            #==== Delete LineArray ====//
            DeleteFeaSubSurf( pod_id, struct_ind, line_array_id )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: ss_id FEA SubSurface ID
        """
        return _vsp.DeleteFeaSubSurf(geom_id, fea_struct_ind, ss_id)
    
    @client_wrap
    def GetFeaSubSurfIndex(self, ss_id):
        r"""
        Get the index of an FEA SubSurface give the SubSurface ID
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Add Slice ====//
            slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
    
            #==== Add LineArray ====//
            line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
    
            #==== Add Rectangle ====//
            rect_id = AddFeaSubSurf( pod_id, struct_ind, SS_RECTANGLE )
    
            if  1 != GetFeaSubSurfIndex( rect_id ) : # These should be equivalent
    
                print( "Error: GetFeaSubSurfIndex" )
    
    
        :param [in]: ss_id FEA SubSurface ID
        :rtype: int
        :return: FEA SubSurface Index
        """
        return _vsp.GetFeaSubSurfIndex(ss_id)
    
    @client_wrap
    def NumFeaStructures(self, ):
        r"""
        Get the total number of FEA Subsurfaces in the vehicle
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add FeaStructure to Pod ====//
            struct_1 = AddFeaStruct( wing_id )
            struct_2 = AddFeaStruct( wing_id )
    
            if  NumFeaStructures() != 2 :
                print( "Error: NumFeaStructures" )
    
    
        See also: GetFeaStructIDVec
        :rtype: int
        :return: Total Number of FEA Structures
        """
        return _vsp.NumFeaStructures()
    
    @client_wrap
    def NumFeaParts(self, fea_struct_id):
        r"""
        Get the number of FEA Parts for a particular FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Add FEA Parts ====//
            slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
            dome_id = AddFeaPart( pod_id, struct_ind, FEA_DOME )
    
            if  NumFeaParts( struct_id ) != 3 : # Includes FeaSkin
    
                print( "Error: NumFeaParts" )
    
    
        See also: GetFeaPartIDVec
        :param [in]: fea_struct_id FEA Structure ID
        :rtype: int
        :return: Number of FEA Parts
        """
        return _vsp.NumFeaParts(fea_struct_id)
    
    @client_wrap
    def NumFeaSubSurfs(self, fea_struct_id):
        r"""
        Get the number of FEA Subsurfaces for a particular FEA Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( wing_id )
    
            struct_id = GetFeaStructID( wing_id, struct_ind )
    
            #==== Add SubSurfaces ====//
            line_array_id = AddFeaSubSurf( wing_id, struct_ind, SS_LINE_ARRAY )
            rectangle_id = AddFeaSubSurf( wing_id, struct_ind, SS_RECTANGLE )
    
            if  NumFeaSubSurfs( struct_id ) != 2 :
                print( "Error: NumFeaSubSurfs" )
    
    
        See also: GetFeaSubSurfIDVec
        :param [in]: fea_struct_id FEA Structure ID
        :rtype: int
        :return: Number of FEA SubSurfaces
        """
        return _vsp.NumFeaSubSurfs(fea_struct_id)
    
    @client_wrap
    def AddFeaBC(self, fea_struct_id, type=-1):
        r"""
        Add an FEA BC to a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind );
    
            #==== Add BC ====//
            bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )
    
    
        See also: FEA_BC_TYPE
        :param [in]: fea_struct_id string FEA Structure ID
        :param [in]: type int FEA BC type enum ( i.e. FEA_BC_STRUCTURE )
        :rtype: string
        :return: FEA BC ID
        """
        return _vsp.AddFeaBC(fea_struct_id, type)
    
    @client_wrap
    def DelFeaBC(self, fea_struct_id, bc_id):
        r"""
        Delete an FEA BC from a Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind );
    
            #==== Add BC ====//
            bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )
    
            DelFeaBC( struct_id, bc_id )
    
    
        See also: FEA_BC_TYPE
        :param [in]: fea_struct_id string FEA Structure ID
        :param [in]: bc_id int FEA BC ID
        """
        return _vsp.DelFeaBC(fea_struct_id, bc_id)
    
    @client_wrap
    def GetFeaBCIDVec(self, fea_struct_id):
        r"""
        Return a vector of FEA BC ID's for a structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind );
    
            #==== Add BC ====//
            bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )
    
            bc_id_vec = GetFeaBCIDVec( struct_id )
    
    
        :param [in]: fea_struct_id string FEA Structure ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of FEA BC IDs
        """
        return _vsp.GetFeaBCIDVec(fea_struct_id)
    
    @client_wrap
    def NumFeaBCs(self, fea_struct_id):
        r"""
        Return number of FEA BC's in a structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind );
    
            #==== Add BC ====//
            bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )
    
            nbc = NumFeaBCs( struct_id )
    
    
        :param [in]: fea_struct_id string FEA Structure ID
        :rtype: int
        :return: Number of FEA BCs
        """
        return _vsp.NumFeaBCs(fea_struct_id)
    
    @client_wrap
    def AddFeaMaterial(self, ):
        r"""
        Add an FEA Material the FEA Mesh material library. Materials are available across all Geoms and Structures.
    
    
        .. code-block:: python
    
            #==== Create FeaMaterial ====//
            mat_id = AddFeaMaterial()
    
            SetParmVal( FindParm( mat_id, "MassDensity", "FeaMaterial" ), 0.016 )
    
    
        :rtype: string
        :return: FEA Material ID
        """
        return _vsp.AddFeaMaterial()
    
    @client_wrap
    def AddFeaProperty(self, property_type=0):
        r"""
        Add aa FEA Property the FEA Mesh property library. Properties are available across all Geoms and Structures. Currently only beam and
        shell properties are available. Note FEA_SHELL_AND_BEAM is not a valid property type.
    
    
        .. code-block:: python
    
            #==== Create FeaProperty ====//
            prop_id = AddFeaProperty()
    
            SetParmVal( FindParm( prop_id, "Thickness", "FeaProperty" ), 0.01 )
    
    
        See also: FEA_PART_ELEMENT_TYPE
        :param [in]: property_type FEA Property type enum (i.e. FEA_SHELL).
        :rtype: string
        :return: FEA Property ID
        """
        return _vsp.AddFeaProperty(property_type)
    
    @client_wrap
    def SetFeaMeshVal(self, geom_id, fea_struct_ind, type, val):
        r"""
        Set the value of a particular FEA Mesh option for the specified Structure. Note, FEA Mesh makes use of enums initially created for CFD Mesh
        but not all CFD Mesh options are available for FEA Mesh.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Adjust FeaMeshSettings ====//
            SetFeaMeshVal( pod_id, struct_ind, CFD_MAX_EDGE_LEN, 0.75 )
    
            SetFeaMeshVal( pod_id, struct_ind, CFD_MIN_EDGE_LEN, 0.2 )
    
    
        See also: CFD_CONTROL_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: type FEA Mesh option type enum (i.e. CFD_MAX_EDGE_LEN)
        :param [in]: val Value the option is set to
        """
        return _vsp.SetFeaMeshVal(geom_id, fea_struct_ind, type, val)
    
    @client_wrap
    def SetFeaMeshFileName(self, geom_id, fea_struct_ind, file_type, file_name):
        r"""
        Set the name of a particular FEA Mesh output file for a specified Structure
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #=== Set Export File Name ===//
            export_name = "FEAMeshTest_calculix.dat"
    
            #==== Get Parent Geom ID and Index ====//
            parent_id = GetFeaStructParentGeomID( struct_id ) # same as pod_id
    
            SetFeaMeshFileName( parent_id, struct_ind, FEA_CALCULIX_FILE_NAME, export_name )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind FEA Structure index
        :param [in]: file_type FEA output file type enum (i.e. FEA_EXPORT_TYPE)
        :param [in]: file_name Name for the output file
        """
        return _vsp.SetFeaMeshFileName(geom_id, fea_struct_ind, file_type, file_name)
    
    @client_wrap
    def ComputeFeaMesh(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Compute an FEA Mesh for a Structure. Only a single output file can be generated with this function.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Generate FEA Mesh and Export ====//
            print( "--> Generating FeaMesh " )
    
            #==== Get Parent Geom ID and Index ====//
            parent_id = GetFeaStructParentGeomID( struct_id ) # same as pod_id
    
            ComputeFeaMesh( parent_id, struct_ind, FEA_CALCULIX_FILE_NAME )
    
    
        See also: SetFeaMeshFileName, FEA_EXPORT_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: fea_struct_ind int FEA Structure index
        :param [in]: file_type int FEA output file type enum (i.e. FEA_EXPORT_TYPE)
    
    
        |
    
        *Overload 2:*
    
    
    
        Compute an FEA Mesh for a Structure. Only a single output file can be generated with this function.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            struct_id = GetFeaStructID( pod_id, struct_ind )
    
            #==== Generate FEA Mesh and Export ====//
            print( string( "--> Generating FeaMesh " ) )
    
            #==== Get Parent Geom ID and Index ====//
            parent_id = GetFeaStructParentGeomID( struct_id ) # same as pod_id
    
            Could also call ComputeFeaMesh ( struct_id, FEA_CALCULIX_FILE_NAME )
    
    
        See also: SetFeaMeshFileName, FEA_EXPORT_TYPE
        :param [in]: struct_id string FEA Structure index
        :param [in]: file_type int FEA output file type enum (i.e. FEA_EXPORT_TYPE)
        """
        return _vsp.ComputeFeaMesh(*args)
    
    @client_wrap
    def SetXSecAlias(self, id, alias):
        r"""
        Set XSec Alias by ID
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Set Alias and verify alias match
            alias = "XSec_One_Alias"
    
            SetXSecAlias( xsec_1, alias )
    
            get_alias = GetXSecAlias( xsec_1 )
    
            if alias != get_alias:
                print("SetXSecAlias/GetXSecAlias error!")
    
    
        :param [in]: id XSec ID
        :param [in]: alias Xsec alias
        """
        return _vsp.SetXSecAlias(id, alias)
    
    @client_wrap
    def GetXSecAlias(self, id):
        r"""
        Get XSec Alias by ID
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Set Alias and verify alias match
            alias = "XSec_One_Alias"
    
            SetXSecAlias( xsec_1, alias )
    
            get_alias = GetXSecAlias( xsec_1 )
    
            if alias != get_alias:
                print("SetXSecAlias/GetXSecAlias error!")
    
    
        :param [in]: id XSec ID
        :rtype: string
        :return: Xsec alias
        """
        return _vsp.GetXSecAlias(id)
    
    @client_wrap
    def SetXSecCurveAlias(self, id, alias):
        r"""
        Set XSecCurve Alias by XSec ID
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Set Alias and verify alias match
            alias = "XSecCurve_One_Alias"
    
            SetXSecCurveAlias( xsec_1, alias )
    
            get_alias = GetXSecCurveAlias( xsec_1 )
    
            if alias != get_alias:
                print("SetXSecCurveAlias/GetXSecCurveAlias error!")
    
    
        :param [in]: id XSec ID
        :param [in]: alias XsecCurve alias
        """
        return _vsp.SetXSecCurveAlias(id, alias)
    
    @client_wrap
    def GetXSecCurveAlias(self, id):
        r"""
        Get XSecCurve Alias by XSec ID
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Set Alias and verify alias match
            alias = "XSecCurve_One_Alias"
    
            SetXSecCurveAlias( xsec_1, alias )
    
            get_alias = GetXSecCurveAlias( xsec_1 )
    
            if alias != get_alias:
                print("SetXSecCurveAlias/GetXSecCurveAlias error!")
    
    
        :param [in]: id XSec ID
        """
        return _vsp.GetXSecCurveAlias(id)
    
    @client_wrap
    def CutXSec(self, geom_id, index):
        r"""
        Cut a cross-section from the specified geometry and maintain it in memory
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            #==== Insert, Cut, Paste Example ====//
            InsertXSec( fid, 1, XS_ROUNDED_RECTANGLE )         # Insert A Cross-Section
    
            CopyXSec( fid, 2 )                                 # Copy Just Created XSec To Clipboard
    
            PasteXSec( fid, 1 )                                # Paste Clipboard
    
            CutXSec( fid, 2 )                                  # Cut Created XSec
    
    
        See also: PasteXSec
        :param [in]: geom_id string Geom ID
        :param [in]: index XSec index
        """
        return _vsp.CutXSec(geom_id, index)
    
    @client_wrap
    def CopyXSec(self, geom_id, index):
        r"""
        Copy a cross-section from the specified geometry and maintain it in memory
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Copy XSec To Clipboard
            CopyXSec( sid, 1 )
    
            # Paste To XSec 3
            PasteXSec( sid, 3 )
    
    
        See also: PasteXSec
        :param [in]: geom_id string Geom ID
        :param [in]: index XSec index
        """
        return _vsp.CopyXSec(geom_id, index)
    
    @client_wrap
    def PasteXSec(self, geom_id, index):
        r"""
        Paste the cross-section currently held in memory to the specified geometry
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Copy XSec To Clipboard
            CopyXSec( sid, 1 )
    
            # Paste To XSec 3
            PasteXSec( sid, 3 )
    
    
        See also: CutXSec, CopyXSec
        :param [in]: geom_id string Geom ID
        :param [in]: index XSec index
        """
        return _vsp.PasteXSec(geom_id, index)
    
    @client_wrap
    def InsertXSec(self, geom_id, index, type):
        r"""
        Insert a cross-section of particular type to the specified geometry after the given index
    
    
        .. code-block:: python
    
            wing_id = AddGeom( "WING" )
    
            #===== Add XSec ====//
            InsertXSec( wing_id, 1, XS_SIX_SERIES )
    
    
        See also: XSEC_CRV_TYPE
        :param [in]: geom_id string Geom ID
        :param [in]: index XSec index
        :param [in]: type XSec type enum (i.e. XS_GENERAL_FUSE)
        """
        return _vsp.InsertXSec(geom_id, index, type)
    
    @client_wrap
    def SplitWingXSec(self, wing_id, section_index):
        r"""
        Split a given wing section.
    
    
        .. code-block:: python
    
            wing_id = AddGeom( "WING", "" )
    
            #==== Set Wing Section Controls ====//
            SplitWingXSec( wing_id, 1 )
    
            Update()
    
        See also: WING_DRIVERS, XSEC_DRIVERS
        :param [in]: wing_id string Geom ID
        :param [in]: section_index Wing section index
        """
        return _vsp.SplitWingXSec(wing_id, section_index)
    
    @client_wrap
    def SetDriverGroup(self, geom_id, section_index, driver_0, driver_1=-1, driver_2=-1):
        r"""
        Set the driver group for a wing section or a XSecCurve. Care has to be taken when setting these driver groups to ensure a valid combination.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry and Set Parms ====//
            wing_id = AddGeom( "WING", "" )
    
            #==== Set Wing Section Controls ====//
            SetDriverGroup( wing_id, 1, AR_WSECT_DRIVER, ROOTC_WSECT_DRIVER, TIPC_WSECT_DRIVER )
    
            Update()
    
            #==== Set Parms ====//
            SetParmVal( wing_id, "Root_Chord", "XSec_1", 2 )
            SetParmVal( wing_id, "Tip_Chord", "XSec_1", 1 )
    
            Update()
    
    
        See also: WING_DRIVERS, XSEC_DRIVERS
        :param [in]: geom_id string Geom ID
        :param [in]: section_index Wing section index
        :param [in]: driver_0 First driver enum (i.e. SPAN_WSECT_DRIVER)
        :param [in]: driver_1 Second driver enum (i.e. ROOTC_WSECT_DRIVER)
        :param [in]: driver_2 Third driver enum (i.e. TIPC_WSECT_DRIVER)
        """
        return _vsp.SetDriverGroup(geom_id, section_index, driver_0, driver_1, driver_2)
    
    @client_wrap
    def GetXSecSurf(self, geom_id, index):
        r"""
        Get the XSecSurf ID for a particular Geom and XSecSurf index
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: index XSecSurf index
        :rtype: string
        :return: XSecSurf ID
        """
        return _vsp.GetXSecSurf(geom_id, index)
    
    @client_wrap
    def GetNumXSec(self, xsec_surf_id):
        r"""
        Get number of XSecs in an XSecSurf
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Flatten ends
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecTanAngles( xsec, XSEC_BOTH_SIDES, 0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Angles At Cross Section
    
                SetXSecTanStrengths( xsec, XSEC_BOTH_SIDES, 0.0, -1.0e12, -1.0e12, -1.0e12 )  # Set Tangent Strengths At Cross Section
    
    
        :param [in]: xsec_surf_id XSecSurf ID
        :rtype: int
        :return: Number of XSecs
        """
        return _vsp.GetNumXSec(xsec_surf_id)
    
    @client_wrap
    def GetXSec(self, xsec_surf_id, xsec_index):
        r"""
        Get Xsec ID for a particular XSecSurf at given index
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
    
        :param [in]: xsec_surf_id XSecSurf ID
        :param [in]: xsec_index Xsec index
        :rtype: string
        :return: Xsec ID
        """
        return _vsp.GetXSec(xsec_surf_id, xsec_index)
    
    @client_wrap
    def ChangeXSecShape(self, xsec_surf_id, xsec_index, type):
        r"""
        Change the shape of a particular XSec, identified by an XSecSurf ID and XSec index
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Set XSec 1 & 2 to Edit Curve type
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            if  GetXSecShape( xsec_2 ) != XS_EDIT_CURVE :
                print( "Error: ChangeXSecShape" )
    
    
        See also: XSEC_CRV_TYPE
        :param [in]: xsec_surf_id XSecSurf ID
        :param [in]: xsec_index Xsec index
        :param [in]: type Xsec type enum (i.e. XS_ELLIPSE)
        """
        return _vsp.ChangeXSecShape(xsec_surf_id, xsec_index, type)
    
    @client_wrap
    def SetXSecSurfGlobalXForm(self, xsec_surf_id, mat):
        r"""
        Set the global surface transform matrix for given XSecSurf
        :param [in]: xsec_surf_id XSecSurf ID
        :param [in]: mat Transformation matrix
        """
        return _vsp.SetXSecSurfGlobalXForm(xsec_surf_id, mat)
    
    @client_wrap
    def GetXSecSurfGlobalXForm(self, xsec_surf_id):
        r"""
        Get the global surface transform matrix for given XSecSurf
        :param [in]: xsec_surf_id XSecSurf ID
        :rtype: :py:class:`Matrix4d`
        :return: Transformation matrix
        """
        return _vsp.GetXSecSurfGlobalXForm(xsec_surf_id)
    
    @client_wrap
    def GetXSecShape(self, xsec_id):
        r"""
        Get the shape of an XSec
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            if  GetXSecShape( xsec ) != XS_EDIT_CURVE : print( "ERROR: GetXSecShape" )
    
    
        See also: XSEC_CRV_TYPE
        :param [in]: xsec_id XSec ID
        :rtype: int
        :return: XSec type enum (i.e. XS_ELLIPSE)
        """
        return _vsp.GetXSecShape(xsec_id)
    
    @client_wrap
    def GetXSecWidth(self, xsec_id):
        r"""
        Get the width of an XSec. Note that POINT type XSecs have a width and height of 0, regardless of what width and height it is set to.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 2 ) # Get 2nd to last XSec
    
            SetXSecWidthHeight( xsec, 3.0, 6.0 )
    
            if  abs( GetXSecWidth( xsec ) - 3.0 ) > 1e-6 : print( "---> Error: API Get/Set Width " )
    
    
        See also: SetXSecWidth
        :param [in]: xsec_id XSec ID
        :rtype: float
        :return: Xsec width
        """
        return _vsp.GetXSecWidth(xsec_id)
    
    @client_wrap
    def GetXSecHeight(self, xsec_id):
        r"""
        Get the height of an XSec. Note that POINT type XSecs have a width and height of 0, regardless of what width and height it is set to.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 2 ) # Get 2nd to last XSec
    
            SetXSecWidthHeight( xsec, 3.0, 6.0 )
    
            if  abs( GetXSecHeight( xsec ) - 6.0 ) > 1e-6 : print( "---> Error: API Get/Set Width " )
    
    
        See also: SetXSecHeight
        :param [in]: xsec_id XSec ID
        :rtype: float
        :return: Xsec height
        """
        return _vsp.GetXSecHeight(xsec_id)
    
    @client_wrap
    def SetXSecWidthHeight(self, xsec_id, w, h):
        r"""
        Set the width and height of an XSec. Note, if the XSec is an EDIT_CURVE type and PreserveARFlag is true, the input width value will be
        ignored and instead set from on the input height and aspect ratio. Use SetXSecWidth and SetXSecHeight directly to avoid this.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            SetXSecWidthHeight( xsec_2, 1.5, 1.5 )
    
    
        See also: SetXSecWidth, SetXSecHeight
        :param [in]: xsec_id XSec ID
        :param [in]: w Xsec width
        :param [in]: h Xsec height
        """
        return _vsp.SetXSecWidthHeight(xsec_id, w, h)
    
    @client_wrap
    def SetXSecWidth(self, xsec_id, w):
        r"""
        Set the width of an XSec. Note that POINT type XSecs have a width and height of 0, regardless of what is input to SetXSecWidth.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            SetXSecWidth( xsec_2, 1.5 )
    
    
        See also: GetXSecWidth
        :param [in]: xsec_id XSec ID
        :param [in]: w Xsec width
        """
        return _vsp.SetXSecWidth(xsec_id, w)
    
    @client_wrap
    def SetXSecHeight(self, xsec_id, h):
        r"""
        Set the height of an XSec. Note that POINT type XSecs have a width and height of 0, regardless of what is input to SetXSecHeight.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            SetXSecHeight( xsec_2, 1.5 )
    
    
        See also: GetXSecHeight
        :param [in]: xsec_id XSec ID
        :param [in]: h Xsec height
        """
        return _vsp.SetXSecHeight(xsec_id, h)
    
    @client_wrap
    def GetXSecParmIDs(self, xsec_id):
        r"""
        Get all Parm IDs for specified XSec Parm Container
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            parm_array = GetXSecParmIDs( xsec )
    
            if  len(parm_array) < 1 : print( "---> Error: API GetXSecParmIDs " )
    
    
        :param [in]: xsec_id XSec ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm IDs
        """
        return _vsp.GetXSecParmIDs(xsec_id)
    
    @client_wrap
    def GetXSecParm(self, xsec_id, name):
        r"""
        Get a specific Parm ID from an Xsec
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            if  not ValidParm( wid ) : print( "---> Error: API GetXSecParm " )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: name Parm name
        :rtype: string
        :return: Parm ID
        """
        return _vsp.GetXSecParm(xsec_id, name)
    
    @client_wrap
    def ReadFileXSec(self, xsec_id, file_name):
        r"""
        Read in XSec shape from fuselage (*.fsx) file and set to the specified XSec. The XSec must be of type XS_FILE_FUSE.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_FILE_FUSE )
    
            xsec = GetXSec( xsec_surf, 2 )
    
            vec_array = ReadFileXSec(xsec, "TestXSec.fxs")
    
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: file_name Fuselage XSec file name
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of coordinate points read from the file and set to the XSec
        """
        return _vsp.ReadFileXSec(xsec_id, file_name)
    
    @client_wrap
    def SetXSecPnts(self, xsec_id, pnt_vec):
        r"""
        Set the coordinate points for a specific XSec. The XSec must be of type XS_FILE_FUSE.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_FILE_FUSE )
    
            xsec = GetXSec( xsec_surf, 2 )
    
            vec_array = ReadFileXSec(xsec, "TestXSec.fxs")
    
    
            if  len(vec_array) > 0 :
                vec_array[1] = vec_array[1] * 2.0
                vec_array[3] = vec_array[3] * 2.0
    
                SetXSecPnts( xsec, vec_array )
    
    
        :param [in]: xsec_id string XSec ID
        :param [in]: pnt_vec vector<vec3d> Vector of XSec coordinate points
        """
        return _vsp.SetXSecPnts(xsec_id, pnt_vec)
    
    @client_wrap
    def ComputeXSecPnt(self, xsec_id, fract):
        r"""
        Compute 3D coordinate for a point on an XSec curve given the parameter value (U) along the curve
    
    
        .. code-block:: python
    
            #==== Add Geom ====//
            stack_id = AddGeom( "STACK" )
    
            #==== Get The XSec Surf ====//
            xsec_surf = GetXSecSurf( stack_id, 0 )
    
            xsec = GetXSec( xsec_surf, 2 )
    
            u_fract = 0.25
    
            pnt = ComputeXSecPnt(xsec, u_fract)
    
    
    
        :param [in]: xsec_id string XSec ID
        :param [in]: fract double Curve parameter value (range: 0 - 1)
        :rtype: :py:class:`vec3d`
        :return: vec3d 3D coordinate point
        """
        return _vsp.ComputeXSecPnt(xsec_id, fract)
    
    @client_wrap
    def ComputeXSecTan(self, xsec_id, fract):
        r"""
        Compute the tangent vector of a point on an XSec curve given the parameter value (U) along the curve
    
    
        .. code-block:: python
    
            #==== Add Geom ====//
            stack_id = AddGeom( "STACK" )
    
            #==== Get The XSec Surf ====//
            xsec_surf = GetXSecSurf( stack_id, 0 )
    
            xsec = GetXSec( xsec_surf, 2 )
    
            u_fract = 0.25
    
            tan = ComputeXSecTan( xsec, u_fract )
    
    
        :param [in]: xsec_id string XSec ID
        :param [in]: fract double Curve parameter value (range: 0 - 1)
        :rtype: :py:class:`vec3d`
        :return: vec3d Tangent vector
        """
        return _vsp.ComputeXSecTan(xsec_id, fract)
    
    @client_wrap
    def ResetXSecSkinParms(self, xsec_id):
        r"""
        Reset all skinning Parms for a specified XSec. Set top, bottom, left, and right strengths, slew, angle, and curvature to 0. Set all symmetry and equality conditions to false.
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf
    
            num_xsecs = GetNumXSec( xsec_surf )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            SetXSecTanAngles( xsec, XSEC_BOTH_SIDES, 0.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Angles At Cross Section
            SetXSecContinuity( xsec, 1 )                       # Set Continuity At Cross Section
    
            ResetXSecSkinParms( xsec )
    
    
        :param [in]: xsec_id string XSec ID
        """
        return _vsp.ResetXSecSkinParms(xsec_id)
    
    @client_wrap
    def SetXSecContinuity(self, xsec_id, cx):
        r"""
        Set C-type continuity enforcement for a particular XSec
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf
    
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecContinuity( xsec, 1 )                       # Set Continuity At Cross Section
    
    
        :param [in]: xsec_id string XSec ID
        :param [in]: cx int Continuity level (0, 1, or 2)
        """
        return _vsp.SetXSecContinuity(xsec_id, cx)
    
    @client_wrap
    def SetXSecTanAngles(self, xsec_id, side, top, right, bottom, left):
        r"""
        Set the tangent angles for the specified XSec
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecTanAngles( xsec, XSEC_BOTH_SIDES, 10.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Angles At Cross Section
    
    
        See also: XSEC_SIDES_TYPE
        :param [in]: xsec_id string XSec ID
        :param [in]: side int Side type enum (i.e. XSEC_BOTH_SIDES)
        :param [in]: top double Top angle (degrees)
        :param [in]: right double Right angle (degrees)
        :param [in]: bottom double Bottom angle (degrees)
        :param [in]: left double Left angle (degrees)
        """
        return _vsp.SetXSecTanAngles(xsec_id, side, top, right, bottom, left)
    
    @client_wrap
    def SetXSecTanSlews(self, xsec_id, side, top, right, bottom, left):
        r"""
        Set the tangent slew angles for the specified XSec
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecTanSlews( xsec, XSEC_BOTH_SIDES, 5.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Slews At Cross Section
    
    
        See also: XSEC_SIDES_TYPE
        :param [in]: xsec_id XSec ID
        :param [in]: side Side type enum (i.e. XSEC_BOTH_SIDES)
        :param [in]: top Top angle (degrees)
        :param [in]: right Right angle (degrees)
        :param [in]: bottom Bottom angle (degrees)
        :param [in]: left Left angle (degrees)
        """
        return _vsp.SetXSecTanSlews(xsec_id, side, top, right, bottom, left)
    
    @client_wrap
    def SetXSecTanStrengths(self, xsec_id, side, top, right, bottom, left):
        r"""
        Set the tangent strengths for the specified XSec
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Flatten ends
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecTanStrengths( xsec, XSEC_BOTH_SIDES, 0.8, -1.0e12, -1.0e12, -1.0e12 )  # Set Tangent Strengths At Cross Section
    
    
        See also: XSEC_SIDES_TYPE
        :param [in]: xsec_id XSec ID
        :param [in]: side Side type enum (i.e. XSEC_BOTH_SIDES)
        :param [in]: top Top strength
        :param [in]: right Right strength
        :param [in]: bottom Bottom strength
        :param [in]: left Left strength
        """
        return _vsp.SetXSecTanStrengths(xsec_id, side, top, right, bottom, left)
    
    @client_wrap
    def SetXSecCurvatures(self, xsec_id, side, top, right, bottom, left):
        r"""
        Set curvatures for the specified XSec
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            # Flatten ends
            num_xsecs = GetNumXSec( xsec_surf )
    
            for i in range(num_xsecs):
    
                xsec = GetXSec( xsec_surf, i )
    
                SetXSecCurvatures( xsec, XSEC_BOTH_SIDES, 0.2, -1.0e12, -1.0e12, -1.0e12 )  # Set Tangent Strengths At Cross Section
    
    
        See also: XSEC_SIDES_TYPE
        :param [in]: xsec_id XSec ID
        :param [in]: side Side type enum (i.e. XSEC_BOTH_SIDES)
        :param [in]: top Top curvature
        :param [in]: right Right curvature
        :param [in]: bottom Bottom curvature
        :param [in]: left Left curvature
        """
        return _vsp.SetXSecCurvatures(xsec_id, side, top, right, bottom, left)
    
    @client_wrap
    def ReadFileAirfoil(self, xsec_id, file_name):
        r"""
        Read in XSec shape from airfoil file and set to the specified XSec. The XSec must be of type XS_FILE_AIRFOIL. Airfoil files may be in Lednicer or Selig format with *.af or *.dat extensions.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: file_name Airfoil XSec file name
        """
        return _vsp.ReadFileAirfoil(xsec_id, file_name)
    
    @client_wrap
    def SetAirfoilUpperPnts(self, xsec_id, up_pnt_vec):
        r"""
        Set the upper points for an airfoil. The XSec must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
            up_array = GetAirfoilUpperPnts( xsec )
    
            for i in range(int( len(up_array) )):
    
                up_array[i].scale_y( 2.0 )
    
            SetAirfoilUpperPnts( xsec, up_array )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: up_pnt_vec Array of points defining the upper surface of the airfoil
        """
        return _vsp.SetAirfoilUpperPnts(xsec_id, up_pnt_vec)
    
    @client_wrap
    def SetAirfoilLowerPnts(self, xsec_id, low_pnt_vec):
        r"""
        Set the lower points for an airfoil. The XSec must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
            low_array = GetAirfoilLowerPnts( xsec )
    
            for i in range(int( len(low_array) )):
    
                low_array[i].scale_y( 0.5 )
    
            SetAirfoilUpperPnts( xsec, low_array )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: low_pnt_vec Array of points defining the lower surface of the airfoil
        """
        return _vsp.SetAirfoilLowerPnts(xsec_id, low_pnt_vec)
    
    @client_wrap
    def SetAirfoilPnts(self, xsec_id, up_pnt_vec, low_pnt_vec):
        r"""
        Set the upper and lower points for an airfoil. The XSec must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
            up_array = GetAirfoilUpperPnts( xsec )
    
            low_array = GetAirfoilLowerPnts( xsec )
    
            for i in range(int( len(up_array) )):
    
                up_array[i].scale_y( 2.0 )
    
                low_array[i].scale_y( 0.5 )
    
            SetAirfoilPnts( xsec, up_array, low_array )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: up_pnt_vec Array of points defining the upper surface of the airfoil
        :param [in]: low_pnt_vec Array of points defining the lower surface of the airfoil
        """
        return _vsp.SetAirfoilPnts(xsec_id, up_pnt_vec, low_pnt_vec)
    
    @client_wrap
    def GetHersheyBarLiftDist(self, npts, alpha, Vinf, span, full_span_flag=False):
        r"""
        Get the theoretical lift (Cl) distribution for a Hershey Bar wing with unit chord length using Glauert's Method. This function was initially created to compare VSPAERO results to Lifting Line Theory.
        If full_span_flag is set to true symmetry is applied to the results.
    
    
        .. code-block:: python
    
            pi = 3.14159265358979323846
            # Compute theoretical lift and drag distributions using 100 points
            Vinf = 100
    
            halfAR = 20
    
            alpha_deg = 10
    
            n_pts = 100
    
            cl_dist_theo = GetHersheyBarLiftDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )
    
            cd_dist_theo = GetHersheyBarDragDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )
    
    
        :param [in]: npts Number of points along the span to assess
        :param [in]: alpha Wing angle of attack (Radians)
        :param [in]: Vinf Freestream velocity
        :param [in]: span Hershey Bar full-span. Note, only half is used in the calculation
        :param [in]: full_span_flag Flag to apply symmetry to results
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Theoretical coefficient of lift distribution array (size = 2*npts if full_span_flag = true)
        """
        return _vsp.GetHersheyBarLiftDist(npts, alpha, Vinf, span, full_span_flag)
    
    @client_wrap
    def GetHersheyBarDragDist(self, npts, alpha, Vinf, span, full_span_flag=False):
        r"""
        Get the theoretical drag (Cd) distribution for a Hershey Bar wing with unit chord length using Glauert's Method. This function was initially created to compare VSPAERO results to Lifting Line Theory.
        If full_span_flag is set to true symmetry is applied to the results.
    
    
        .. code-block:: python
    
            pi = 3.14159265358979323846
            # Compute theoretical lift and drag distributions using 100 points
            Vinf = 100
    
            halfAR = 20
    
            alpha_deg = 10
    
            n_pts = 100
    
            cl_dist_theo = GetHersheyBarLiftDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )
    
            cd_dist_theo = GetHersheyBarDragDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )
    
    
        :param [in]: npts Number of points along the span to assess
        :param [in]: alpha Wing angle of attack (Radians)
        :param [in]: Vinf Freestream velocity
        :param [in]: span Hershey Bar full-span. Note, only half is used in the calculation
        :param [in]: full_span_flag Flag to apply symmetry to results (default: false)
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Theoretical coefficient of drag distribution array (size = 2*npts if full_span_flag = true)
        """
        return _vsp.GetHersheyBarDragDist(npts, alpha, Vinf, span, full_span_flag)
    
    @client_wrap
    def GetVKTAirfoilPnts(self, npts, alpha, epsilon, kappa, tau):
        r"""
        Get the 2D coordinates an input number of points along a Von K�rm�n-Trefftz airfoil of specified shape
    
    
        .. code-block:: python
    
            pi = 3.14159265358979323846
    
            npts = 122
    
            alpha = 0.0
    
            epsilon = 0.1
    
            kappa = 0.1
    
            tau = 10
    
            xyz_airfoil = GetVKTAirfoilPnts(npts, alpha, epsilon, kappa, tau*(pi/180) )
    
            cp_dist = GetVKTAirfoilCpDist( alpha, epsilon, kappa, tau*(pi/180), xyz_airfoil )
    
    
        :param [in]: npts Number of points along the airfoil to return
        :param [in]: alpha Airfoil angle of attack (Radians)
        :param [in]: epsilon Airfoil thickness
        :param [in]: kappa Airfoil camber
        :param [in]: tau Airfoil trailing edge angle (Radians)
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of points on the VKT airfoil (size = npts)
        """
        return _vsp.GetVKTAirfoilPnts(npts, alpha, epsilon, kappa, tau)
    
    @client_wrap
    def GetVKTAirfoilCpDist(self, alpha, epsilon, kappa, tau, xyz_data):
        r"""
        Get the pressure coefficient (Cp) along a Von Kármán-Trefftz airfoil of specified shape at specified points along the airfoil
    
    
        .. code-block:: python
    
            pi = 3.14159265358979323846
    
            npts = 122
    
            alpha = 0.0
    
            epsilon = 0.1
    
            kappa = 0.1
    
            tau = 10
    
            xyz_airfoil = GetVKTAirfoilPnts(npts, alpha, epsilon, kappa, tau*(pi/180) )
    
            cp_dist = GetVKTAirfoilCpDist( alpha, epsilon, kappa, tau*(pi/180), xyz_airfoil )
    
    
        See also: GetVKTAirfoilPnts
        :param [in]: alpha double Airfoil angle of attack (Radians)
        :param [in]: epsilon double Airfoil thickness
        :param [in]: kappa double Airfoil camber
        :param [in]: tau double Airfoil trailing edge angle (Radians)
        :param [in]: xyz_data vector<vec3d> Vector of points on the airfoil to evaluate
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of Cp values for each point in xydata
        """
        return _vsp.GetVKTAirfoilCpDist(alpha, epsilon, kappa, tau, xyz_data)
    
    @client_wrap
    def GetEllipsoidSurfPnts(self, center, abc_rad, u_npts=20, w_npts=20):
        r"""
        Generate the surface coordinate points for a ellipsoid at specified center of input radius along each axis.
        Based on the MATLAB function ellipsoid (https://in.mathworks.com/help/matlab/ref/ellipsoid.html).
        See also: GetVKTAirfoilPnts
        :param [in]: center 3D location of the ellipsoid center
        :param [in]: abc_rad Radius along the A (X), B (Y), and C (Z) axes
        :param [in]: u_npts Number of points in the U direction
        :param [in]: w_npts Number of points in the W direction
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of coordinates describing the ellipsoid surface
        """
        return _vsp.GetEllipsoidSurfPnts(center, abc_rad, u_npts, w_npts)
    
    @client_wrap
    def GetFeatureLinePnts(self, geom_id):
        r"""
        Get the points along the feature lines of a particular Geom
        :param [in]: geom_id string Geom ID
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of points along the Geom's feature lines
        """
        return _vsp.GetFeatureLinePnts(geom_id)
    
    @client_wrap
    def GetEllipsoidCpDist(self, surf_pnt_vec, abc_rad, V_inf):
        r"""
        Generate Analytical Solution for Potential Flow for specified ellipsoid shape at input surface points for input velocity vector.
        Based on Munk, M. M., 'Remarks on the Pressure Distribution over the Surface of an Ellipsoid, Moving Translationally Through a Perfect
        Fluid,' NACA TN-196, June 1924. Function initially created to compare VSPAERO results to theory.
    
    
        .. code-block:: python
    
            import math
            pi = 3.14159265358979323846
    
            npts = 101
    
            abc_rad = vec3d(1.0, 2.0, 3.0)
    
            alpha = 5 # deg
    
            beta = 5 # deg
    
            V_inf = 100.0
    
            x_slice_pnt_vec = [None]*npts
            theta_vec = [None]*npts
    
            theta_vec[0] = 0
    
            for i in range(1, npts):
                theta_vec[i] = theta_vec[i-1] + (2 * pi / (npts - 1))
    
    
            for i in range(npts):
    
                x_slice_pnt_vec[i] = vec3d( 0, abc_rad.y() * math.cos( theta_vec[i] ), abc_rad.z() * math.sin( theta_vec[i] ) )
    
            V_vec = vec3d( ( V_inf * math.cos( alpha*pi/180 ) * math.cos( beta*pi/180 ) ), ( V_inf * math.sin( beta*pi/180 ) ), ( V_inf * math.sin( alpha*pi/180 ) * math.cos( beta*pi/180 ) ) )
    
            cp_dist = GetEllipsoidCpDist( x_slice_pnt_vec, abc_rad, V_vec )
    
    
        See also: GetEllipsoidSurfPnts
        :param [in]: surf_pnt_vec vector<vec3d> Vector of points on the ellipsoid surface to assess
        :param [in]: abc_rad vec3d Radius along the A (X), B (Y), and C (Z) axes
        :param [in]: V_inf vec3d 3D components of freestream velocity
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of Cp results corresponding to each point in surf_pnt_arr
        """
        return _vsp.GetEllipsoidCpDist(surf_pnt_vec, abc_rad, V_inf)
    
    @client_wrap
    def IntegrateEllipsoidFlow(self, abc_rad, abc_index):
        r"""IntegrateEllipsoidFlow(vec3d abc_rad, int const & abc_index) -> double"""
        return _vsp.IntegrateEllipsoidFlow(abc_rad, abc_index)
    
    @client_wrap
    def GetAirfoilUpperPnts(self, xsec_id):
        r"""
        Get the coordinate points for the upper surface of an airfoil. The XSec must be of type XS_FILE_AIRFOIL
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
            up_array = GetAirfoilUpperPnts( xsec )
    
    
        See also: SetAirfoilPnts
        :param [in]: xsec_id string XSec ID
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> VectorArray of coordinate points for the upper airfoil surface
        """
        return _vsp.GetAirfoilUpperPnts(xsec_id)
    
    @client_wrap
    def GetAirfoilLowerPnts(self, xsec_id):
        r"""
        Get the coordinate points for the lower surface of an airfoil. The XSec must be of type XS_FILE_AIRFOIL
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )
    
            xsec = GetXSec( xsec_surf, 1 )
    
            ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )
    
            low_array = GetAirfoilLowerPnts( xsec )
    
    
        See also: SetAirfoilPnts
        :param [in]: xsec_id string XSec ID
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of coordinate points for the lower airfoil surface
        """
        return _vsp.GetAirfoilLowerPnts(xsec_id)
    
    @client_wrap
    def GetUpperCSTCoefs(self, xsec_id):
        r"""
        Get the CST coefficients for the upper surface of an airfoil. The XSec must be of type XS_CST_AIRFOIL
        See also: SetUpperCST
        :param [in]: xsec_id string XSec ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of CST coefficients for the upper airfoil surface
        """
        return _vsp.GetUpperCSTCoefs(xsec_id)
    
    @client_wrap
    def GetLowerCSTCoefs(self, xsec_id):
        r"""
        Get the CST coefficients for the lower surface of an airfoil. The XSec must be of type XS_CST_AIRFOIL
        See also: SetLowerCST
        :param [in]: xsec_id string XSec ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of CST coefficients for the lower airfoil surface
        """
        return _vsp.GetLowerCSTCoefs(xsec_id)
    
    @client_wrap
    def GetUpperCSTDegree(self, xsec_id):
        r"""
        Get the CST degree for the upper surface of an airfoil. The XSec must be of type XS_CST_AIRFOIL
        See also: SetUpperCST
        :param [in]: xsec_id string XSec ID
        :rtype: int
        :return: int CST Degree for upper airfoil surface
        """
        return _vsp.GetUpperCSTDegree(xsec_id)
    
    @client_wrap
    def GetLowerCSTDegree(self, xsec_id):
        r"""
        Get the CST degree for the lower surface of an airfoil. The XSec must be of type XS_CST_AIRFOIL
        See also: SetLowerCST
        :param [in]: xsec_id XSec ID
        :rtype: int
        :return: int CST Degree for lower airfoil surface
        """
        return _vsp.GetLowerCSTDegree(xsec_id)
    
    @client_wrap
    def SetUpperCST(self, xsec_id, deg, coefs):
        r"""
        Set the CST degree and coefficients for the upper surface of an airfoil. The number of coefficients should be one more than the CST degree. The XSec must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree, GetUpperCSTCoefs
        :param [in]: xsec_id string XSec ID
        :param [in]: deg int CST degree of upper airfoil surface
        :param [in]: coefs vector<double> Vector of CST coefficients for the upper airfoil surface
        """
        return _vsp.SetUpperCST(xsec_id, deg, coefs)
    
    @client_wrap
    def SetLowerCST(self, xsec_id, deg, coefs):
        r"""
        Set the CST degree and coefficients for the lower surface of an airfoil. The number of coefficients should be one more than the CST degree. The XSec must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree, GetLowerCSTCoefs
        :param [in]: xsec_id string XSec ID
        :param [in]: deg int CST degree of lower airfoil surface
        :param [in]: coefs vector<double> Vector of CST coefficients for the lower airfoil surface
        """
        return _vsp.SetLowerCST(xsec_id, deg, coefs)
    
    @client_wrap
    def PromoteCSTUpper(self, xsec_id):
        r"""
        Promote the CST for the upper airfoil surface. The XSec must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree
        :param [in]: xsec_id XSec ID
        """
        return _vsp.PromoteCSTUpper(xsec_id)
    
    @client_wrap
    def PromoteCSTLower(self, xsec_id):
        r"""
        Promote the CST for the lower airfoil surface. The XSec must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree
        :param [in]: xsec_id XSec ID
        """
        return _vsp.PromoteCSTLower(xsec_id)
    
    @client_wrap
    def DemoteCSTUpper(self, xsec_id):
        r"""
        Demote the CST for the upper airfoil surface. The XSec must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree
        :param [in]: xsec_id XSec ID
        """
        return _vsp.DemoteCSTUpper(xsec_id)
    
    @client_wrap
    def DemoteCSTLower(self, xsec_id):
        r"""
        Demote the CST for the lower airfoil surface. The XSec must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree
        :param [in]: xsec_id XSec ID
        """
        return _vsp.DemoteCSTLower(xsec_id)
    
    @client_wrap
    def FitAfCST(self, xsec_surf_id, xsec_index, deg):
        r"""
        Fit a CST airfoil for an existing airfoil of type XS_FOUR_SERIES, XS_SIX_SERIES, XS_FOUR_DIGIT_MOD, XS_FIVE_DIGIT, XS_FIVE_DIGIT_MOD, XS_ONE_SIX_SERIES, or XS_FILE_AIRFOIL.
        :param [in]: xsec_surf_id XsecSurf ID
        :param [in]: xsec_index XSec index
        :param [in]: deg CST degree
        """
        return _vsp.FitAfCST(xsec_surf_id, xsec_index, deg)
    
    @client_wrap
    def AddBackground3D(self, ):
        r"""
        Add a Background3D to model
    
    
        .. code-block:: python
    
            nbg = GetNumBackground3Ds()
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            if GetNumBackground3Ds() != nbg + 1 :
                print( "ERROR: AddBackground3D" )
    
            DelBackground3D( bg_id )
    
        :rtype: string
        :return: string ID for added Background3D
        """
        return _vsp.AddBackground3D()
    
    @client_wrap
    def GetNumBackground3Ds(self, ):
        r"""
        Get Number of Background3D's in a model
    
    
        .. code-block:: python
    
            nbg = GetNumBackground3Ds()
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            if GetNumBackground3Ds() != nbg + 1 :
                print( "ERROR: AddBackground3D" )
    
            DelBackground3D( bg_id )
    
        :rtype: int
        :return: int Number of Background3D's in model
        """
        return _vsp.GetNumBackground3Ds()
    
    @client_wrap
    def GetAllBackground3Ds(self, ):
        r"""
        Get id's of all Background3Ds in model
    
    
        .. code-block:: python
    
            nbg = GetNumBackground3Ds()
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            if GetNumBackground3Ds() != nbg + 3 :
                print( "ERROR: AddBackground3D" )
    
            bg_array = GetAllBackground3Ds()
    
            for n in range( len( bg_array ) ):
                print( bg_array[n] )
    
            DelAllBackground3Ds()
    
        :rtype: vector< string >
        :return: vector<string> Vector of Background3D IDs
        """
        return _vsp.GetAllBackground3Ds()
    
    @client_wrap
    def ShowAllBackground3Ds(self, ):
        r"""
        Show all Background3Ds in model
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            ShowAllBackground3Ds()
    
            DelAllBackground3Ds()
    
        """
        return _vsp.ShowAllBackground3Ds()
    
    @client_wrap
    def HideAllBackground3Ds(self, ):
        r"""
        Hide all Background3Ds in model
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            HideAllBackground3Ds()
    
            DelAllBackground3Ds()
    
        """
        return _vsp.HideAllBackground3Ds()
    
    @client_wrap
    def DelAllBackground3Ds(self, ):
        r"""
        Delete all Background3Ds in model
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            DelAllBackground3Ds()
    
            nbg = GetNumBackground3Ds()
    
            if nbg != 0 :
                print( "ERROR: DelAllBackground3Ds" )
    
    
        """
        return _vsp.DelAllBackground3Ds()
    
    @client_wrap
    def DelBackground3D(self, id):
        r"""
        Delete specific Background3D frommodel
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            bg_id = AddBackground3D()
            AddBackground3D()
    
            nbg = GetNumBackground3Ds()
    
            DelBackground3D( bg_id )
    
            if GetNumBackground3Ds() != nbg -1 :
                print( "ERROR: DelBackground3D" )
    
    
        :param [in]: id string Background3D ID to delete
        """
        return _vsp.DelBackground3D(id)
    
    @client_wrap
    def GetAllBackground3DRelativePaths(self, ):
        r"""
        Get relative paths to all Background3D images in model.  Note that path is relative to the model's *.vsp3 file.
        Consequently, if a file has not yet been saved or assigned a file name, the relative path is meaningless.
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            bg_file_array = GetAllBackground3DRelativePaths()
    
            for n in range( len( bg_file_array ) ):
                print( bg_file_array[n] )
    
            DelAllBackground3Ds()
    
        :rtype: vector< string >
        :return: vector<string> Vector of relative paths to Background3D image files
        """
        return _vsp.GetAllBackground3DRelativePaths()
    
    @client_wrap
    def GetAllBackground3DAbsolutePaths(self, ):
        r"""
        Get absolute paths to all Background3D images in model.
    
    
        .. code-block:: python
    
            # Add Background3D
            AddBackground3D()
            AddBackground3D()
            AddBackground3D()
    
            bg_file_array = GetAllBackground3DAbsolutePaths()
    
            for n in range( len( bg_file_array ) ):
                print( bg_file_array[n] )
    
            DelAllBackground3Ds()
    
        :rtype: vector< string >
        :return: vector<string> Vector of absolute paths to Background3D image files
        """
        return _vsp.GetAllBackground3DAbsolutePaths()
    
    @client_wrap
    def GetBackground3DRelativePath(self, id):
        r"""
        Get relative path to specified Background3D's image.  Note that path is relative to the model's *.vsp3 file.
        Consequently, if a file has not yet been saved or assigned a file name, the relative path is meaningless.
    
    
        .. code-block:: python
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            SetBackground3DRelativePath( bg_id, "front.png" )
            bg_file = GetBackground3DRelativePath( bg_id )
    
            print( bg_file )
    
            DelAllBackground3Ds()
    
        :param [in]: id string Background3D ID
        :rtype: string
        :return: string Relative path to Background3D image file
        """
        return _vsp.GetBackground3DRelativePath(id)
    
    @client_wrap
    def GetBackground3DAbsolutePath(self, id):
        r"""
        Get absolute path to specified Background3D's image.
    
    
        .. code-block:: python
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            SetBackground3DAbsolutePath( bg_id, "/user/me/vsp_work/front.png" )
            bg_file = GetBackground3DAbsolutePath( bg_id )
    
            print( bg_file )
    
            DelAllBackground3Ds()
    
        :param [in]: id string Background3D ID
        :rtype: string
        :return: string Absolute path to Background3D image file
        """
        return _vsp.GetBackground3DAbsolutePath(id)
    
    @client_wrap
    def SetBackground3DRelativePath(self, id, fname):
        r"""
        Set relative path to specified Background3D's image.  Note that path is relative to the model's *.vsp3 file.
        Consequently, if a file has not yet been saved or assigned a file name, the relative path is meaningless.
    
    
        .. code-block:: python
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            SetBackground3DRelativePath( bg_id, "front.png" )
            bg_file = GetBackground3DRelativePath( bg_id )
    
            print( bg_file )
    
            DelAllBackground3Ds()
    
        :param [in]: id string Background3D ID
        :param [in]: fname string Relative path to Background3D image file
        """
        return _vsp.SetBackground3DRelativePath(id, fname)
    
    @client_wrap
    def SetBackground3DAbsolutePath(self, id, fname):
        r"""
        Set absolute path to specified Background3D's image.
    
    
        .. code-block:: python
    
            # Add Background3D
            bg_id = AddBackground3D()
    
            SetBackground3DAbsolutePath( bg_id, "front.png" )
            bg_file = GetBackground3DAbsolutePath( bg_id )
    
            print( bg_file )
    
            DelAllBackground3Ds()
    
        :param [in]: id string Background3D ID
        :param [in]: fname string Absolute path to Background3D image file
        """
        return _vsp.SetBackground3DAbsolutePath(id, fname)
    
    @client_wrap
    def GetNumRoutingPts(self, routing_id):
        r"""
        Get the number of routing points in a RoutingGeom
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            npt = vsp.GetNumRoutingPts(routing_geom)
    
        See also: AddRoutingPt, DelRoutingPt
        :param [in]: routing_id string RoutingGeom Geom ID
        :rtype: int
        :return: int Number of routing points in specified RoutingGeom
        """
        return _vsp.GetNumRoutingPts(routing_id)
    
    @client_wrap
    def AddRoutingPt(self, routing_id, geom_id, surf_index):
        r"""
        Add a routing point to a RoutingGeom.  The new point will be the last point in the route.  The new point will be
        anchored to the specified geom and surface.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
        See also: AddRoutingPt, DelRoutingPt, InsertRoutingPt
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: geom_id string Geom ID of geom to anchor new routing point to
        :param [in]: surf_index int Index of surf to anchor new routing point to
        :rtype: string
        :return: string ParmContainer ID for the newly added routing point
        """
        return _vsp.AddRoutingPt(routing_id, geom_id, surf_index)
    
    @client_wrap
    def InsertRoutingPt(self, routing_id, index, geom_id, surf_index):
        r"""
        Add a routing point to a RoutingGeom.  The new point will be inserted before the specified index.  The new point
        will be anchored to the specified geom and surface.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            npt = vsp.GetNumRoutingPts(routing_geom)
            rptPre2 = vsp.InsertRoutingPt(routing_geom, 2, pod2, 0)
            uPre2 = vsp.GetParm( rptPre2, 'U', 'RoutePt')
            vsp.SetParmVal(uPre2, 0.)
    
        See also: AddRoutingPt, DelRoutingPt
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: index int Index of routing point to insert new point before
        :param [in]: geom_id string Geom ID of geom to anchor new routing point to
        :param [in]: surf_index int Index of surf to anchor new routing point to
        :rtype: string
        :return: string ParmContainer ID for the newly added routing point
        """
        return _vsp.InsertRoutingPt(routing_id, index, geom_id, surf_index)
    
    @client_wrap
    def DelRoutingPt(self, routing_id, index):
        r"""
        Delete a specified routing point from a RoutingGeom.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.DelRoutingPt( routing_geom, 1 )
    
        See also: AddRoutingPt, DelAllRoutingPt
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: index int Index of routing point to delete
        """
        return _vsp.DelRoutingPt(routing_id, index)
    
    @client_wrap
    def DelAllRoutingPt(self, routing_id):
        r"""
        Delete all routing points from a RoutingGeom.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.DelAllRoutingPt( routing_geom )
    
        See also: AddRoutingPt, DelRoutingPt
        :param [in]: routing_id string RoutingGeom Geom ID
        """
        return _vsp.DelAllRoutingPt(routing_id)
    
    @client_wrap
    def MoveRoutingPt(self, routing_id, index, reorder_type):
        r"""
        Move a specified routing point within the route of a RoutingGeom.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            newindx = vsp.MoveRoutingPt( routing_geom, 1, vsp.REORDER_MOVE_DOWN )
    
        See also: AddRoutingPt, DelRoutingPt, REORDER_TYPE
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: index int Index of routing point to move
        :param [in]: reorder_type int Enum specifying reordering type (i.e. REORDER_MOVE_UP, REORDER_MOVE_DOWN, REORDER_MOVE_TOP, REORDER_MOVE_BOTTOM)
        """
        return _vsp.MoveRoutingPt(routing_id, index, reorder_type)
    
    @client_wrap
    def GetRoutingPtID(self, routing_id, index):
        r"""
        Get the ParmContainer ID of a routing point within a RoutingGeom.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            rid = vsp.GetRoutingPtID(routing_geom, 2)
    
        See also: AddRoutingPt, DelAllRoutingPt, GetAllRoutingPtIds
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: index int Index of routing point to ID to retreive
        :rtype: string
        :return: string ParmContainer ID for the specified routing point
        """
        return _vsp.GetRoutingPtID(routing_id, index)
    
    @client_wrap
    def GetAllRoutingPtIds(self, routing_id):
        r"""
        Get the ParmContainer IDs of all the routing points within a RoutingGeom.  The vector will contain the IDs in order.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            rpts = vsp.GetAllRoutingPtIds(routing_geom)
    
        See also: AddRoutingPt, DelAllRoutingPt, GetRoutingPtId
        :param [in]: routing_id string RoutingGeom Geom ID
        :rtype: vector< string >
        :return: vector<string> Vector of routing point ParmConatiner IDs
        """
        return _vsp.GetAllRoutingPtIds(routing_id)
    
    @client_wrap
    def GetRoutingPtParentID(self, pt_id):
        r"""
        Get the Geom ID of the geom a routing point is anchored to.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            gid = vsp.GetRoutingPtParentID(rpt1)
    
        See also: AddRoutingPt, DelAllRoutingPt, GetAllRoutingPtIds
        :param [in]: pt_id string ParmContainer ID of desired routing point
        :rtype: string
        :return: string Geom ID for the geom the routing point is anchored to
        """
        return _vsp.GetRoutingPtParentID(pt_id)
    
    @client_wrap
    def SetRoutingPtParentID(self, pt_id, parent_id):
        r"""
        Set the Geom ID of the geom a routing point is anchored to.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.SetRoutingPtParentID(rpt1, pod1)
    
        See also: AddRoutingPt, DelAllRoutingPt, GetAllRoutingPtIds
        :param [in]: pt_id string ParmContainer ID of desired routing point
        :param [in]: parent_id string Geom ID for the geom to anchor the routing point to
        """
        return _vsp.SetRoutingPtParentID(pt_id, parent_id)
    
    @client_wrap
    def GetMainRoutingPtCoord(self, pt_id):
        r"""
        Get the main coordinate location a routing point.  The main location is the location of the base copy before
        symmetry has been applied.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.Update()
            p1 = vsp.GetMainRoutingPtCoord(rpt1)
    
        See also: AddRoutingPt, DelRoutingPt, GetRoutingPtCoord, GetAllRoutingPtCoords, GetRoutingCurve
        :param [in]: pt_id string ParmContainer ID of desired routing point
        :rtype: :py:class:`vec3d`
        :return: vec3d coordinate of main routing point
        """
        return _vsp.GetMainRoutingPtCoord(pt_id)
    
    @client_wrap
    def GetRoutingPtCoord(self, routing_id, index, symm_index):
        r"""
        Get the coordinate location a routing point in a RoutingGeom.  The main location is symm_index = 0.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.Update()
            p1 = vsp.GetRoutingPtCoord(rpt1, 1, 0)
    
        See also: AddRoutingPt, DelRoutingPt, GetMainRoutingPtCoord, GetAllRoutingPtCoords, GetRoutingCurve
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: index int Index of routing point to get cordinate of
        :param [in]: symm_index int Symmetry index to get coordinate of
        :rtype: :py:class:`vec3d`
        :return: vec3d coordinate of routing point
        """
        return _vsp.GetRoutingPtCoord(routing_id, index, symm_index)
    
    @client_wrap
    def GetAllRoutingPtCoords(self, routing_id, symm_index):
        r"""
        Get the coordinate locations along a RoutingGeom.  The main copy is symm_index = 0.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.Update()
            pvec = vsp.GetAllRoutingPtCoords(rpt1, 0)
    
        See also: AddRoutingPt, DelRoutingPt, GetMainRoutingPtCoord, GetRoutingPtCoord, GetRoutingCurve
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: symm_index int Symmetry index to get coordinate of
        :rtype: vector< vec3d >
        :return: vector < vec3d > coordinate of routing points along RoutingGeom
        """
        return _vsp.GetAllRoutingPtCoords(routing_id, symm_index)
    
    @client_wrap
    def GetRoutingCurve(self, routing_id, symm_index):
        r"""
        Get points along a RoutingGeom.  These points will follow the curve of a RoutingGeom with radiused
        routing points.  The main copy is symm_index = 0.
    
    
        .. code-block:: python
    
            pod1 = vsp.AddGeom('POD', '')
    
            pod2 = vsp.AddGeom('POD', '')
            ypod2 = vsp.GetParm(pod2, 'Y_Rel_Location', 'XForm')
            vsp.SetParmVal(ypod2, 2.0)
    
            routing_geom = vsp.AddGeom('ROUTING', '')
    
            rpt0 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u0 = vsp.GetParm( rpt0, 'U', 'RoutePt')
            vsp.SetParmVal(u0, 0.0)
    
            rpt1 = vsp.AddRoutingPt(routing_geom, pod2, 0)
    
            rpt2 = vsp.AddRoutingPt(routing_geom, pod1, 0)
            u2 = vsp.GetParm( rpt2, 'U', 'RoutePt')
            vsp.SetParmVal(u2, 1.0)
    
            vsp.Update()
            pvec = vsp.GetRoutingCurve(rpt1, 0)
    
        See also: AddRoutingPt, DelRoutingPt, GetMainRoutingPtCoord, GetRoutingPtCoord, GetAllRoutingPtCoords
        :param [in]: routing_id string RoutingGeom Geom ID
        :param [in]: symm_index int Symmetry index to get coordinate of
        :rtype: vector< vec3d >
        :return: vector < vec3d > coordinate of points along RoutingGeom curve
        """
        return _vsp.GetRoutingCurve(routing_id, symm_index)
    
    @client_wrap
    def ChangeBORXSecShape(self, bor_id, type):
        r"""
        Set the XSec type for a BOR component
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_ROUNDED_RECTANGLE )
    
            if  GetBORXSecShape( bor_id ) != XS_ROUNDED_RECTANGLE : print( "ERROR: ChangeBORXSecShape" )
    
    
        See also: XSEC_CRV_TYPE
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: type int XSec type enum (i.e. XS_ROUNDED_RECTANGLE)
        """
        return _vsp.ChangeBORXSecShape(bor_id, type)
    
    @client_wrap
    def GetBORXSecShape(self, bor_id):
        r"""
        Get the XSec type for a BOR component
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_ROUNDED_RECTANGLE )
    
            if  GetBORXSecShape( bor_id ) != XS_ROUNDED_RECTANGLE : print( "ERROR: GetBORXSecShape" )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: int
        :return: int XSec type enum (i.e. XS_ROUNDED_RECTANGLE)
        """
        return _vsp.GetBORXSecShape(bor_id)
    
    @client_wrap
    def ReadBORFileXSec(self, bor_id, file_name):
        r"""
        Set the coordinate points for a specific BOR. The BOR XSecCurve must be of type XS_FILE_FUSE.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_FUSE )
    
            vec_array = ReadBORFileXSec( bor_id, "TestXSec.fxs" )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: file_name string Fuselage XSec file name
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Array of coordinate points read from the file and set to the XSec
        """
        return _vsp.ReadBORFileXSec(bor_id, file_name)
    
    @client_wrap
    def SetBORXSecPnts(self, bor_id, pnt_vec):
        r"""
        Set the coordinate points for a specific BOR. The BOR XSecCurve must be of type XS_FILE_FUSE.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_FUSE )
    
            vec_array = ReadBORFileXSec( bor_id, "TestXSec.fxs" )
    
            if  len(vec_array) > 0 :
                vec_array[1] = vec_array[1] * 2.0
                vec_array[3] = vec_array[3] * 2.0
    
                SetBORXSecPnts( bor_id, vec_array )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: pnt_vec vector<vec3d> Vector of XSec coordinate points
        """
        return _vsp.SetBORXSecPnts(bor_id, pnt_vec)
    
    @client_wrap
    def ComputeBORXSecPnt(self, bor_id, fract):
        r"""
        Compute 3D coordinate for a point on a BOR XSecCurve given the parameter value (U) along the curve
    
    
        .. code-block:: python
    
            #==== Add Geom ====//
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            u_fract = 0.25
    
            pnt = ComputeBORXSecPnt( bor_id, u_fract )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: fract double Curve parameter value (range: 0 - 1)
        :rtype: :py:class:`vec3d`
        :return: vec3d Coordinate point on curve
        """
        return _vsp.ComputeBORXSecPnt(bor_id, fract)
    
    @client_wrap
    def ComputeBORXSecTan(self, bor_id, fract):
        r"""
        Compute the tangent vector of a point on a BOR XSecCurve given the parameter value (U) along the curve
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            u_fract = 0.25
    
            tan = ComputeBORXSecTan( bor_id, u_fract )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: fract double Curve parameter value (range: 0 - 1)
        :rtype: :py:class:`vec3d`
        :return: vec3d Tangent vector on curve
        """
        return _vsp.ComputeBORXSecTan(bor_id, fract)
    
    @client_wrap
    def ReadBORFileAirfoil(self, bor_id, file_name):
        r"""
        Read in shape from airfoil file and set to the specified BOR XSecCurve. The XSecCurve must be of type XS_FILE_AIRFOIL. Airfoil files may be in Lednicer or Selig format with *.af or *.dat extensions.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: file_name string Airfoil XSec file name
        """
        return _vsp.ReadBORFileAirfoil(bor_id, file_name)
    
    @client_wrap
    def SetBORAirfoilUpperPnts(self, bor_id, up_pnt_vec):
        r"""
        Set the upper points for an airfoil on a BOR. The BOR XSecCurve must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
            up_array = GetBORAirfoilUpperPnts( bor_id )
    
            for i in range(int( len(up_array) )):
    
                up_array[i].scale_y( 2.0 )
    
            SetBORAirfoilUpperPnts( bor_id, up_array )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: up_pnt_vec vector<vec3d> Vector of points defining the upper surface of the airfoil
        """
        return _vsp.SetBORAirfoilUpperPnts(bor_id, up_pnt_vec)
    
    @client_wrap
    def SetBORAirfoilLowerPnts(self, bor_id, low_pnt_vec):
        r"""
        Set the lower points for an airfoil on a BOR. The BOR XSecCurve must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
            low_array = GetBORAirfoilLowerPnts( bor_id )
    
            for i in range(int( len(low_array) )):
    
                low_array[i].scale_y( 0.5 )
    
            SetBORAirfoilLowerPnts( bor_id, low_array )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: low_pnt_vec vector<vec3d> Vector of points defining the lower surface of the airfoil
        """
        return _vsp.SetBORAirfoilLowerPnts(bor_id, low_pnt_vec)
    
    @client_wrap
    def SetBORAirfoilPnts(self, bor_id, up_pnt_vec, low_pnt_vec):
        r"""
        Set the upper and lower points for an airfoil on a BOR. The BOR XSecCurve must be of type XS_FILE_AIRFOIL.
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
            up_array = GetBORAirfoilUpperPnts( bor_id )
    
            low_array = GetBORAirfoilLowerPnts( bor_id )
    
            for i in range(int( len(up_array) )):
    
                up_array[i].scale_y( 2.0 )
    
                low_array[i].scale_y( 0.5 )
    
            SetBORAirfoilPnts( bor_id, up_array, low_array )
    
    
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: up_pnt_vec vector<vec3d> Vector of points defining the upper surface of the airfoil
        :param [in]: low_pnt_vec vector<_>vec3d> Vector of points defining the lower surface of the airfoil
        """
        return _vsp.SetBORAirfoilPnts(bor_id, up_pnt_vec, low_pnt_vec)
    
    @client_wrap
    def GetBORAirfoilUpperPnts(self, bor_id):
        r"""
        Get the coordinate points for the upper surface of an airfoil on a BOR. The BOR XSecCurve must be of type XS_FILE_AIRFOIL
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
            up_array = GetBORAirfoilUpperPnts( bor_id )
    
    
        See also: SetAirfoilPnts
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of coordinate points for the upper airfoil surface
        """
        return _vsp.GetBORAirfoilUpperPnts(bor_id)
    
    @client_wrap
    def GetBORAirfoilLowerPnts(self, bor_id):
        r"""
        Get the coordinate points for the lower surface of an airfoil of a BOR. The XSecCurve must be of type XS_FILE_AIRFOIL
    
    
        .. code-block:: python
    
            # Add Body of Recolution
            bor_id = AddGeom( "BODYOFREVOLUTION", "" )
    
            ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )
    
            ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )
    
            low_array = GetBORAirfoilLowerPnts( bor_id )
    
    
        See also: SetAirfoilPnts
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of coordinate points for the lower airfoil surface
        """
        return _vsp.GetBORAirfoilLowerPnts(bor_id)
    
    @client_wrap
    def GetBORUpperCSTCoefs(self, bor_id):
        r"""
        Get the CST coefficients for the upper surface of an airfoil of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: SetUpperCST
        :param [in]: bor_id Body of revolution Geom ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of CST coefficients for the upper airfoil surface
        """
        return _vsp.GetBORUpperCSTCoefs(bor_id)
    
    @client_wrap
    def GetBORLowerCSTCoefs(self, bor_id):
        r"""
        Get the CST coefficients for the lower surface of an airfoil of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: SetLowerCST
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: vector<double> Vector of CST coefficients for the lower airfoil surface
        """
        return _vsp.GetBORLowerCSTCoefs(bor_id)
    
    @client_wrap
    def GetBORUpperCSTDegree(self, bor_id):
        r"""
        Get the CST degree for the upper surface of an airfoil of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: SetUpperCST
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: int
        :return: int CST Degree for upper airfoil surface
        """
        return _vsp.GetBORUpperCSTDegree(bor_id)
    
    @client_wrap
    def GetBORLowerCSTDegree(self, bor_id):
        r"""
        Get the CST degree for the lower surface of an airfoil of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: SetLowerCST
        :param [in]: bor_id string Body of revolution Geom ID
        :rtype: int
        :return: int CST Degree for lower airfoil surface
        """
        return _vsp.GetBORLowerCSTDegree(bor_id)
    
    @client_wrap
    def SetBORUpperCST(self, bor_id, deg, coefs):
        r"""
        Set the CST degree and coefficients for the upper surface of an airfoil of a BOR. The number of coefficients should be one more than the CST degree. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree, GetUpperCSTCoefs
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: deg CST degree of upper airfoil surface
        :param [in]: coefs Array of CST coefficients for the upper airfoil surface
        """
        return _vsp.SetBORUpperCST(bor_id, deg, coefs)
    
    @client_wrap
    def SetBORLowerCST(self, bor_id, deg, coefs):
        r"""
        Set the CST degree and coefficients for the lower surface of an airfoil of a BOR. The number of coefficients should be one more than the CST degree. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree, GetLowerCSTCoefs
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: deg int CST degree of lower airfoil surface
        :param [in]: coefs vector<double> Vector of CST coefficients for the lower airfoil surface
        """
        return _vsp.SetBORLowerCST(bor_id, deg, coefs)
    
    @client_wrap
    def PromoteBORCSTUpper(self, bor_id):
        r"""
        Promote the CST for the upper airfoil surface of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree
        :param [in]: bor_id string Body of revolution Geom ID
        """
        return _vsp.PromoteBORCSTUpper(bor_id)
    
    @client_wrap
    def PromoteBORCSTLower(self, bor_id):
        r"""
        Promote the CST for the lower airfoil surface of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree
        :param [in]: bor_id string Body of revolution Geom ID
        """
        return _vsp.PromoteBORCSTLower(bor_id)
    
    @client_wrap
    def DemoteBORCSTUpper(self, bor_id):
        r"""
        Demote the CST for the upper airfoil surface of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetUpperCSTDegree
        :param [in]: bor_id string Body of revolution Geom ID
        """
        return _vsp.DemoteBORCSTUpper(bor_id)
    
    @client_wrap
    def DemoteBORCSTLower(self, bor_id):
        r"""
        Demote the CST for the lower airfoil surface of a BOR. The XSecCurve must be of type XS_CST_AIRFOIL
        See also: GetLowerCSTDegree
        :param [in]: bor_id string Body of revolution Geom ID
        """
        return _vsp.DemoteBORCSTLower(bor_id)
    
    @client_wrap
    def FitBORAfCST(self, bor_id, deg):
        r"""
        Fit a CST airfoil for an existing airfoil of a BOR of type XS_FOUR_SERIES, XS_SIX_SERIES, XS_FOUR_DIGIT_MOD, XS_FIVE_DIGIT, XS_FIVE_DIGIT_MOD, XS_ONE_SIX_SERIES, or XS_FILE_AIRFOIL.
        :param [in]: bor_id string Body of revolution Geom ID
        :param [in]: deg int CST degree
        """
        return _vsp.FitBORAfCST(bor_id, deg)
    
    @client_wrap
    def WriteBezierAirfoil(self, file_name, geom_id, foilsurf_u):
        r"""
        Write out the untwisted unit-length 2D Bezier curve for the specified airfoil in custom *.bz format. The output will describe the analytical shape of the airfoil. See BezierAirfoilExample.m and BezierCtrlToCoordPnts.m for examples of
        discretizing the Bezier curve and generating a Selig airfoil file.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry and Set Parms ====//
            wing_id = AddGeom( "WING", "" )
    
            u = 0.5 # export airfoil at mid span location
    
            #==== Write Bezier Airfoil File ====//
            WriteBezierAirfoil( "Example_Bezier.bz", wing_id, u )
    
    
        :param [in]: file_name Airfoil (*.bz) output file name
        :param [in]: geom_id string Geom ID
        :param [in]: foilsurf_u U location (range: 0 - 1) along the surface. The foil surface does not include root and tip caps (i.e. 2 section wing -> XSec0 @ u=0, XSec1 @ u=0.5, XSec2 @ u=1.0)
        """
        return _vsp.WriteBezierAirfoil(file_name, geom_id, foilsurf_u)
    
    @client_wrap
    def WriteSeligAirfoil(self, file_name, geom_id, foilsurf_u):
        r"""
        Write out the untwisted unit-length 2D coordinate points for the specified airfoil in Selig format. Coordinate points follow the on-screen wire frame W tessellation.
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry and Set Parms ====//
            wing_id = AddGeom( "WING", "" )
    
            u = 0.5 # export airfoil at mid span location
    
            #==== Write Selig Airfoil File ====//
            WriteSeligAirfoil( "Example_Selig.dat", wing_id, u )
    
    
        See also: GetAirfoilCoordinates
        :param [in]: file_name Airfoil (*.dat) output file name
        :param [in]: geom_id string Geom ID
        :param [in]: foilsurf_u U location (range: 0 - 1) along the surface. The foil surface does not include root and tip caps (i.e. 2 section wing -> XSec0 @ u=0, XSec1 @ u=0.5, XSec2 @ u=1.0)
        """
        return _vsp.WriteSeligAirfoil(file_name, geom_id, foilsurf_u)
    
    @client_wrap
    def GetAirfoilCoordinates(self, geom_id, foilsurf_u):
        r"""
        Get the untwisted unit-length 2D coordinate points for the specified airfoil
        See also: WriteSeligAirfoil
        :param [in]: geom_id string Geom ID
        :param [in]: foilsurf_u U location (range: 0 - 1) along the surface. The foil surface does not include root and tip caps (i.e. 2 section wing -> XSec0 @ u=0, XSec1 @ u=0.5, XSec2 @ u=1.0)
        """
        return _vsp.GetAirfoilCoordinates(geom_id, foilsurf_u)
    
    @client_wrap
    def EditXSecInitShape(self, xsec_id):
        r"""
        Initialize the EditCurveXSec to the current value of m_ShapeType (i.e. EDIT_XSEC_ELLIPSE)
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            # Set XSec 2 to linear
            EditXSecConvertTo( xsec_2, LINEAR )
    
            EditXSecInitShape( xsec_2 ) # Change back to default ellipse
    
    
        See also: INIT_EDIT_XSEC_TYPE
        :param [in]: xsec_id XSec ID
        """
        return _vsp.EditXSecInitShape(xsec_id)
    
    @client_wrap
    def EditXSecConvertTo(self, xsec_id, newtype):
        r"""
        Convert the EditCurveXSec curve type to the specified new type. Note, EditCurveXSec uses the same enumerations for PCurve to identify curve type,
        but APPROX_CEDIT is not supported at this time.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Set XSec 1 to Linear
            EditXSecConvertTo( xsec_1, LINEAR )
    
    
        See also: PCURV_TYPE
        :param [in]: xsec_id XSec ID
        :param [in]: newtype New curve type enum (i.e. CEDIT)
        """
        return _vsp.EditXSecConvertTo(xsec_id, newtype)
    
    @client_wrap
    def GetEditXSecUVec(self, xsec_id):
        r"""
        Get the U parameter vector for an EditCurveXSec. The vector will be in increasing order with a range of 0 - 1.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            # Set XSec 2 to linear
            EditXSecConvertTo( xsec_2, LINEAR )
    
            u_vec = GetEditXSecUVec( xsec_2 )
    
            if  u_vec[1] - 0.25 > 1e-6 :
                print( "Error: GetEditXSecUVec" )
    
    
        :param [in]: xsec_id XSec ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: Array of U parameter values
        """
        return _vsp.GetEditXSecUVec(xsec_id)
    
    @client_wrap
    def GetEditXSecCtrlVec(self, xsec_id, non_dimensional=True):
        r"""
        Get the control point vector for an EditCurveXSec. Note, the returned array of vec3d values will be represented in 2D with Z set to 0.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Get the control points for the default shape
            xsec1_pts = GetEditXSecCtrlVec( xsec_1, True ) # The returned control points will not be scaled by width and height
    
            print( f"Normalized Bottom Point of XSecCurve: {xsec1_pts[3].x()}, {xsec1_pts[3].y()}, {xsec1_pts[3].z()}" )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: non_dimensional True to get the points non-dimensionalized, False to get them scaled by m_Width and m_Height
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: Array of control points
        """
        return _vsp.GetEditXSecCtrlVec(xsec_id, non_dimensional)
    
    @client_wrap
    def SetEditXSecPnts(self, xsec_id, u_vec, control_pts, r_vec):
        r"""
        Set the U parameter vector and the control point vector for an EditCurveXSec. The arrays must be of equal length, with the values for U defined in
        increasing order and range 0 - 1. The input control points to SetEditXSecPnts must be nondimensionalized in the approximate range of [-0.5, 0.5].
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            # Set XSec 2 to linear
            EditXSecConvertTo( xsec_2, LINEAR )
    
            # Turn off R/L symmetry
            SetParmVal( GetXSecParm( xsec_2, "SymType"), SYM_NONE )
    
            # Define a square
            xsec2_pts = [vec3d(0.5, 0.5, 0.0),
                     vec3d(0.5, -0.5, 0.0),
                     vec3d(-0.5, -0.5, 0.0),
                     vec3d(-0.5, 0.5, 0.0),
                     vec3d(0.5, 0.5, 0.0)]
    
            # u vec must start at 0.0 and end at 1.0
            u_vec = [0.0, 0.25, 0.5, 0.75, 1.0]
    
            r_vec = [0.0, 0.0, 0.0, 0.0, 0.0]
    
            SetEditXSecPnts( xsec_2, u_vec, xsec2_pts, r_vec ) # Note: points are unscaled by the width and height parms
    
            new_pnts = GetEditXSecCtrlVec( xsec_2, True ) # The returned control points will not be scaled by width and height
    
            if  dist( new_pnts[3], xsec2_pts[3] ) > 1e-6 :
                print( "Error: SetEditXSecPnts")
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: u_vec Array of U parameter values
        :param [in]: r_vec Array of R parameter values
        :param [in]: control_pts Nondimensionalized array of control points
        """
        return _vsp.SetEditXSecPnts(xsec_id, u_vec, control_pts, r_vec)
    
    @client_wrap
    def EditXSecDelPnt(self, xsec_id, indx):
        r"""
        Delete an EditCurveXSec control point. Note, cubic Bezier intermediate control points (those not on the curve) cannot be deleted.
        The previous and next Bezier control point will be deleted along with the point on the curve. Regardless of curve type, the first
        and last points may not be deleted.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            # Turn off R/L symmetry
            SetParmVal( GetXSecParm( xsec_2, "SymType"), SYM_NONE )
    
            old_pnts = GetEditXSecCtrlVec( xsec_2, True ) # The returned control points will not be scaled by width and height
    
            EditXSecDelPnt( xsec_2, 3 ) # Remove control point at bottom of circle
    
            new_pnts = GetEditXSecCtrlVec( xsec_2, True ) # The returned control points will not be scaled by width and height
    
            if  len(old_pnts) - len(new_pnts) != 3  :
                print( "Error: EditXSecDelPnt")
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: indx Control point index
        """
        return _vsp.EditXSecDelPnt(xsec_id, indx)
    
    @client_wrap
    def EditXSecSplit01(self, xsec_id, u):
        r"""
        Split the EditCurveXSec at the specified U value
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 2, XS_EDIT_CURVE )
    
            # Identify XSec 2
            xsec_2 = GetXSec( xsec_surf, 2 )
    
            # Turn off R/L symmetry
            SetParmVal( GetXSecParm( xsec_2, "SymType"), SYM_NONE )
    
            old_pnts = GetEditXSecCtrlVec( xsec_2, True ) # The returned control points will not be scaled by width and height
    
            new_pnt_ind = EditXSecSplit01( xsec_2, 0.375 )
    
            new_pnts = GetEditXSecCtrlVec( xsec_2, True ) # The returned control points will not be scaled by width and height
    
            if  len(new_pnts) - len(old_pnts) != 3  :
                print( "Error: EditXSecSplit01")
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: u U value to split the curve at (0 - 1)
        :rtype: int
        :return: Index of the point added from the split
        """
        return _vsp.EditXSecSplit01(xsec_id, u)
    
    @client_wrap
    def MoveEditXSecPnt(self, xsec_id, indx, new_pnt):
        r"""
        Move an EditCurveXSec control point. The XSec points are nondimensionalized by m_Width and m_Height and
        defined in 2D, so the Z value of the new coordinate point will be ignored.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Turn off R/L symmetry
            SetParmVal( GetXSecParm( xsec_1, "SymType"), SYM_NONE )
    
            # Get the control points for the default shape
            xsec1_pts = GetEditXSecCtrlVec( xsec_1, True ) # The returned control points will not be scaled by width and height
    
            # Identify a control point that lies on the curve and shift it in Y
            move_pnt_ind = 3
    
            new_pnt = vec3d( xsec1_pts[move_pnt_ind].x(), 2 * xsec1_pts[move_pnt_ind].y(), 0.0 )
    
            # Move the control point
            MoveEditXSecPnt( xsec_1, move_pnt_ind, new_pnt )
    
            new_pnts = GetEditXSecCtrlVec( xsec_1, True ) # The returned control points will not be scaled by width and height
    
            if  dist( new_pnt, new_pnts[move_pnt_ind] ) > 1e-6 :
                print( "Error: MoveEditXSecPnt" )
    
    
        :param [in]: xsec_id XSec ID
        :param [in]: indx Control point index
        :param [in]: new_pnt Coordinate of the new point
        """
        return _vsp.MoveEditXSecPnt(xsec_id, indx, new_pnt)
    
    @client_wrap
    def ConvertXSecToEdit(self, geom_id, indx=0):
        r"""
        Convert any XSec type into an EditCurveXSec. This function will work for BOR Geoms, in which case the input XSec index is ignored.
    
    
        .. code-block:: python
    
            # Add Stack
            sid = AddGeom( "STACK", "" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( sid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_ROUNDED_RECTANGLE )
    
            # Convert Rounded Rectangle to Edit Curve type XSec
            ConvertXSecToEdit( sid, 1 )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            # Get the control points for the default shape
            xsec1_pts = GetEditXSecCtrlVec( xsec_1, True ) # The returned control points will not be scaled by width and height
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: indx XSec index
        """
        return _vsp.ConvertXSecToEdit(geom_id, indx)
    
    @client_wrap
    def GetEditXSecFixedUVec(self, xsec_id):
        r"""
        Get the vector of fixed U flags for each control point in an EditCurveXSec. The fixed U flag is used to hold the
        U parameter of the control point constant when performing an equal arc length reparameterization of the curve.
    
    
        .. code-block:: python
    
            # Add Wing
            wid = AddGeom( "WING" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( wid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            fixed_u_vec = list(GetEditXSecFixedUVec( xsec_1 ))
    
            fixed_u_vec[3] = True # change a flag
    
            SetEditXSecFixedUVec( xsec_1, fixed_u_vec )
    
            ReparameterizeEditXSec( xsec_1 )
    
    
        See also: SetEditXSecFixedUVec, ReparameterizeEditXSec
        :param [in]: xsec_id XSec ID
        :rtype: std::vector< bool,std::allocator< bool > >
        :return: Array of bool values for each control point
        """
        return _vsp.GetEditXSecFixedUVec(xsec_id)
    
    @client_wrap
    def SetEditXSecFixedUVec(self, xsec_id, fixed_u_vec):
        r"""
        Set the vector of fixed U flags for each control point in an EditCurveXSec. The fixed U flag is used to hold the
        U parameter of the control point constant when performing an equal arc length reparameterization of the curve.
    
    
        .. code-block:: python
    
            # Add Wing
            wid = AddGeom( "WING" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( wid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            fixed_u_vec = list(GetEditXSecFixedUVec( xsec_1 ))
    
            fixed_u_vec[3] = True # change a flag
    
            SetEditXSecFixedUVec( xsec_1, fixed_u_vec )
    
            ReparameterizeEditXSec( xsec_1 )
    
    
        See also: GetEditXSecFixedUVec, ReparameterizeEditXSec
        :param [in]: xsec_id XSec ID
        :param [in]: fixed_u_vec Array of fixed U flags
        """
        return _vsp.SetEditXSecFixedUVec(xsec_id, fixed_u_vec)
    
    @client_wrap
    def ReparameterizeEditXSec(self, xsec_id):
        r"""
        Perform an equal arc length repareterization on an EditCurveXSec. The reparameterization is performed between
        specific U values if the Fixed U flag is true. This allows corners, such as at 0.25, 0.5, and 0.75 U, to be held
        constant while everything between them is reparameterized.
    
    
        .. code-block:: python
    
            # Add Wing
            wid = AddGeom( "WING" )
    
            # Get First (and Only) XSec Surf
            xsec_surf = GetXSecSurf( wid, 0 )
    
            ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )
    
            # Identify XSec 1
            xsec_1 = GetXSec( xsec_surf, 1 )
    
            fixed_u_vec = list(GetEditXSecFixedUVec( xsec_1 ))
    
            fixed_u_vec[3] = True # change a flag
    
            SetEditXSecFixedUVec( xsec_1, fixed_u_vec )
    
            ReparameterizeEditXSec( xsec_1 )
    
    
        See also: SetEditXSecFixedUVec, GetEditXSecFixedUVec
        :param [in]: xsec_id XSec ID
        """
        return _vsp.ReparameterizeEditXSec(xsec_id)
    
    @client_wrap
    def GetNumSets(self, ):
        r"""
        Get the total number of defined sets. Named sets are used to group components and read/write on them. The number of named
        sets will be 10 for OpenVSP versions up to 3.17.1 and 20 for later versions.
    
    
        .. code-block:: python
    
            if  GetNumSets() <= 0 : print( "---> Error: API GetNumSets " )
    
    
        :rtype: int
        :return: Number of sets
        """
        return _vsp.GetNumSets()
    
    @client_wrap
    def SetSetName(self, index, name):
        r"""
        Set the name of a set at specified index
    
    
        .. code-block:: python
    
            SetSetName( 3, "SetFromScript" )
    
            if GetSetName(3) != "SetFromScript":
                print("---> Error: API Get/Set Set Name")
    
    
    
        See also: SET_TYPE
        :param [in]: index Set index
        :param [in]: name Set name
        """
        return _vsp.SetSetName(index, name)
    
    @client_wrap
    def GetSetName(self, index):
        r"""
        Get the name of a set at specified index
    
    
        .. code-block:: python
    
            SetSetName( 3, "SetFromScript" )
    
            if GetSetName(3) != "SetFromScript":
                print("---> Error: API Get/Set Set Name")
    
    
        See also: SET_TYPE
        :param [in]: index Set index
        :rtype: string
        :return: Set name
        """
        return _vsp.GetSetName(index)
    
    @client_wrap
    def GetGeomSetAtIndex(self, index):
        r"""
        Get an array of Geom IDs for the specified set index
    
    
        .. code-block:: python
    
            SetSetName( 3, "SetFromScript" )
    
            geom_arr1 = GetGeomSetAtIndex( 3 )
    
            geom_arr2 = GetGeomSet( "SetFromScript" )
    
            if  len(geom_arr1) != len(geom_arr2) : print( "---> Error: API GetGeomSet " )
    
    
        See also: SET_TYPE
        :param [in]: index Set index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Geom IDs
        """
        return _vsp.GetGeomSetAtIndex(index)
    
    @client_wrap
    def GetGeomSet(self, name):
        r"""
        Get an array of Geom IDs for the specified set name
    
    
        .. code-block:: python
    
            SetSetName( 3, "SetFromScript" )
    
            geom_arr1 = GetGeomSetAtIndex( 3 )
    
            geom_arr2 = GetGeomSet( "SetFromScript" )
    
            if  len(geom_arr1) != len(geom_arr2) : print( "---> Error: API GetGeomSet " )
    
    
        :param [in]: name const string set name
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: array<string> array of Geom IDs
        """
        return _vsp.GetGeomSet(name)
    
    @client_wrap
    def GetSetIndex(self, name):
        r"""
        Get the set index for the specified set name
    
    
        .. code-block:: python
    
            SetSetName( 3, "SetFromScript" )
    
            if GetSetIndex("SetFromScript") != 3:
                print("ERROR: GetSetIndex")
    
    
    
        :param [in]: name Set name
        :rtype: int
        :return: Set index
        """
        return _vsp.GetSetIndex(name)
    
    @client_wrap
    def GetSetFlag(self, geom_id, set_index):
        r"""
        Check if a Geom is in the set at the specified set index
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            SetSetFlag( fuseid, 3, True )
    
            if not GetSetFlag(fuseid, 3):
                print("---> Error: API Set/Get Set Flag")
    
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: set_index Set index
        :rtype: boolean
        :return: True if geom is in the set, false otherwise
        """
        return _vsp.GetSetFlag(geom_id, set_index)
    
    @client_wrap
    def SetSetFlag(self, geom_id, set_index, flag):
        r"""
        Set whether or not a Geom is a member of the set at specified set index
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            SetSetFlag( fuseid, 3, True )
    
            if not GetSetFlag(fuseid, 3):
                print("---> Error: API Set/Get Set Flag")
    
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: set_index Set index
        :param [in]: flag Flag that indicates set membership
        """
        return _vsp.SetSetFlag(geom_id, set_index, flag)
    
    @client_wrap
    def CopyPasteSet(self, copyIndex, pasteIndex):
        r"""
        Copies all the states of a geom set and pastes them into a specific set based on passed in indexs
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            #set fuseid's state for set 3 to true
            SetSetFlag( fuseid, 3, True )
    
            #Copy set 3 and Paste into set 4
            CopyPasteSet( 3, 4 )
    
            #get fuseid's state for set 4
            flag_value = GetSetFlag( fuseid, 4 )
    
            if  flag_value != True: print( "---> Error: API CopyPasteSet " )
    
    
        :param [in]: copyIndex Copy Index
        :param [in]: pasteIndex Paste Index
        """
        return _vsp.CopyPasteSet(copyIndex, pasteIndex)
    
    @client_wrap
    def GetBBoxSet(self, set):
        r"""
        Get the corners of the bounding box of the specified Set.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            Update()
    
            sethasmembers, xmin, ymin, zmin, xlen, ylen, zlen = GetBBoxSet( SET_ALL )
    
        :param [in]: set int Desired Set
        :param [out]: xmin_out double Minimum bounding box X coordinate
        :param [out]: ymin_out double Minimum bounding box Y coordinate
        :param [out]: zmin_out double Minimum bounding box Z coordinate
        :param [out]: xlen_out double Maximum bounding box X length
        :param [out]: ylen_out double Maximum bounding box Y length
        :param [out]: zlen_out double Maximum bounding box Z length
        :rtype: boolean
        :return: bool Flag indicating whether the set has members (is non-empty)
        """
        return _vsp.GetBBoxSet(set)
    
    @client_wrap
    def GetScaleIndependentBBoxSet(self, set):
        r"""
        Get the corners of the scale independent bounding box of the specified Set.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            Update()
    
            sethasmembers, xmin, ymin, zmin, xlen, ylen, zlen = GetScaleIndependentBBoxSet( SET_ALL );
    
        :param [in]: set int Desired Set
        :param [out]: xmin_out double Minimum bounding box X coordinate
        :param [out]: ymin_out double Minimum bounding box Y coordinate
        :param [out]: zmin_out double Minimum bounding box Z coordinate
        :param [out]: xlen_out double Maximum bounding box X length
        :param [out]: ylen_out double Maximum bounding box Y length
        :param [out]: zlen_out double Maximum bounding box Z length
        :rtype: boolean
        :return: bool Flag indicating whether the set has members (is non-empty)
        """
        return _vsp.GetScaleIndependentBBoxSet(set)
    
    @client_wrap
    def ScaleSet(self, set_index, scale):
        r"""
        Apply a scale factor to a set
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE" )
    
            SetSetFlag( fuseid, 3, True )
    
            # Scale by a factor of 2
            ScaleSet( 3, 2.0 )
    
    
        :param [in]: set_index Set index
        :param [in]: scale Scale factor
        """
        return _vsp.ScaleSet(set_index, scale)
    
    @client_wrap
    def RotateSet(self, set_index, x_rot_deg, y_rot_deg, z_rot_deg):
        r"""
        Rotate a set about the global X, Y, and Z axes
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE" )
    
            SetSetFlag( fuseid, 3, True )
    
            # Rotate 90 degrees about Y
            RotateSet( 3, 0, 90, 0 )
    
    
        :param [in]: set_index Set index
        :param [in]: x_rot_deg Rotation about the X axis (degrees)
        :param [in]: y_rot_deg Rotation about the Y axis (degrees)
        :param [in]: z_rot_deg Rotation about the Z axis (degrees)
        """
        return _vsp.RotateSet(set_index, x_rot_deg, y_rot_deg, z_rot_deg)
    
    @client_wrap
    def TranslateSet(self, set_index, translation_vec):
        r"""
        Translate a set along a given vector
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE" )
    
            SetSetFlag( fuseid, 3, True )
    
            # Translate 2 units in X and 3 units in Y
            TranslateSet( 3, vec3d( 2, 3, 0 ) )
    
    
        :param [in]: set_index Set index
        :param [in]: translation_vec Translation vector
        """
        return _vsp.TranslateSet(set_index, translation_vec)
    
    @client_wrap
    def TransformSet(self, set_index, translation_vec, x_rot_deg, y_rot_deg, z_rot_deg, scale, scale_translations_flag):
        r"""
        Apply translation, rotation, and scale transformations to a set
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE" )
    
            SetSetFlag( fuseid, 3, True )
    
            # Translate 2 units in X and 3 units in Y, rotate 90 degrees about Y, and scale by a factor of 2
            TransformSet( 3, vec3d( 2, 3, 0 ), 0, 90, 0, 2.0, True )
    
    
        See also: TranslateSet, RotateSet, ScaleSet
        :param [in]: set_index Set index
        :param [in]: translation_vec Translation vector
        :param [in]: x_rot_deg Rotation about the X axis (degrees)
        :param [in]: y_rot_deg Rotation about the Y axis (degrees)
        :param [in]: z_rot_deg Rotation about the Z axis (degrees)
        :param [in]: scale Scale factor
        :param [in]: scale_translations_flag Flag to apply the scale factor to translations
        """
        return _vsp.TransformSet(set_index, translation_vec, x_rot_deg, y_rot_deg, z_rot_deg, scale, scale_translations_flag)
    
    @client_wrap
    def ValidParm(self, id):
        r"""
        Check if given Parm is valid
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pid = AddGeom( "POD" )
    
            lenid = GetParm( pid, "Length", "Design" )
    
            if  not ValidParm( lenid ) : print( "---> Error: API GetParm  " )
    
    
        :param [in]: id Parm ID
        :rtype: boolean
        :return: True if Parm ID is valid, false otherwise
        """
        return _vsp.ValidParm(id)
    
    @client_wrap
    def SetParmVal(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Set the value of the specified Parm.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 23.0 )
    
            if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )
    
    
        See also: SetParmValUpdate
        :param [in]: parm_id string Parm ID
        :param [in]: val Parm value to set
        :rtype: float
        :return: Value that the Parm was set to
    
    
        |
    
        *Overload 2:*
    
    
    
        Set the value of the specified Parm.
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 23.0 )
    
            if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )
    
    
        See also: SetParmValUpdate
        :param [in]: geom_id string Geom ID
        :param [in]: name string Parm name
        :param [in]: group string Parm group name
        :param [in]: val double Parm value to set
        :rtype: float
        :return: double Value that the Parm was set to
        """
        return _vsp.SetParmVal(*args)
    
    @client_wrap
    def SetParmValLimits(self, parm_id, val, lower_limit, upper_limit):
        r"""
        Set the value along with the upper and lower limits of the specified Parm
    
    
        .. code-block:: python
    
            pod_id = AddGeom( "POD" )
    
            length = FindParm( pod_id, "Length", "Design" )
    
            SetParmValLimits( length, 10.0, 0.001, 1.0e12 )
    
            SetParmDescript( length, "Total Length of Geom" )
    
    
        See also: SetParmLowerLimit, SetParmUpperLimit
        :param [in]: parm_id string Parm ID
        :param [in]: val Parm value to set
        :param [in]: lower_limit Parm lower limit
        :param [in]: upper_limit Parm upper limit
        :rtype: float
        :return: Value that the Parm was set to
        """
        return _vsp.SetParmValLimits(parm_id, val, lower_limit, upper_limit)
    
    @client_wrap
    def SetParmValUpdate(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Set the value of the specified Parm and force an Update.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            parm_id = GetParm( pod_id, "X_Rel_Location", "XForm" )
    
            SetParmValUpdate( parm_id, 5.0 )
    
    
        See also: SetParmVal
        :param [in]: parm_id string Parm ID
        :param [in]: val Parm value to set
        :rtype: float
        :return: Value that the Parm was set to
    
    
        |
    
        *Overload 2:*
    
    
    
        Set the value of the specified Parm and force an Update.
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            parm_id = GetParm( pod_id, "X_Rel_Location", "XForm" )
    
            SetParmValUpdate( parm_id, 5.0 )
    
    
        See also: SetParmVal
        :param [in]: geom_id string Geom ID
        :param [in]: parm_name string Parm name
        :param [in]: parm_group_name string Parm group name
        :param [in]: val double Parm value to set
        :rtype: float
        :return: double Value that the Parm was set to
        """
        return _vsp.SetParmValUpdate(*args)
    
    @client_wrap
    def GetParmVal(self, *args):
        r"""
        *Overload 1:*
    
    
    
        Get the value of the specified Parm. The data type of the Parm value will be cast to a double
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 23.0 )
    
            if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: float
        :return: Parm value
    
    
        |
    
        *Overload 2:*
    
    
    
        Get the value of the specified Parm. The data type of the Parm value will be cast to a double
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 23.0 )
    
            if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: name string Parm name
        :param [in]: group string Parm group name
        :rtype: float
        :return: double Parm value
        """
        return _vsp.GetParmVal(*args)
    
    @client_wrap
    def GetIntParmVal(self, parm_id):
        r"""
        Get the value of the specified int type Parm
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            num_blade_id = GetParm( prop_id, "NumBlade", "Design" )
    
            num_blade = GetIntParmVal( num_blade_id )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: int
        :return: double Parm value
        """
        return _vsp.GetIntParmVal(parm_id)
    
    @client_wrap
    def GetBoolParmVal(self, parm_id):
        r"""
        Get the value of the specified bool type Parm
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            rev_flag_id = GetParm( prop_id, "ReverseFlag", "Design" )
    
            reverse_flag = GetBoolParmVal( rev_flag_id )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: boolean
        :return: bool Parm value
        """
        return _vsp.GetBoolParmVal(parm_id)
    
    @client_wrap
    def SetParmUpperLimit(self, parm_id, val):
        r"""
        Set the upper limit value for the specified Parm
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 23.0 )
    
            SetParmUpperLimit( wid, 13.0 )
    
            if  abs( GetParmVal( wid ) - 13 ) > 1e-6 : print( "---> Error: API SetParmUpperLimit " )
    
    
        See also: SetParmValLimits
        :param [in]: parm_id string Parm ID
        :param [in]: val double Parm upper limit
        """
        return _vsp.SetParmUpperLimit(parm_id, val)
    
    @client_wrap
    def GetParmUpperLimit(self, parm_id):
        r"""
        Get the upper limit value for the specified Parm
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            num_blade_id = GetParm( prop_id, "NumBlade", "Design" )
    
            max_blade = GetParmUpperLimit( num_blade_id )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: float
        :return: double Parm upper limit
        """
        return _vsp.GetParmUpperLimit(parm_id)
    
    @client_wrap
    def SetParmLowerLimit(self, parm_id, val):
        r"""
        Set the lower limit value for the specified Parm
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            SetParmVal( wid, 13.0 )
    
            SetParmLowerLimit( wid, 15.0 )
    
            if  abs( GetParmVal( wid ) - 15 ) > 1e-6 : print( "---> Error: API SetParmLowerLimit " )
    
    
        See also: SetParmValLimits
        :param [in]: parm_id string Parm ID
        :param [in]: val Parm lower limit
        """
        return _vsp.SetParmLowerLimit(parm_id, val)
    
    @client_wrap
    def GetParmLowerLimit(self, parm_id):
        r"""
        Get the lower limit value for the specified Parm
    
    
        .. code-block:: python
    
            #==== Add Prop Geometry ====//
            prop_id = AddGeom( "PROP" )
    
            num_blade_id = GetParm( prop_id, "NumBlade", "Design" )
    
            min_blade = GetParmLowerLimit( num_blade_id )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: float
        :return: Parm lower limit
        """
        return _vsp.GetParmLowerLimit(parm_id)
    
    @client_wrap
    def GetParmType(self, parm_id):
        r"""
        Get the data type for the specified Parm
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            if  GetParmType( wid ) != PARM_DOUBLE_TYPE : print( "---> Error: API GetParmType " )
    
    
        See also: PARM_TYPE
        :param [in]: parm_id string Parm ID
        :rtype: int
        :return: Parm data type enum (i.e. PARM_BOOL_TYPE)
        """
        return _vsp.GetParmType(parm_id)
    
    @client_wrap
    def GetParmName(self, parm_id):
        r"""
        Get the name for the specified Parm
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Get Structure Name and Parm Container ID ====//
            parm_container_name = GetFeaStructName( pod_id, struct_ind )
    
            parm_container_id = FindContainer( parm_container_name, struct_ind )
    
            #==== Get and List All Parms in the Container ====//
            parm_ids = FindContainerParmIDs( parm_container_id )
    
            for i in range(len(parm_ids)):
    
                name_id = GetParmName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"
    
                print( name_id )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: string
        :return: Parm name
        """
        return _vsp.GetParmName(parm_id)
    
    @client_wrap
    def GetParmGroupName(self, parm_id):
        r"""
        Get the group name for the specified Parm
    
    
        .. code-block:: python
    
            veh_id = FindContainer( "Vehicle", 0 )
    
            #==== Get and List All Parms in the Container ====//
            parm_ids = FindContainerParmIDs( veh_id )
    
            print( "Parm Groups and IDs in Vehicle Parm Container: " )
    
            for i in range(len(parm_ids)):
    
                group_str = GetParmGroupName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"
    
                print( group_str )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: string
        :return: Parm group name
        """
        return _vsp.GetParmGroupName(parm_id)
    
    @client_wrap
    def GetParmDisplayGroupName(self, parm_id):
        r"""
        Get the display group name for the specified Parm
    
    
        .. code-block:: python
    
            veh_id = FindContainer( "Vehicle", 0 )
    
            #==== Get and List All Parms in the Container ====//
            parm_ids = FindContainerParmIDs( veh_id )
    
            print( "Parm Group Display Names and IDs in Vehicle Parm Container: " )
    
            for i in range(len(parm_ids)):
    
                group_str = GetParmDisplayGroupName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"
    
                print( group_str )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: string
        :return: Parm display group name
        """
        return _vsp.GetParmDisplayGroupName(parm_id)
    
    @client_wrap
    def GetParmContainer(self, parm_id):
        r"""
        Get Parm Container ID for the specified Parm
    
    
        .. code-block:: python
    
            # Add Fuselage Geom
            fuseid = AddGeom( "FUSELAGE", "" )
    
            xsec_surf = GetXSecSurf( fuseid, 0 )
    
            ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )
    
            xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )
    
            wid = GetXSecParm( xsec, "RoundedRect_Width" )
    
            cid = GetParmContainer( wid )
    
            if  len(cid) == 0 : print( "---> Error: API GetParmContainer " )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: string
        :return: Parm Container ID
        """
        return _vsp.GetParmContainer(parm_id)
    
    @client_wrap
    def SetParmDescript(self, parm_id, desc):
        r"""
        Set the description of the specified Parm
    
    
        .. code-block:: python
    
            pod_id = AddGeom( "POD" )
    
            length = FindParm( pod_id, "Length", "Design" )
    
            SetParmValLimits( length, 10.0, 0.001, 1.0e12 )
    
            SetParmDescript( length, "Total Length of Geom" )
    
    
        :param [in]: parm_id string Parm ID
        :param [in]: desc Parm description
        """
        return _vsp.SetParmDescript(parm_id, desc)
    
    @client_wrap
    def GetParmDescript(self, parm_id):
        r"""
        Get the description of the specified Parm
    
    
        .. code-block:: python
    
            pod_id = AddGeom( "POD" )
    
            length = FindParm( pod_id, "Length", "Design" )
    
            SetParmValLimits( length, 10.0, 0.001, 1.0e12 )
    
            desc = GetParmDescript( length )
            print( desc )
    
    
        :param [in]: parm_id string Parm ID
        :rtype: string
        :return: desc Parm description
        """
        return _vsp.GetParmDescript(parm_id)
    
    @client_wrap
    def FindParm(self, parm_container_id, parm_name, group_name):
        r"""
        Find a Parm ID given the Parm Container ID, Parm name, and Parm group
    
    
        .. code-block:: python
    
            #==== Add Wing Geometry ====//
            wing_id = AddGeom( "WING" )
    
            #==== Turn Symmetry OFF ====//
            sym_id = FindParm( wing_id, "Sym_Planar_Flag", "Sym")
    
            SetParmVal( sym_id, 0.0 ) # Note: bool input not supported in SetParmVal
    
    
        :param [in]: parm_container_id Parm Container ID
        :param [in]: parm_name Parm name
        :param [in]: group_name Parm group name
        :rtype: string
        :return: Parm ID
        """
        return _vsp.FindParm(parm_container_id, parm_name, group_name)
    
    @client_wrap
    def FindContainers(self, ):
        r"""
        Get an array of all Parm Container IDs
    
    
        .. code-block:: python
    
            ctr_arr = FindContainers()
    
            print( "---> API Parm Container IDs: " )
    
            for i in range(int( len(ctr_arr) )):
    
                message = "\t" + ctr_arr[i] + "\n"
    
                print( message )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm Container IDs
        """
        return _vsp.FindContainers()
    
    @client_wrap
    def FindContainersWithName(self, name):
        r"""
        Get an array of Parm Container IDs for Containers with the specified name
    
    
        .. code-block:: python
    
            ctr_arr = FindContainersWithName( "UserParms" )
    
            if  len(ctr_arr) > 0 : print( ( "UserParms Parm Container ID: " + ctr_arr[0] ) )
    
    
        :param [in]: name Parm Container name
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm Container IDs
        """
        return _vsp.FindContainersWithName(name)
    
    @client_wrap
    def FindContainer(self, name, index):
        r"""
        Get the ID of a Parm Container with specified name at input index
    
    
        .. code-block:: python
    
            #===== Get Vehicle Parm Container ID ====//
            veh_id = FindContainer( "Vehicle", 0 )
    
    
        See also: FindContainersWithName
        :param [in]: name Parm Container name
        :param [in]: index Parm Container index
        :rtype: string
        :return: Parm Container ID
        """
        return _vsp.FindContainer(name, index)
    
    @client_wrap
    def GetContainerName(self, parm_container_id):
        r"""
        Get the name of the specified Parm Container
    
    
        .. code-block:: python
    
            veh_id = FindContainer( "Vehicle", 0 )
    
            if  GetContainerName( veh_id) != "Vehicle":       print( "---> Error: API GetContainerName" )
    
    
        :param [in]: parm_container_id Parm Container ID
        :rtype: string
        :return: Parm Container name
        """
        return _vsp.GetContainerName(parm_container_id)
    
    @client_wrap
    def FindContainerGroupNames(self, parm_container_id):
        r"""
        Get an array of Parm group names included in the specified Container
    
    
        .. code-block:: python
    
            user_ctr = FindContainer( "UserParms", 0 )
    
            grp_arr = FindContainerGroupNames( user_ctr )
    
            print( "---> UserParms Container Group IDs: " )
            for i in range(int( len(grp_arr) )):
    
                message = "\t" + grp_arr[i] + "\n"
    
                print( message )
    
    
        :param [in]: parm_container_id Parm Container ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm group names
        """
        return _vsp.FindContainerGroupNames(parm_container_id)
    
    @client_wrap
    def FindContainerParmIDs(self, parm_container_id):
        r"""
        Get an array of Parm IDs included in the specified Container
    
    
        .. code-block:: python
    
            #==== Add Pod Geometry ====//
            pod_id = AddGeom( "POD" )
    
            #==== Add FeaStructure to Pod ====//
            struct_ind = AddFeaStruct( pod_id )
    
            #==== Get Structure Name and Parm Container ID ====//
            parm_container_name = GetFeaStructName( pod_id, struct_ind )
    
            parm_container_id = FindContainer( parm_container_name, struct_ind )
    
            #==== Get and List All Parms in the Container ====//
            parm_ids = FindContainerParmIDs( parm_container_id )
    
            for i in range(len(parm_ids)):
    
                name_id = GetParmName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"
    
                print( name_id )
    
    
        :param [in]: parm_container_id Parm Container ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of Parm IDs
        """
        return _vsp.FindContainerParmIDs(parm_container_id)
    
    @client_wrap
    def GetVehicleID(self, ):
        r"""
        Get the ID of the Vehicle Parm Container
    
    
        .. code-block:: python
    
            #===== Get Vehicle Parm Container ID ====//
            veh_id = GetVehicleID()
    
    
        :rtype: string
        :return: Vehicle ID
        """
        return _vsp.GetVehicleID()
    
    @client_wrap
    def GetNumUserParms(self, ):
        r"""
        Get the number of user parameters
    
    
        .. code-block:: python
    
            n = GetNumUserParms()
    
    
    
        :rtype: int
        :return: Number of user Parms
        """
        return _vsp.GetNumUserParms()
    
    @client_wrap
    def GetNumPredefinedUserParms(self, ):
        r"""
        Get the number of pre-defined user parameters
    
    
        .. code-block:: python
    
            n = GetNumPredefinedUserParms()
    
    
    
        :rtype: int
        :return: Number of pre-defined user Parms
        """
        return _vsp.GetNumPredefinedUserParms()
    
    @client_wrap
    def GetAllUserParms(self, ):
        r"""
        Get the vector of id's for all user parameters
    
    
        .. code-block:: python
    
            id_arr = GetAllUserParms()
    
            print( "---> User Parm IDs: " )
    
            for i in range(int( len(id_arr) )):
    
                message = "\t" + id_arr[i] + "\n"
    
                print( message )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of user parameter ids
        """
        return _vsp.GetAllUserParms()
    
    @client_wrap
    def GetUserParmContainer(self, ):
        r"""
        Get the user parm container ID
    
    
        .. code-block:: python
    
            up_id = GetUserParmContainer()
    
    
        :rtype: string
        :return: User parm container ID
        """
        return _vsp.GetUserParmContainer()
    
    @client_wrap
    def AddUserParm(self, type, name, group):
        r"""
        Function to add a new user Parm of input type, name, and group
    
    
        .. code-block:: python
    
            length = AddUserParm( PARM_DOUBLE_TYPE, "Length", "Design" )
    
            SetParmValLimits( length, 10.0, 0.001, 1.0e12 )
    
            SetParmDescript( length, "Length user parameter" )
    
    
        See also: PARM_TYPE
        :param [in]: type Parm type enum (i.e. PARM_DOUBLE_TYPE)
        :param [in]: name Parm name
        :param [in]: group Parm group
        :rtype: string
        :return: Parm ID
        """
        return _vsp.AddUserParm(type, name, group)
    
    @client_wrap
    def DeleteUserParm(self, id):
        r"""
        Get the user parm container ID
    
    
        .. code-block:: python
    
    
            n = GetNumPredefinedUserParms()
            id_arr = GetAllUserParms()
    
            if  len(id_arr) > n :
                DeleteUserParm( id_arr[n] )
    
    
        """
        return _vsp.DeleteUserParm(id)
    
    @client_wrap
    def DeleteAllUserParm(self, ):
        r"""
        Get the user parm container ID
    
    
        .. code-block:: python
    
            DeleteAllUserParm()
    
    
        """
        return _vsp.DeleteAllUserParm()
    
    @client_wrap
    def ComputeMinClearanceDistance(self, *args):
        r"""
        Compute the minimum clearance distance for the specified geometry
    
    
        .. code-block:: python
    
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            pid = AddGeom( "POD", "" )                     # Add Pod
    
            x = GetParm( pid, "X_Rel_Location", "XForm" )
    
            SetParmVal( x, 3.0 )
    
            Update()
    
            min_dist = ComputeMinClearanceDistance( pid, SET_ALL )
    
    
        :param [in]: geom_id string Geom ID
        :param [in]: set Collision set enum (i.e. SET_ALL)
        :param [in]: useMode bool Flag determine if mode is used instead of sets
        :param [in]: modeID string ID of Mode to use
        :rtype: float
        :return: Minimum clearance distance
        """
        return _vsp.ComputeMinClearanceDistance(*args)
    
    @client_wrap
    def SnapParm(self, *args):
        r"""
        Snap the specified Parm to input target minimum clearance distance
    
    
        .. code-block:: python
    
            #Add Geoms
            fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage
    
            pid = AddGeom( "POD", "" )                     # Add Pod
    
            x = GetParm( pid, "X_Rel_Location", "XForm" )
    
            SetParmVal( x, 3.0 )
    
            Update()
    
            min_dist = SnapParm( x, 0.1, True, SET_ALL )
    
    
        :param [in]: parm_id string Parm ID
        :param [in]: target_min_dist Target minimum clearance distance
        :param [in]: inc_flag Direction indication flag. If true, upper parm limit is used and direction is set to positive
        :param [in]: set Collision set enum (i.e. SET_ALL)
        :param [in]: useMode bool Flag determine if mode is used instead of sets
        :param [in]: modeID string ID of Mode to use
        :rtype: float
        :return: Minimum clearance distance
        """
        return _vsp.SnapParm(*args)
    
    @client_wrap
    def AddVarPresetGroup(self, group_name):
        r"""
        Add a Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
        :param [in]: group_name string Name for Var Preset Group
        :rtype: string
        :return: string Var Preset Group ID
        """
        return _vsp.AddVarPresetGroup(group_name)
    
    @client_wrap
    def AddVarPresetSetting(self, group_id, setting_name):
        r"""
        Add a Setting to the Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_name string Var Preset Setting Name
        :rtype: string
        :return: string Var Preset Setting ID
        """
        return _vsp.AddVarPresetSetting(group_id, setting_name)
    
    @client_wrap
    def AddVarPresetParm(self, group_id, parm_id):
        r"""
        Add a Parm to the Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: parm_id string Parm ID
        """
        return _vsp.AddVarPresetParm(group_id, parm_id)
    
    @client_wrap
    def DeleteVarPresetGroup(self, group_id):
        r"""
        Delete Variable Preset Group (and all contained settings)
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            DeleteVarPresetGroup( gid )
    
    
        :param [in]: group_id string Var Preset Group ID
        """
        return _vsp.DeleteVarPresetGroup(group_id)
    
    @client_wrap
    def DeleteVarPresetSetting(self, group_id, setting_id):
        r"""
        Delete Variable Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            DeleteVarPresetSetting( gid, sid )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_id string Var Preset Setting ID
        """
        return _vsp.DeleteVarPresetSetting(group_id, setting_id)
    
    @client_wrap
    def DeleteVarPresetParm(self, group_id, parm_id):
        r"""
        Delete Parm from Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            DeleteVarPresetParm( gid, p1 )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: parm_id string Var Parm ID
        """
        return _vsp.DeleteVarPresetParm(group_id, parm_id)
    
    @client_wrap
    def SetVarPresetParmVal(self, group_id, setting_id, parm_id, parm_val):
        r"""
        Set value for Parm in Var Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            SetVarPresetParmVal( gid, sid, p1, 51 )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_id string Var Preset Setting ID
        :param [in]: parm_id string Var Parm ID
        :param [in]: parm_val double Parm value
        """
        return _vsp.SetVarPresetParmVal(group_id, setting_id, parm_id, parm_val)
    
    @client_wrap
    def GetVarPresetParmVal(self, group_id, setting_id, parm_id):
        r"""
        Get value for Parm in Var Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            val = GetVarPresetParmVal( gid, sid, p1 )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_id string Var Preset Setting ID
        :param [in]: parm_id string Var Parm ID
        :rtype: float
        :return: double Var Preset Parm value
        """
        return _vsp.GetVarPresetParmVal(group_id, setting_id, parm_id)
    
    @client_wrap
    def GetGroupName(self, group_id):
        r"""
        Get Variable Preset group name
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            name = GetGroupName( gid )
    
    
        :param [in]: group_id string Var Preset Group ID
        :rtype: string
        :return: string Var Preset Group name
        """
        return _vsp.GetGroupName(group_id)
    
    @client_wrap
    def GetSettingName(self, setting_id):
        r"""
        Get Variable Preset Setting name
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            name = GetSettingName( sid )
    
    
        :param [in]: setting_id string Var Preset Setting ID
        :rtype: string
        :return: string Var Preset Setting name
        """
        return _vsp.GetSettingName(setting_id)
    
    @client_wrap
    def SetGroupName(self, group_id, group_name):
        r"""
        Set Variable Preset group name
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            SetGroupName( gid, "Resolution" )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: group_name string New Var Preset Group name
        """
        return _vsp.SetGroupName(group_id, group_name)
    
    @client_wrap
    def SetSettingName(self, setting_id, setting_name):
        r"""
        Set Variable Preset Setting name
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            SetSettingName( sid, "Low" )
    
    
        :param [in]: setting_id string Var Preset Setting ID
        :param [in]: setting_name string New Var Preset Setting name
        """
        return _vsp.SetSettingName(setting_id, setting_name)
    
    @client_wrap
    def GetVarPresetGroups(self, ):
        r"""
        Get group_ids for Variable Preset Groups
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            group_ids = GetVarPresetGroups()
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: array<string> Array of Variable Preset Group IDs
        """
        return _vsp.GetVarPresetGroups()
    
    @client_wrap
    def GetVarPresetSettings(self, group_id):
        r"""
        Get Setting IDs for Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            settingds = GetVarPresetSettings( gid )
    
    
        :param [in]: group_id string Var Preset Group ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: array<string> Array of Variable Preset Group ParmIDs
        """
        return _vsp.GetVarPresetSettings(group_id)
    
    @client_wrap
    def GetVarPresetParmIDs(self, group_id):
        r"""
        Get ParmIDs for Variable Preset Group
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            parmids = GetVarPresetParmIDs( gid )
    
    
        :param [in]: group_id string Var Preset Group ID
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: array<string> Array of Variable Preset Group ParmIDs
        """
        return _vsp.GetVarPresetParmIDs(group_id)
    
    @client_wrap
    def GetVarPresetParmVals(self, setting_id):
        r"""
        Get Parm values for Variable Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            parmval_vec = GetVarPresetParmVals( sid )
    
    
        :param [in]: setting_id string Var Preset Setting ID
        :rtype: std::vector< double,std::allocator< double > >
        :return: array<double> Var Preset Parm values for Setting
    
        """
        return _vsp.GetVarPresetParmVals(setting_id)
    
    @client_wrap
    def SetVarPresetParmVals(self, setting_id, parm_vals):
        r"""
        Set Parm values for Variable Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            vals = [ 45 ]
    
            SetVarPresetParmVals( sid, vals )
    
    
        :param [in]: setting_id string Var Preset Setting ID
        :param [in]: parm_vals array<double> Array of Variable Preset Group Parm values
        """
        return _vsp.SetVarPresetParmVals(setting_id, parm_vals)
    
    @client_wrap
    def SaveVarPresetParmVals(self, group_id, setting_id):
        r"""
        Save current Parm values to Variable Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            SaveVarPresetParmVals( gid, sid )
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_id string Var Preset Setting ID
        """
        return _vsp.SaveVarPresetParmVals(group_id, setting_id)
    
    @client_wrap
    def ApplyVarPresetSetting(self, group_id, setting_id):
        r"""
        Apply Parm values for Var Preset Setting
    
    
        .. code-block:: python
    
            # Add Pod Geom
            pod1 = AddGeom( "POD", "" )
    
            gid = AddVarPresetGroup( "Tess" )
    
            sid = AddVarPresetSetting( gid, "Coarse" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
    
            AddVarPresetParm( gid, p1 )
    
            ApplyVarPresetSetting( gid, sid )
    
            Update()
    
    
        :param [in]: group_id string Var Preset Group ID
        :param [in]: setting_id string Var Preset Setting ID
        """
        return _vsp.ApplyVarPresetSetting(group_id, setting_id)
    
    @client_wrap
    def CreateAndAddMode(self, name, normal_set, degen_set):
        r"""
        Create a Mode -- a combination of Sets and Variable Presets
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
    
        :param [in]: name string Name for new Mode
        :param [in]: normal_set int Normal set for Mode
        :param [in]: degen_set int Degen set for Mode
        :rtype: string
        :return: string Mode ID for new Mode
        """
        return _vsp.CreateAndAddMode(name, normal_set, degen_set)
    
    @client_wrap
    def GetNumModes(self, ):
        r"""
        Get number of Modes in model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            nmod = GetNumModes()
    
    
        :rtype: int
        :return: int Number of Modes in model.
        """
        return _vsp.GetNumModes()
    
    @client_wrap
    def GetAllModes(self, ):
        r"""
        Get all ModeID's in model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            modids = GetAllModes();
    
    
        :rtype: vector< string >
        :return: array<string> array of Mode IDs
        """
        return _vsp.GetAllModes()
    
    @client_wrap
    def DelMode(self, mid):
        r"""
        Delete a mode from the model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            DelMode( mid1 )
    
    
        :param [in]: mid string Mode ID of mode to delete
        """
        return _vsp.DelMode(mid)
    
    @client_wrap
    def DelAllModes(self, ):
        r"""
        Delete all modes from the model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            DelAllModes()
    
    
        """
        return _vsp.DelAllModes()
    
    @client_wrap
    def ApplyModeSettings(self, mid):
        r"""
        Apply Parm settings corresponding to a Mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
    
        :param [in]: mid string Mode ID of mode to apply
        """
        return _vsp.ApplyModeSettings(mid)
    
    @client_wrap
    def ShowOnlyMode(self, mid):
        r"""
        Show-only a mode in a model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            ShowOnlyMode( mid1 )
    
    
        :param [in]: mid string Mode ID of mode to show-only
        """
        return _vsp.ShowOnlyMode(mid)
    
    @client_wrap
    def ModeAddGroupSetting(self, mid, gid, sid):
        r"""
        Add a variable preset group and setting to a mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
    
        :param [in]: mid string Mode ID to add variable preset to
        :param [in]: gid string Variable preset group ID to add to mode
        :param [in]: sid string Variable preset setting ID to add to mode
        """
        return _vsp.ModeAddGroupSetting(mid, gid, sid)
    
    @client_wrap
    def ModeGetGroup(self, mid, indx):
        r"""
        Get the group ID of var preset indx from a mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            gid3 = ModeGetGroup( mid1, 0 )
    
    
        :param [in]: mid string Mode ID to return GroupID
        :param [in]: indx int Index of Variable preset to return GroupID
        :rtype: string
        :return: string Group ID for Mode Variable preset indx
        """
        return _vsp.ModeGetGroup(mid, indx)
    
    @client_wrap
    def ModeGetSetting(self, mid, indx):
        r"""
        Get the setting ID of var preset indx from a mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            sid6 = ModeGetSetting( mid1, 0 )
    
    
        :param [in]: mid string Mode ID to return settingID
        :param [in]: indx int Index of Variable preset to return SettingID
        :rtype: string
        :return: string Setting ID for Mode Variable preset indx
        """
        return _vsp.ModeGetSetting(mid, indx)
    
    @client_wrap
    def ModeGetAllGroups(self, mid):
        r"""
        Get all var preset group IDs in model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            gids = ModeGetAllGroups( mid1 )
    
    
        :param [in]: mid string Mode ID to return all group IDs
        :rtype: vector< string >
        :return: array<string> array of Group IDs
        """
        return _vsp.ModeGetAllGroups(mid)
    
    @client_wrap
    def ModeGetAllSettings(self, mid):
        r"""
        Get all var preset setting IDs in model.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            sids = ModeGetAllSettings( mid1 )
    
    
        :param [in]: mid string Mode ID to return all group IDs
        :rtype: vector< string >
        :return: array<string> array of Group IDs
        """
        return _vsp.ModeGetAllSettings(mid)
    
    @client_wrap
    def RemoveGroupSetting(self, mid, indx):
        r"""
        Remove the indx'th variable preset group and setting from the specified mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            RemoveGroupSetting( mid1, 0 )
    
    
        :param [in]: mid string Mode ID to remove varible preset group and setting from
        :param [in]: indx int Index of Variable preset to remove
        """
        return _vsp.RemoveGroupSetting(mid, indx)
    
    @client_wrap
    def RemoveAllGroupSettings(self, mid):
        r"""
        Remove all variable preset groups and settings from mode.
    
    
        .. code-block:: python
    
            # Illustrating use of Modes requires substantial setup of the model including components, sets, and variable presets.
            #
            # Setup boiler plate.
            pod1 = AddGeom( "POD", "" )
            wing = AddGeom( "WING", pod1 )
    
            SetParmVal( wing, "Trans_Attach_Flag", "Attach", ATTACH_TRANS_LMN )
            SetParmVal( wing, "L_Attach_Location", "Attach", 0.35 )
    
            SetSetName( SET_FIRST_USER, "NonLifting" )
            SetSetName( SET_FIRST_USER + 1, "Lifting" )
    
            SetSetFlag( pod1, SET_FIRST_USER, True )
            SetSetFlag( wing, SET_FIRST_USER + 1, True )
    
    
            gid = AddVarPresetGroup( "Tess" )
    
            p1 = FindParm( pod1, "Tess_U", "Shape" )
            AddVarPresetParm( gid, p1 )
    
            p2 = FindParm( pod1, "Tess_W", "Shape" )
            AddVarPresetParm( gid, p2 )
    
            sid = AddVarPresetSetting( gid, "Default" )
            SaveVarPresetParmVals( gid, sid )
    
            sid1 = AddVarPresetSetting( gid, "Coarse" )
            SetVarPresetParmVal( gid, sid1, p1, 3 )
            SetVarPresetParmVal( gid, sid1, p2, 5 )
    
            sid2 = AddVarPresetSetting( gid, "Fine" )
            SetVarPresetParmVal( gid, sid, p1, 35 )
            SetVarPresetParmVal( gid, sid, p2, 21 )
    
    
            gid2 = AddVarPresetGroup( "Design" )
    
            p3 = FindParm( pod1, "Length", "Design" )
            AddVarPresetParm( gid2, p3 )
    
            p4 = FindParm( pod1, "FineRatio", "Design" )
            AddVarPresetParm( gid2, p4 )
    
            sid3 = AddVarPresetSetting( gid2, "Normal" )
            SaveVarPresetParmVals( gid2, sid3 )
    
            sid4 = AddVarPresetSetting( gid2, "ShortFat" )
            SetVarPresetParmVal( gid2, sid4, p3, 3.0 )
            SetVarPresetParmVal( gid2, sid4, p4, 5.0 )
    
            sid5 = AddVarPresetSetting( gid2, "LongThin" )
            SetVarPresetParmVal( gid2, sid5, p3, 20.0 )
            SetVarPresetParmVal( gid2, sid5, p4, 35.0 )
    
            # End of setup boiler plate.
    
            mid1 = CreateAndAddMode( "FatWetAreas", SET_ALL, SET_NONE )
            ModeAddGroupSetting( mid1, gid, sid1 )
            ModeAddGroupSetting( mid1, gid2, sid4 )
    
            mid2 = CreateAndAddMode( "ThinAero", SET_FIRST_USER, SET_FIRST_USER + 1 )
            ModeAddGroupSetting( mid2, gid, sid2 )
            ModeAddGroupSetting( mid1, gid2, sid5 )
    
            ApplyModeSettings( mid2 )
            Update()
    
            RemoveAllGroupSettings( mid1 )
    
    
        :param [in]: mid string Mode ID to remove all variable presets from
        """
        return _vsp.RemoveAllGroupSettings(mid)
    
    @client_wrap
    def SetPCurve(self, geom_id, pcurveid, tvec, valvec, newtype):
        r"""
        Set the parameters, values, and curve type of a propeller blade curve (P Curve)
        See also: PCURV_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :param [in]: tvec Array of parameter values
        :param [in]: valvec Array of values
        :param [in]: newtype Curve type enum (i.e. CEDIT)
        """
        return _vsp.SetPCurve(geom_id, pcurveid, tvec, valvec, newtype)
    
    @client_wrap
    def PCurveConvertTo(self, geom_id, pcurveid, newtype):
        r"""
        Change the type of a propeller blade curve (P Curve)
        See also: PCURV_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :param [in]: newtype Curve type enum (i.e. CEDIT)
        """
        return _vsp.PCurveConvertTo(geom_id, pcurveid, newtype)
    
    @client_wrap
    def PCurveGetType(self, geom_id, pcurveid):
        r"""
        Get the type of a propeller blade curve (P Curve)
        See also: PCURV_TYPE
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :rtype: int
        :return: Curve type enum (i.e. CEDIT)
        """
        return _vsp.PCurveGetType(geom_id, pcurveid)
    
    @client_wrap
    def PCurveGetTVec(self, geom_id, pcurveid):
        r"""
        Get the parameters of a propeller blade curve (P Curve). Each parameter is a fraction of propeller radius.
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :rtype: std::vector< double,std::allocator< double > >
        :return: Array of parameters
        """
        return _vsp.PCurveGetTVec(geom_id, pcurveid)
    
    @client_wrap
    def PCurveGetValVec(self, geom_id, pcurveid):
        r"""
        Get the values of a propeller blade curve (P Curve). What the values represent id dependent on the curve type (i.e. twist, chord, etc.).
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :rtype: std::vector< double,std::allocator< double > >
        :return: Array of values
        """
        return _vsp.PCurveGetValVec(geom_id, pcurveid)
    
    @client_wrap
    def PCurveDeletePt(self, geom_id, pcurveid, indx):
        r"""
        Delete a propeller blade curve (P Curve) point
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :param [in]: indx Point index
        """
        return _vsp.PCurveDeletePt(geom_id, pcurveid, indx)
    
    @client_wrap
    def PCurveSplit(self, geom_id, pcurveid, tsplit):
        r"""
        Split a propeller blade curve (P Curve) at the specified 1D parameter
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pcurveid P Curve index
        :param [in]: tsplit 1D parameter split location
        :rtype: int
        :return: Index of new control point
        """
        return _vsp.PCurveSplit(geom_id, pcurveid, tsplit)
    
    @client_wrap
    def ApproximateAllPropellerPCurves(self, geom_id):
        r"""
        Approximate all propeller blade curves with cubic Bezier curves.
    
    
        .. code-block:: python
    
            # Add Propeller
            prop = AddGeom( "PROP", "" )
    
            ApproximateAllPropellerPCurves( prop )
    
    
    
        :param [in]: geom_id string Geom ID
        """
        return _vsp.ApproximateAllPropellerPCurves(geom_id)
    
    @client_wrap
    def ResetPropellerThicknessCurve(self, geom_id):
        r"""
        Reset propeller T/C curve to match basic thickness of file-type airfoils.  Typically only used for a propeller that
        has been constructed with file-type airfoils across the blade.  The new thickness curve will be a PCHIP curve
        with t/c matching the propeller's XSecs -- unless it is a file XSec, then the Base thickness is used.
    
    
        .. code-block:: python
    
            # Add Propeller
            prop = AddGeom( "PROP", "" )
    
            ResetPropellerThicknessCurve( prop )
    
    
    
        :param [in]: geom_id string Geom ID
        """
        return _vsp.ResetPropellerThicknessCurve(geom_id)
    
    @client_wrap
    def AutoGroupVSPAEROControlSurfaces(self, ):
        r"""
        Creates the initial default grouping for the control surfaces.
        The initial grouping collects all surface copies of the sub-surface into a single group.
        For example if a wing is defined with an aileron and that wing is symmetrical about the
        xz plane there will be a surface copy of the master wing surface as well as a copy of
        the sub-surface. The two sub-surfaces may get deflected differently during analysis
        routines and can be identified uniquely by their full name.
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            #==== Add Vertical tail and set some parameters =====//
            vert_id = AddGeom( "WING" )
    
            SetGeomName( vert_id, "Vert" )
    
            SetParmValUpdate( vert_id, "TotalArea", "WingGeom", 10.0 )
            SetParmValUpdate( vert_id, "X_Rel_Location", "XForm", 8.5 )
            SetParmValUpdate( vert_id, "X_Rel_Rotation", "XForm", 90 )
    
            rudder_id = AddSubSurf( vert_id, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            AutoGroupVSPAEROControlSurfaces()
    
            Update()
    
            print( "COMPLETE\n" )
            control_group_settings_container_id = FindContainer( "VSPAEROSettings", 0 )   # auto grouping produces parm containers within VSPAEROSettings
    
            #==== Set Control Surface Group Deflection Angle ====//
            print( "\tSetting control surface group deflection angles..." )
    
            # subsurfaces get added to groups with "CSGQualities_[geom_name]_[control_surf_name]"
            # subsurfaces gain parm name is "Surf[surfndx]_Gain" starting from 0 to NumSymmetricCopies-1
    
            deflection_gain_id = FindParm( control_group_settings_container_id, "Surf_" + aileron_id + "_0_Gain", "ControlSurfaceGroup_0" )
            deflection_gain_id = FindParm( control_group_settings_container_id, "Surf_" + aileron_id + "_1_Gain", "ControlSurfaceGroup_0" )
    
            #  deflect aileron
            deflection_angle_id = FindParm( control_group_settings_container_id, "DeflectionAngle", "ControlSurfaceGroup_0" )
    
    
        See also: CreateVSPAEROControlSurfaceGroup
        """
        return _vsp.AutoGroupVSPAEROControlSurfaces()
    
    @client_wrap
    def CreateVSPAEROControlSurfaceGroup(self, ):
        r"""
        Add a new VSPAERO control surface group using the default naming convention. The control surface group will not contain any
        control surfaces until they are added.
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            num_group = GetNumControlSurfaceGroups()
    
            if  num_group != 1 : print( "Error: CreateVSPAEROControlSurfaceGroup" )
    
    
        See also: AddSelectedToCSGroup
        :rtype: int
        :return: Index of the new VSPAERO control surface group
        """
        return _vsp.CreateVSPAEROControlSurfaceGroup()
    
    @client_wrap
    def AddAllToVSPAEROControlSurfaceGroup(self, CSGroupIndex):
        r"""
        Add all available control surfaces to the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            AddAllToVSPAEROControlSurfaceGroup( group_index )
    
    
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.AddAllToVSPAEROControlSurfaceGroup(CSGroupIndex)
    
    @client_wrap
    def RemoveAllFromVSPAEROControlSurfaceGroup(self, CSGroupIndex):
        r"""
        Remove all used control surfaces from the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            AddAllToVSPAEROControlSurfaceGroup( group_index )
    
            RemoveAllFromVSPAEROControlSurfaceGroup( group_index ) # Empty control surface group
    
    
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.RemoveAllFromVSPAEROControlSurfaceGroup(CSGroupIndex)
    
    @client_wrap
    def GetActiveCSNameVec(self, CSGroupIndex):
        r"""
        Get the names of each active (used) control surface in the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            AddAllToVSPAEROControlSurfaceGroup( group_index )
    
            cs_name_vec = GetActiveCSNameVec( group_index )
    
            print( "Active CS in Group Index #", False )
            print( group_index )
    
            for i in range(int( len(cs_name_vec) )):
    
                print( cs_name_vec[i] )
    
    
        :param [in]: CSGroupIndex Index of the control surface group
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of active control surface names
        """
        return _vsp.GetActiveCSNameVec(CSGroupIndex)
    
    @client_wrap
    def GetCompleteCSNameVec(self, ):
        r"""
        Get the names of all control surfaces. Some may be active (used) while others may be available.
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            cs_name_vec = GetCompleteCSNameVec()
    
            print( "All Control Surfaces: ", False )
    
            for i in range(int( len(cs_name_vec) )):
    
                print( cs_name_vec[i] )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of all control surface names
        """
        return _vsp.GetCompleteCSNameVec()
    
    @client_wrap
    def GetAvailableCSNameVec(self, CSGroupIndex):
        r"""
        Get the names of each available (not used) control surface in the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            cs_name_vec = GetAvailableCSNameVec( group_index )
    
            cs_ind_vec = [1]
    
            AddSelectedToCSGroup( cs_ind_vec, group_index ) # Add the first available control surface to the group
    
    
        :param [in]: CSGroupIndex Index of the control surface group
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of active control surface names
        """
        return _vsp.GetAvailableCSNameVec(CSGroupIndex)
    
    @client_wrap
    def SetVSPAEROControlGroupName(self, name, CSGroupIndex):
        r"""
        Set the name for the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            SetVSPAEROControlGroupName( "Example_CS_Group", group_index )
    
            print( "CS Group name: ", False )
    
            print( GetVSPAEROControlGroupName( group_index ) )
    
    
        :param [in]: name Name to set for the control surface group
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.SetVSPAEROControlGroupName(name, CSGroupIndex)
    
    @client_wrap
    def GetVSPAEROControlGroupName(self, CSGroupIndex):
        r"""
        Get the name of the control surface group at the specified index
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            SetVSPAEROControlGroupName( "Example_CS_Group", group_index )
    
            print( "CS Group name: ", False )
    
            print( GetVSPAEROControlGroupName( group_index ) )
    
    
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.GetVSPAEROControlGroupName(CSGroupIndex)
    
    @client_wrap
    def AddSelectedToCSGroup(self, selected, CSGroupIndex):
        r"""
        Add each control surfaces in the array of control surface indexes to the control surface group at the specified index.
    
        Warning: The indexes in input "selected" must be matched with available control surfaces identified by GetAvailableCSNameVec.
        The "selected" input uses one- based indexing to associate available control surfaces.
    
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            cs_name_vec = GetAvailableCSNameVec( group_index )
    
            cs_ind_vec = [0] * len(cs_name_vec)
    
            for i in range(int( len(cs_name_vec) )):
    
                cs_ind_vec[i] = i + 1
    
            AddSelectedToCSGroup( cs_ind_vec, group_index ) # Add all available control surfaces to the group
    
    
        See also: GetAvailableCSNameVec
        :param [in]: selected Array of control surface indexes to add to the group. Note, the integer values are one based.
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.AddSelectedToCSGroup(selected, CSGroupIndex)
    
    @client_wrap
    def RemoveSelectedFromCSGroup(self, selected, CSGroupIndex):
        r"""
        Remove each control surfaces in the array of control surface indexes from the control surface group at the specified index.
    
        Warning: The indexes in input "selected" must be matched with active control surfaces identified by GetActiveCSNameVec. The
        "selected" input uses one-based indexing to associate available control surfaces.
    
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" ) # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface
    
            group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group
    
            cs_name_vec = GetAvailableCSNameVec( group_index )
    
            cs_ind_vec = [0] * len(cs_name_vec)
    
            for i in range(int( len(cs_name_vec) )):
    
                cs_ind_vec[i] = i + 1
    
            AddSelectedToCSGroup( cs_ind_vec, group_index ) # Add the available control surfaces to the group
    
            remove_cs_ind_vec = [1]
    
            RemoveSelectedFromCSGroup( remove_cs_ind_vec, group_index ) # Remove the first control surface
    
    
        See also: GetActiveCSNameVec
        :param [in]: selected Array of control surface indexes to remove from the group. Note, the integer values are one based.
        :param [in]: CSGroupIndex Index of the control surface group
        """
        return _vsp.RemoveSelectedFromCSGroup(selected, CSGroupIndex)
    
    @client_wrap
    def GetNumControlSurfaceGroups(self, ):
        r"""
        Get the total number of control surface groups
    
    
        .. code-block:: python
    
            wid = AddGeom( "WING", "" )                             # Add Wing
    
            aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            #==== Add Horizontal tail and set some parameters =====//
            horiz_id = AddGeom( "WING", "" )
    
            SetGeomName( horiz_id, "Vert" )
    
            SetParmValUpdate( horiz_id, "TotalArea", "WingGeom", 10.0 )
            SetParmValUpdate( horiz_id, "X_Rel_Location", "XForm", 8.5 )
    
            elevator_id = AddSubSurf( horiz_id, SS_CONTROL )                      # Add Control Surface Sub-Surface
    
            AutoGroupVSPAEROControlSurfaces()
    
            num_group = GetNumControlSurfaceGroups()
    
            if  num_group != 2 : print( "Error: GetNumControlSurfaceGroups" )
    
    
        :rtype: int
        :return: Number of control surface groups
        """
        return _vsp.GetNumControlSurfaceGroups()
    
    @client_wrap
    def FindActuatorDisk(self, disk_index):
        r"""
        Get the ID of a VSPAERO actuator disk at the specified index. An empty string is returned if
        the index is out of range.
    
    
        .. code-block:: python
    
            # Add a propeller
            prop_id = AddGeom( "PROP", "" )
            SetParmVal( prop_id, "PropMode", "Design", PROP_DISK )
            SetParmVal( prop_id, "Diameter", "Design", 6.0 )
    
            Update()
    
            # Setup the actuator disk VSPAERO parms
            disk_id = FindActuatorDisk( 0 )
    
            SetParmVal( FindParm( disk_id, "RotorRPM", "Rotor" ), 1234.0 )
            SetParmVal( FindParm( disk_id, "RotorCT", "Rotor" ), 0.35 )
            SetParmVal( FindParm( disk_id, "RotorCP", "Rotor" ), 0.55 )
            SetParmVal( FindParm( disk_id, "RotorHubDiameter", "Rotor" ), 1.0 )
    
    
        See also: PROP_MODE
        :param [in]: disk_index Actuator disk index for the current VSPAERO set
        :rtype: string
        :return: Actuator disk ID
        """
        return _vsp.FindActuatorDisk(disk_index)
    
    @client_wrap
    def GetNumActuatorDisks(self, ):
        r"""
        Get the number of actuator disks in the current VSPAERO set. This is equivalent to the number of disk surfaces in the VSPAERO set.
    
    
        .. code-block:: python
    
            # Set VSPAERO set index to SET_ALL
            SetParmVal( FindParm( FindContainer( "VSPAEROSettings", 0 ), "GeomSet", "VSPAERO" ), SET_ALL )
    
            # Add a propeller
            prop_id = AddGeom( "PROP", "" )
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_BLADES )
    
            num_disk = GetNumActuatorDisks() # Should be 0
    
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_DISK )
    
            num_disk = GetNumActuatorDisks() # Should be 1
    
    
        See also: PROP_MODE
        :rtype: int
        :return: Number of actuator disks in the current VSPAERO set
        """
        return _vsp.GetNumActuatorDisks()
    
    @client_wrap
    def FindUnsteadyGroup(self, group_index):
        r"""
        Get the ID of the VSPAERO unsteady group at the specified index. An empty string is returned if
        the index is out of range.
    
    
        .. code-block:: python
    
            wing_id = AddGeom( "WING" )
            pod_id = AddGeom( "POD" )
    
            # Create an actuator disk
            prop_id = AddGeom( "PROP", "" )
            SetParmVal( prop_id, "PropMode", "Design", PROP_BLADES )
    
            Update()
    
            # Setup the unsteady group VSPAERO parms
            disk_id = FindUnsteadyGroup( 1 ) # fixed components are in group 0 (wing & pod)
    
            SetParmVal( FindParm( disk_id, "RPM", "UnsteadyGroup" ), 1234.0 )
    
    
        See also: PROP_MODE
        :param [in]: group_index Unsteady group index for the current VSPAERO set
        :rtype: string
        :return: Unsteady group ID
        """
        return _vsp.FindUnsteadyGroup(group_index)
    
    @client_wrap
    def GetUnsteadyGroupName(self, group_index):
        r"""
        Get the name of the unsteady group at the specified index.
    
    
        .. code-block:: python
    
            # Add a pod and wing
            pod_id = AddGeom( "POD", "" )
            wing_id = AddGeom( "WING", pod_id )
    
            SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
            Update()
    
            print( GetUnsteadyGroupName( 0 ) )
    
    
        See also: SetUnsteadyGroupName
        :param [in]: group_index Unsteady group index for the current VSPAERO set
        :rtype: string
        :return: Unsteady group name
        """
        return _vsp.GetUnsteadyGroupName(group_index)
    
    @client_wrap
    def GetUnsteadyGroupCompIDs(self, group_index):
        r"""
        Get an array of IDs for all components in the unsteady group at the specified index.
    
    
        .. code-block:: python
    
            # Add a pod and wing
            pod_id = AddGeom( "POD", "" )
            wing_id = AddGeom( "WING", pod_id ) # Default with symmetry on -> 2 surfaces
    
            SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
            Update()
    
            comp_ids = GetUnsteadyGroupCompIDs( 0 )
    
            if  len(comp_ids) != 3 :
                print( "ERROR: GetUnsteadyGroupCompIDs" )
    
    
        See also: GetUnsteadyGroupSurfIndexes
        :param [in]: group_index Unsteady group index for the current VSPAERO set
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of component IDs
        """
        return _vsp.GetUnsteadyGroupCompIDs(group_index)
    
    @client_wrap
    def GetUnsteadyGroupSurfIndexes(self, group_index):
        r"""
        Get an array of surface indexes for all components in the unsteady group at the specified index.
    
    
        .. code-block:: python
    
            # Add a pod and wing
            pod_id = AddGeom( "POD", "" )
            wing_id = AddGeom( "WING", pod_id ) # Default with symmetry on -> 2 surfaces
    
            SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
            Update()
    
            surf_indexes = GetUnsteadyGroupSurfIndexes( 0 )
    
            if  len(surf_indexes) != 3 :
                print( "ERROR: GetUnsteadyGroupSurfIndexes" )
    
    
        See also: GetUnsteadyGroupCompIDs
        :param [in]: group_index Unsteady group index for the current VSPAERO set
        :rtype: std::vector< int,std::allocator< int > >
        :return: Array of surface indexes
        """
        return _vsp.GetUnsteadyGroupSurfIndexes(group_index)
    
    @client_wrap
    def GetNumUnsteadyGroups(self, ):
        r"""
        Get the number of unsteady groups in the current VSPAERO set. Each propeller is placed in its own unsteady group. All symmetric copies
        of propellers are also placed in an unsteady group. All other component types are placed in a single fixed component unsteady group.
    
    
        .. code-block:: python
    
            # Set VSPAERO set index to SET_ALL
            SetParmVal( FindParm( FindContainer( "VSPAEROSettings", 0 ), "GeomSet", "VSPAERO" ), SET_ALL )
    
            # Add a propeller
            prop_id = AddGeom( "PROP" )
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_DISK )
    
            num_group = GetNumUnsteadyGroups() # Should be 0
    
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_BLADES )
    
            num_group = GetNumUnsteadyGroups() # Should be 1
    
            wing_id = AddGeom( "WING" )
    
            num_group = GetNumUnsteadyGroups() # Should be 2 (includes fixed component group)
    
    
        See also: PROP_MODE, GetNumUnsteadyRotorGroups
        :rtype: int
        :return: Number of unsteady groups in the current VSPAERO set
        """
        return _vsp.GetNumUnsteadyGroups()
    
    @client_wrap
    def GetNumUnsteadyRotorGroups(self, ):
        r"""
        Get the number of unsteady rotor groups in the current VSPAERO set. This is equivalent to the total number of propeller Geoms,
        including each symmetric copy, in the current VSPAERO set. While all fixed components (wings, fuseleage, etc.) are placed in
        their own unsteady group, this function does not consider them.
    
    
        .. code-block:: python
    
            # Set VSPAERO set index to SET_ALL
            SetParmVal( FindParm( FindContainer( "VSPAEROSettings", 0 ), "GeomSet", "VSPAERO" ), SET_ALL )
    
            # Add a propeller
            prop_id = AddGeom( "PROP" )
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_DISK )
    
            num_group = GetNumUnsteadyRotorGroups() # Should be 0
    
            SetParmValUpdate( prop_id, "PropMode", "Design", PROP_BLADES )
    
            num_group = GetNumUnsteadyRotorGroups() # Should be 1
    
            wing_id = AddGeom( "WING" )
    
            num_group = GetNumUnsteadyRotorGroups() # Should be 1 still (fixed group not included)
    
    
        See also: PROP_MODE, GetNumUnsteadyGroups
        :rtype: int
        :return: Number of unsteady rotor groups in the current VSPAERO set
        """
        return _vsp.GetNumUnsteadyRotorGroups()
    
    @client_wrap
    def AddExcrescence(self, excresName, excresType, excresVal):
        r"""
        Add an Excresence to the Parasite Drag Tool
    
    
        .. code-block:: python
    
            AddExcrescence( "Miscellaneous", EXCRESCENCE_COUNT, 8.5 )
    
            AddExcrescence( "Cowl Boattail", EXCRESCENCE_CD, 0.0003 )
    
    
        See also: EXCRES_TYPE
        :param [in]: excresName Name of the Excressence
        :param [in]: excresType Excressence type enum (i.e. EXCRESCENCE_PERCENT_GEOM)
        :param [in]: excresVal Excressence value
        """
        return _vsp.AddExcrescence(excresName, excresType, excresVal)
    
    @client_wrap
    def DeleteExcrescence(self, index):
        r"""
        Delete an Excresence from the Parasite Drag Tool
    
    
        .. code-block:: python
    
            AddExcrescence( "Miscellaneous", EXCRESCENCE_COUNT, 8.5 )
    
            AddExcrescence( "Cowl Boattail", EXCRESCENCE_CD, 0.0003 )
    
            AddExcrescence( "Percentage Example", EXCRESCENCE_PERCENT_GEOM, 5 )
    
            DeleteExcrescence( 2 ) # Last Index
    
    
        :param [in]: index int Index of the Excressence to delete
        """
        return _vsp.DeleteExcrescence(index)
    
    @client_wrap
    def UpdateParasiteDrag(self, ):
        r"""    Update any reference geometry, atmospheric properties, excressences, etc. in the Parasite Drag Tool"""
        return _vsp.UpdateParasiteDrag()
    
    @client_wrap
    def WriteAtmosphereCSVFile(self, file_name, atmos_type):
        r"""
        Calculate the atmospheric properties determined by a specified model for a preset array of altitudes ranging from 0 to 90000 m and
        write the results to a CSV output file
    
    
        .. code-block:: python
    
            print( "Starting USAF Atmosphere 1966 Table Creation. \n" )
    
            WriteAtmosphereCSVFile( "USAFAtmosphere1966Data.csv", ATMOS_TYPE_HERRINGTON_1966 )
    
    
        See also: ATMOS_TYPE
        :param [in]: file_name Output CSV file
        :param [in]: atmos_type Atmospheric model enum (i.e. ATMOS_TYPE_HERRINGTON_1966)
        """
        return _vsp.WriteAtmosphereCSVFile(file_name, atmos_type)
    
    @client_wrap
    def CalcAtmosphere(self, alt, delta_temp, atmos_type):
        r"""
        Calculate the atmospheric properties determined by a specified model at input altitude and temperature deviation. This function may
        not be used for any manual atmospheric model types (i.e. ATMOS_TYPE_MANUAL_P_T). This function assumes freestream units are metric,
        temperature units are Kelvin, and pressure units are kPA.
    
    
        .. code-block:: python
    
    
            alt = 4000
    
            delta_temp = 0
    
            temp, pres, pres_ratio, rho_ratio = CalcAtmosphere( alt, delta_temp, ATMOS_TYPE_US_STANDARD_1976)
    
    
        See also: ATMOS_TYPE
        :param [in]: alt Altitude
        :param [in]: delta_temp Deviation in temperature from the value specified in the atmospheric model
        :param [in]: atmos_type Atmospheric model enum (i.e. ATMOS_TYPE_HERRINGTON_1966)
        :param [out]: temp output Temperature
        :param [out]: pres output Pressure
        :param [out]: pres_ratio Output pressure ratio
        :param [out]: rho_ratio Output density ratio
        """
        return _vsp.CalcAtmosphere(alt, delta_temp, atmos_type)
    
    @client_wrap
    def WriteBodyFFCSVFile(self, file_name):
        r"""
        Calculate the form factor from each body FF equation (i.e. Hoerner Streamlined Body) and write the results to a CSV output file
    
    
        .. code-block:: python
    
            print( "Starting Body Form Factor Data Creation. \n" )
            WriteBodyFFCSVFile( "BodyFormFactorData.csv" )
    
    
        :param [in]: file_name Output CSV file
        """
        return _vsp.WriteBodyFFCSVFile(file_name)
    
    @client_wrap
    def WriteWingFFCSVFile(self, file_name):
        r"""
        Calculate the form factor from each wing FF equation (i.e. Schemensky 4 Series Airfoil) and write the results to a CSV output file
    
    
        .. code-block:: python
    
            print( "Starting Wing Form Factor Data Creation. \n" )
            WriteWingFFCSVFile( "WingFormFactorData.csv" )
    
    
        :param [in]: file_name Output CSV file
        """
        return _vsp.WriteWingFFCSVFile(file_name)
    
    @client_wrap
    def WriteCfEqnCSVFile(self, file_name):
        r"""
        Calculate the coefficient of friction from each Cf equation (i.e. Power Law Blasius) and write the results to a CSV output file
    
    
        .. code-block:: python
    
            print( "Starting Turbulent Friciton Coefficient Data Creation. \n" )
            WriteCfEqnCSVFile( "FrictionCoefficientData.csv" )
    
    
        :param [in]: file_name Output CSV file
        """
        return _vsp.WriteCfEqnCSVFile(file_name)
    
    @client_wrap
    def WritePartialCfMethodCSVFile(self, file_name):
        r"""
        Calculate the partial coefficient of friction and write the results to a CSV output file
    
    
        .. code-block:: python
    
            print( "Starting Partial Friction Method Data Creation. \n" )
            WritePartialCfMethodCSVFile( "PartialFrictionMethodData.csv" )
    
    
        :param [in]: file_name Output CSV file
        """
        return _vsp.WritePartialCfMethodCSVFile(file_name)
    
    @client_wrap
    def CompPnt01(self, geom_id, surf_indx, u, w):
        r"""
        Calculate the 3D coordinate equivalent for the input surface coordinate point
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            pnt = CompPnt01( geom_id, surf_indx, u, w )
    
            print( f"Point: ( {pnt.x()}, {pnt.y()}, {pnt.z()} )" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u U (0 - 1) surface coordinate
        :param [in]: w W (0 - 1) surface coordinate
        :rtype: :py:class:`vec3d`
        :return: Normal vector3D coordinate point
        """
        return _vsp.CompPnt01(geom_id, surf_indx, u, w)
    
    @client_wrap
    def CompNorm01(self, geom_id, surf_indx, u, w):
        r"""
        Calculate the normal vector on the specified surface at input surface coordinate
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            norm = CompNorm01( geom_id, surf_indx, u, w )
    
            print( "Point: ( {norm.x()}, {norm.y()}, {norm.z()} )" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u U (0 - 1) surface coordinate
        :param [in]: w W (0 - 1) surface coordinate
        :rtype: :py:class:`vec3d`
        :return: Normal vector
        """
        return _vsp.CompNorm01(geom_id, surf_indx, u, w)
    
    @client_wrap
    def CompTanU01(self, geom_id, surf_indx, u, w):
        r"""
        Calculate the vector tangent to the specified surface at input surface coordinate in the U direction
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            tanu = CompTanU01( geom_id, surf_indx, u, w )
    
            print( f"Point: ( {tanu.x()}, {tanu.y()}, {tanu.z()} )" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u U (0 - 1) surface coordinate
        :param [in]: w W (0 - 1) surface coordinate
        :rtype: :py:class:`vec3d`
        :return: Tangent vector in U direction
        """
        return _vsp.CompTanU01(geom_id, surf_indx, u, w)
    
    @client_wrap
    def CompTanW01(self, geom_id, surf_indx, u, w):
        r"""
        Calculate the vector tangent to the specified surface at input surface coordinate in the W direction
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            tanw = CompTanW01( geom_id, surf_indx, u, w )
    
            print( f"Point: ( {tanw.x()}, {tanw.y()}, {tanw.z()} )" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u U (0 - 1) surface coordinate
        :param [in]: w W (0 - 1) surface coordinate
        :rtype: :py:class:`vec3d`
        :return: Tangent vector in W direction
        """
        return _vsp.CompTanW01(geom_id, surf_indx, u, w)
    
    @client_wrap
    def CompCurvature01(self, geom_id, surf_indx, u, w):
        r"""
        Determine the curvature of a specified surface at the input surface coordinate point
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
    
            u = 0.25
            w = 0.75
    
            k1, k2, ka, kg = CompCurvature01( geom_id, surf_indx, u, w )
    
            print( f"Curvature : k1 {k1} k2 {k2} ka {ka} kg {kg}" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u double U (0 - 1) surface coordinate
        :param [in]: w double W (0 - 1) surface coordinate
        :param [out]: k1_out double Output value of maximum principal curvature
        :param [out]: k2_out double Output value of minimum principal curvature
        :param [out]: ka_out double Output value of mean curvature
        :param [out]: kg_out double Output value of Gaussian curvature
        """
        return _vsp.CompCurvature01(geom_id, surf_indx, u, w)
    
    @client_wrap
    def ProjPnt01(self, geom_id, surf_indx, pt):
        r"""
        Determine the nearest surface coordinate for an input 3D coordinate point and calculate the distance between the
        3D point and the closest point of the surface.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            pnt = CompPnt01( geom_id, surf_indx, u, w )
    
            norm = CompNorm01( geom_id, surf_indx, u, w )
    
    
            # Offset point from surface
            pnt.set_xyz( pnt.x() + norm.x(), pnt.y() + norm.y(), pnt.z() + norm.z() )
    
            d, uout, wout = ProjPnt01( geom_id, surf_indx, pnt )
    
            print( f"Dist {d} u {uout} w {wout}" )
    
    
        See also: ProjPnt01Guess, ProjPnt01I
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pt vec3d Input 3D coordinate point
        :param [out]: u_out double Output closest U (0 - 1) surface coordinate
        :param [out]: w_out double Output closest W (0 - 1) surface coordinate
        :rtype: float
        :return: double Distance between the 3D point and the closest point of the surface
        """
        return _vsp.ProjPnt01(geom_id, surf_indx, pt)
    
    @client_wrap
    def ProjPnt01I(self, geom_id, pt):
        r"""
        Determine the nearest surface coordinate and corresponding parent Geom main surface index for an input 3D coordinate point. Return the distance between
        the closest point and the input.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            d = 0
    
            pnt = CompPnt01( geom_id, surf_indx, u, w )
    
            norm = CompNorm01( geom_id, surf_indx, u, w )
    
    
    
            # Offset point from surface
            pnt.set_xyz( pnt.x() + norm.x(), pnt.y() + norm.y(), pnt.z() + norm.z() )
    
            d, surf_indx_out, uout, wout = ProjPnt01I( geom_id, pnt )
    
            print( f"Dist {d} u {uout} w {wout} surf_index {surf_indx_out}" )
    
    
        See also: ProjPnt01, ProjPnt01Guess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: pt vec3d Input 3D coordinate point
        :param [out]: surf_indx_out int Output main surface index from the parent Geom
        :param [out]: u_out double Output closest U (0 - 1) surface coordinat
        :param [out]: w_out double Output closest W (0 - 1) surface coordinat
        :rtype: float
        :return: double Distance between the 3D point and the closest point of the surface
        """
        return _vsp.ProjPnt01I(geom_id, pt)
    
    @client_wrap
    def ProjPnt01Guess(self, geom_id, surf_indx, pt, u0, w0):
        r"""
        Determine the nearest surface coordinate for an input 3D coordinate point and calculate the distance between the
        3D point and the closest point of the surface. This function takes an input surface coordinate guess for, offering
        a potential decrease in computation time compared to ProjPnt01.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            d = 0
    
            pnt = CompPnt01( geom_id, surf_indx, u, w )
    
            norm = CompNorm01( geom_id, surf_indx, u, w )
    
    
            # Offset point from surface
            pnt.set_xyz( pnt.x() + norm.x(), pnt.y() + norm.y(), pnt.z() + norm.z() )
    
            d, uout, wout = ProjPnt01Guess( geom_id, surf_indx, pnt, u + 0.1, w + 0.1 )
    
            print( f"Dist {d} u {uout} w {wout}" )
    
    
        See also: ProjPnt01, ProjPnt01I
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pt vec3d Input 3D coordinate point
        :param [in]: u0 double Input U (0 - 1) surface coordinate guess
        :param [in]: w0 double Input W (0 - 1) surface coordinate guess
        :param [out]: u_out double Output closest U (0 - 1) surface coordinate
        :param [out]: w_out double Output closest W (0 - 1) surface coordinate
        :rtype: float
        :return: double Distance between the 3D point and the closest point of the surface
        """
        return _vsp.ProjPnt01Guess(geom_id, surf_indx, pt, u0, w0)
    
    @client_wrap
    def AxisProjPnt01(self, geom_id, surf_indx, iaxis, pt):
        r"""
        Project an input 3D coordinate point onto a surface along a specified axis.  If the axis-aligned ray from the point intersects the surface multiple times, the nearest intersection is returned.  If the axis-aligned ray from the point does not intersect the surface, the original point is returned and -1 is returned in the other output parameters.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            surf_pt = CompPnt01( geom_id, surf_indx, u, w )
            pt = surf_pt
    
            pt.offset_y( -5.0 )
    
            idist, u_out, w_out = AxisProjPnt01( geom_id, surf_indx, Y_DIR, pt )
    
            print( f"iDist {idist} u_out {u_out} w_out {w_out}" )
            print( "3D Offset ", False)
    
    
        See also: AxisProjPnt01Guess, AxisProjPnt01I, AxisProjVecPnt01, AxisProjVecPnt01Guess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: iaxis int Axis direction to project point along (X_DIR, Y_DIR, or Z_DIR)
        :param [in]: pt Input 3D coordinate point
        :param [out]: u_out Output closest U (0 - 1) surface coordinate
        :param [out]: w_out Output closest W (0 - 1) surface coordinate
        :rtype: float
        :return: Axis aligned distance between the 3D point and the projected point on the surface
        """
        return _vsp.AxisProjPnt01(geom_id, surf_indx, iaxis, pt)
    
    @client_wrap
    def AxisProjPnt01I(self, geom_id, iaxis, pt):
        r"""
        Project an input 3D coordinate point onto a Geom along a specified axis.  The intersecting surface index is also returned.  If the axis-aligned ray from the point intersects the Geom multiple times, the nearest intersection is returned.  If the axis-aligned ray from the point does not intersect the Geom, the original point is returned and -1 is returned in the other output parameters.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
            surf_pt = CompPnt01( geom_id, surf_indx, u, w )
            pt = surf_pt
    
            pt.offset_y( -5.0 )
    
    
            idist, surf_indx_out, u_out, w_out = AxisProjPnt01I( geom_id, Y_DIR, pt )
    
            print( "iDist {idist} u_out {u_out} w_out {w_out} surf_index {surf_indx_out}" )
            print( "3D Offset ", False)
    
    
        See also: AxisProjPnt01, AxisProjPnt01Guess, AxisProjVecPnt01, AxisProjVecPnt01Guess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: iaxis int Axis direction to project point along (X_DIR, Y_DIR, or Z_DIR)
        :param [in]: pt Input 3D coordinate point
        :param [out]: surf_indx_out Output main surface index from the parent Geom
        :param [out]: u_out Output closest U (0 - 1) surface coordinate
        :param [out]: w_out Output closest W (0 - 1) surface coordinate
        :rtype: float
        :return: Axis aligned distance between the 3D point and the projected point on the surface
        """
        return _vsp.AxisProjPnt01I(geom_id, iaxis, pt)
    
    @client_wrap
    def AxisProjPnt01Guess(self, geom_id, surf_indx, iaxis, pt, u0, w0):
        r"""
        Project an input 3D coordinate point onto a surface along a specified axis given an initial guess of surface parameter.  If the axis-aligned ray from the point intersects the surface multiple times, the nearest intersection is returned.  If the axis-aligned ray from the point does not intersect the surface, the original point is returned and -1 is returned in the other output parameters.  The surface parameter guess should allow this call to be faster than calling AxisProjPnt01 without a guess.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            u = 0.12345
            w = 0.67890
    
    
    
            surf_pt = CompPnt01( geom_id, surf_indx, u, w )
            pt = surf_pt
    
            pt.offset_y( -5.0 )
    
            # Construct initial guesses near actual parameters
            u0 = u + 0.01234
            w0 = w - 0.05678
    
            d, uout, wout = AxisProjPnt01Guess( geom_id, surf_indx, Y_DIR, pt, u0, w0 )
    
            print( f"Dist {d} u {uout} w {wout}" )
    
    
        See also: AxisProjPnt01, AxisProjPnt01I, AxisProjVecPnt01, AxisProjVecPnt01Guess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: iaxis int Axis direction to project point along (X_DIR, Y_DIR, or Z_DIR)
        :param [in]: pt Input 3D coordinate point
        :param [in]: u0 Input U (0 - 1) surface coordinate guess
        :param [in]: w0 Input W (0 - 1) surface coordinate guess
        :param [out]: u_out Output closest U (0 - 1) surface coordinate
        :param [out]: w_out Output closest W (0 - 1) surface coordinate
        :rtype: float
        :return: Distance between the 3D point and the closest point of the surface
        """
        return _vsp.AxisProjPnt01Guess(geom_id, surf_indx, iaxis, pt, u0, w0)
    
    @client_wrap
    def InsideSurf(self, geom_id, surf_indx, pt):
        r"""
        Test whether a given point is inside a specified surface.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
            s = 0.68
            t = 0.56
    
            pnt = CompPntRST( geom_id, surf_indx, r, s, t )
    
            res = InsideSurf( geom_id, surf_indx, pnt )
    
            if  res :
                print( "Inside" )
            else:
                print( "Outside" )
    
    
    
        See also: VecInsideSurf
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pt Input 3D coordinate point
        :rtype: boolean
        :return: Boolean true if the point is inside the surface, false otherwise.
        """
        return _vsp.InsideSurf(geom_id, surf_indx, pt)
    
    @client_wrap
    def CompPntRST(self, geom_id, surf_indx, r, s, t):
        r"""
        Calculate the (X, Y, Z) coordinate for the input volume (R, S, T) coordinate point
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
            s = 0.68
            t = 0.56
    
            pnt = CompPntRST( geom_id, surf_indx, r, s, t )
    
            print( f"Point: ( {pnt.x()}, {pnt.y()}, {pnt.z()} )" )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: r R (0 - 1) volume coordinate
        :param [in]: s S (0 - 1) volume coordinate
        :param [in]: t T (0 - 1) volume coordinate
        :rtype: :py:class:`vec3d`
        :return: vec3d coordinate point
        """
        return _vsp.CompPntRST(geom_id, surf_indx, r, s, t)
    
    @client_wrap
    def FindRST(self, geom_id, surf_indx, pt):
        r"""
        Determine the nearest (R, S, T) volume coordinate for an input (X, Y, Z) 3D coordinate point and calculate the distance between the
        3D point and the found volume point.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
            s = 0.68
            t = 0.56
    
            pnt = CompPntRST( geom_id, surf_indx, r, s, t )
    
    
            d, rout, sout, tout = FindRST( geom_id, surf_indx, pnt )
    
            print( f"Dist {d} r {rout} s {sout} t {tout}" )
    
    
        See also: FindRSTGuess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pt vec3d Input 3D coordinate point
        :param [out]: r_out double Output closest R (0 - 1.0) volume coordinate
        :param [out]: s_out double Output closest S (0 - 1.0) volume coordinate
        :param [out]: t_out double Output closest T (0 - 1.0) volume coordinate
        :rtype: float
        :return: double Distance between the 3D point and the closest point of the volume
        """
        return _vsp.FindRST(geom_id, surf_indx, pt)
    
    @client_wrap
    def FindRSTGuess(self, geom_id, surf_indx, pt, r0, s0, t0):
        r"""
        Determine the nearest (R, S, T) volume coordinate for an input (X, Y, Z) 3D coordinate point given an initial guess of volume coordinates.  Also calculate the distance between the
        3D point and the found volume point.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
            s = 0.68
            t = 0.56
    
            pnt = CompPntRST( geom_id, surf_indx, r, s, t )
    
    
            r0 = 0.1
            s0 = 0.6
            t0 = 0.5
    
            d, rout, sout, tout = FindRSTGuess( geom_id, surf_indx, pnt, r0, s0, t0 )
    
            print( f"Dist {d} r {rout} s {sout} t {tout}" )
    
    
        See also: FindRST
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pt vec3d Input 3D coordinate point
        :param [in]: r0 double Input R (0 - 1.0) volume coordinate guess
        :param [in]: s0 double Input S (0 - 1.0) volume coordinate guess
        :param [in]: t0 double Input T (0 - 1.0) volume coordinate guess
        :param [out]: r_out double Output closest R (0 - 1.0) volume coordinate
        :param [out]: s_out double Output closest S (0 - 1.0) volume coordinate
        :param [out]: t_out double Output closest T (0 - 1.0) volume coordinate
        :rtype: float
        :return: double Distance between the 3D point and the closest point of the volume
        """
        return _vsp.FindRSTGuess(geom_id, surf_indx, pt, r0, s0, t0)
    
    @client_wrap
    def ConvertRSTtoLMN(self, geom_id, surf_indx, r, s, t):
        r"""
        Convert RST volumetric coordinates to LMN coordinates.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
            s = 0.68
            t = 0.56
    
            l_out, m_out, n_out = ConvertRSTtoLMN( geom_id, surf_indx, r, s, t )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: r R (0 - 1) volume coordinate
        :param [in]: s S (0 - 1) volume coordinate
        :param [in]: t T (0 - 1) volume coordinate
        :param [out]: l_out L (0 - 1) linear volume coordinate
        :param [out]: m_out M (0 - 1) linear volume coordinate
        :param [out]: n_out N (0 - 1) linear volume coordinate
        """
        return _vsp.ConvertRSTtoLMN(geom_id, surf_indx, r, s, t)
    
    @client_wrap
    def ConvertRtoL(self, geom_id, surf_indx, r):
        r"""
        Convert R volumetric coordinate to L coordinate.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            r = 0.12
    
            l_out = ConvertRtoL( geom_id, surf_indx, r )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: r R (0 - 1) volume coordinate
        :param [out]: l_out L (0 - 1) linear volume coordinate
        """
        return _vsp.ConvertRtoL(geom_id, surf_indx, r)
    
    @client_wrap
    def ConvertLMNtoRST(self, geom_id, surf_indx, l, m, n):
        r"""
        Convert LMN volumetric coordinates to RST coordinates.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            l = 0.12
            m = 0.34
            n = 0.56
    
            r_out, s_out, t_out = ConvertLMNtoRST( geom_id, surf_indx, l, m, n )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: l L (0 - 1) linear volume coordinate
        :param [in]: m M (0 - 1) linear volume coordinate
        :param [in]: n N (0 - 1) linear volume coordinate
        :param [out]: r_out R (0 - 1) volume coordinate
        :param [out]: s_out S (0 - 1) volume coordinate
        :param [out]: t_out T (0 - 1) volume coordinate
        """
        return _vsp.ConvertLMNtoRST(geom_id, surf_indx, l, m, n)
    
    @client_wrap
    def ConvertLtoR(self, geom_id, surf_indx, l):
        r"""
        Convert L volumetric coordinate to R coordinate.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            l = 0.12
    
            r_out = ConvertLtoR( geom_id, surf_indx, l )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: l L (0 - 1) volume coordinate
        :param [out]: r_out R (0 - 1) linear volume coordinate
        """
        return _vsp.ConvertLtoR(geom_id, surf_indx, l)
    
    @client_wrap
    def ConvertUtoEta(self, geom_id, u):
        r"""
        Convert U coordinate to eta wing coordinate.
    
    
        .. code-block:: python
    
            # Add Wing Geom
            geom_id = AddGeom( "WING", "" )
    
            surf_indx = 0
    
            u = 0.25
    
            eta_out = ConvertUtoEta( geom_id, u )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: u U (0 - 1) surface coordinate
        :param [out]: eta_out Eta (0 - 1) wing spanwise coordinate
        """
        return _vsp.ConvertUtoEta(geom_id, u)
    
    @client_wrap
    def ConvertEtatoU(self, geom_id, eta):
        r"""
        Convert eta wing coordinate to u coordinate.
    
    
        .. code-block:: python
    
            # Add Wing Geom
            geom_id = AddGeom( "WING", "" )
    
            surf_indx = 0
    
            eta= 0.25
    
            u = ConvertEtatoU( geom_id, eta )
    
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: eta Eta (0 - 1) wing spanwise coordinate
        :param [out]: u_out U (0 - 1) surface coordinate
        """
        return _vsp.ConvertEtatoU(geom_id, eta)
    
    @client_wrap
    def CompVecPnt01(self, geom_id, surf_indx, u_in_vec, w_in_vec):
        r"""
        Determine 3D coordinate for each surface coordinate point in the input arrays
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecPnt01( geom_id, 0, uvec, wvec )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: u_in_vec vector<double> Input vector of U (0 - 1) surface coordinates
        :param [in]: w_in_vec vector<double> Input vector of W (0 - 1) surface coordinates
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of 3D coordinate points
        """
        return _vsp.CompVecPnt01(geom_id, surf_indx, u_in_vec, w_in_vec)
    
    @client_wrap
    def CompVecDegenPnt01(self, geom_id, surf_indx, degen_type, u_in_vec, w_in_vec):
        r"""
        Determine 3D coordinate for each degen surface coordinate point in the input arrays
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecDegenPnt01( geom_id, 0, 0, uvec, wvec )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: degen_type int Type of degen surface (0-S, 1-V, 2-H, 3-C)
        :param [in]: u_in_vec vector<double> Input vector of U (0 - 1) surface coordinates
        :param [in]: w_in_vec vector<double> Input vector of W (0 - 1) surface coordinates
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of 3D coordinate points
        """
        return _vsp.CompVecDegenPnt01(geom_id, surf_indx, degen_type, u_in_vec, w_in_vec)
    
    @client_wrap
    def CompVecNorm01(self, geom_id, surf_indx, us, ws):
        r"""
        Determine the normal vector on a surface for each surface coordinate point in the input arrays
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            normvec = CompVecNorm01( geom_id, 0, uvec, wvec )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: us vector<double> Input vector of U (0 - 1) surface coordinates
        :param [in]: ws vector<double> Input vector of W (0 - 1) surface coordinates
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of 3D normal vectors
        """
        return _vsp.CompVecNorm01(geom_id, surf_indx, us, ws)
    
    @client_wrap
    def CompVecCurvature01(self, geom_id, surf_indx, us, ws):
        r"""
        Determine the curvature of a specified surface at each surface coordinate point in the input arrays
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
    
    
            k1vec, k2vec, kavec, kgvec = CompVecCurvature01( geom_id, 0, uvec, wvec )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: us vector<double> Input vector of U (0 - 1) surface coordinates
        :param [in]: ws vector<double> Input vector of W (0 - 1) surface coordinates
        :param [out]: k1_out_vec vector<double> Output vector of maximum principal curvatures
        :param [out]: k2_out_vec vector<double> Output vector of minimum principal curvatures
        :param [out]: ka_out_vec vector<double> Output vector of mean curvatures
        :param [out]: kg_out_vec vector<double> Output vector of Gaussian curvatures
        """
        return _vsp.CompVecCurvature01(geom_id, surf_indx, us, ws)
    
    @client_wrap
    def ProjVecPnt01(self, geom_id, surf_indx, pts):
        r"""
        Determine the nearest surface coordinates for an input array of 3D coordinate points and calculate the distance between each
        3D point and the closest point of the surface.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecPnt01( geom_id, 0, uvec, wvec )
    
            normvec = CompVecNorm01( geom_id, 0, uvec, wvec )
    
            for i in range(n):
    
                ptvec[i].set_xyz( ptvec[i].x() + normvec[i].x(), ptvec[i].y() + normvec[i].y(), ptvec[i].z() + normvec[i].z() )
    
            uoutv, woutv, doutv = ProjVecPnt01( geom_id, 0, ptvec )
    
    
        See also: ProjVecPnt01Guess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [out]: u_out_vec vector<double> Output vector of the closest U (0 - 1) surface coordinate for each 3D input point
        :param [out]: w_out_vec vector<double> Output vector of the closest W (0 - 1) surface coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output vector of distances for each 3D point and the closest point of the surface
        """
        return _vsp.ProjVecPnt01(geom_id, surf_indx, pts)
    
    @client_wrap
    def ProjVecPnt01Guess(self, geom_id, surf_indx, pts, u0s, w0s):
        r"""
        Determine the nearest surface coordinates for an input array of 3D coordinate points and calculate the distance between each
        3D point and the closest point of the surface. This function takes an input array of surface coordinate guesses for each 3D
        coordinate, offering a potential decrease in computation time compared to ProjVecPnt01.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecPnt01( geom_id, 0, uvec, wvec )
    
            normvec = CompVecNorm01( geom_id, 0, uvec, wvec )
    
            for i in range(n):
    
                ptvec[i].set_xyz( ptvec[i].x() + normvec[i].x(), ptvec[i].y() + normvec[i].y(), ptvec[i].z() + normvec[i].z() )
    
            u0v = [0]*n
            w0v = [0]*n
    
            for i in range(n):
    
                u0v[i] = uvec[i] + 0.01234
    
                w0v[i] = wvec[i] - 0.05678
    
            uoutv, woutv, doutv = ProjVecPnt01Guess( geom_id, 0, ptvec, u0v,  w0v )
    
    
        See also: ProjVecPnt01,
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [in]: u0s vector<double> Input vector of U (0 - 1) surface coordinate guesses
        :param [in]: w0s vector<double> Input vector of W (0 - 1) surface coordinate guesses
        :param [out]: u_out_vec vector<double> Output vector of the closest U (0 - 1) surface coordinate for each 3D input point
        :param [out]: w_out_vec vector<double> Output vector of the closest W (0 - 1) surface coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output array of distances for each 3D point and the closest point of the surface
        """
        return _vsp.ProjVecPnt01Guess(geom_id, surf_indx, pts, u0s, w0s)
    
    @client_wrap
    def AxisProjVecPnt01(self, geom_id, surf_indx, iaxis, pts):
        r"""
        Project an input array of 3D coordinate points onto a surface along a specified axis.  If the axis-aligned ray from the point intersects the surface multiple times, the nearest intersection is returned.  If the axis-aligned ray from the point does not intersect the surface, the original point is returned and -1 is returned in the other output parameters.
    
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
            surf_indx = 0
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecPnt01( geom_id, surf_indx, uvec, wvec )
    
            for i in range(n):
    
                ptvec[i].offset_y( -5.0 )
    
            uoutv, woutv, doutv = AxisProjVecPnt01( geom_id, surf_indx, Y_DIR, ptvec )
    
            # Some of these outputs are expected to be non-zero because the projected point is on the opposite side of
            # the pod from the originally computed point.  I.e. there were multiple solutions and the original point
            # is not the closest intersection point.  We could offset those points in the +Y direction instead of -Y.
            for i in range(n):
    
                print( i, False )
                print( "U delta ", False )
                print( uvec[i] - uoutv[i], False )
                print( "W delta ", False )
                print( wvec[i] - woutv[i] )
    
    
    
        See also: AxisProjPnt01, AxisProjPnt01Guess, AxisProjPnt01I, AxisProjVecPnt01Guess
        :param [in]: geom_id string Geom ID
        :param [in]: surf_indx int Main surface index from the Geom
        :param [in]: iaxis int Axis direction to project point along (X_DIR, Y_DIR, or Z_DIR)
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [out]: u_out_vec vector<double> Output vector of the closest U (0 - 1) surface coordinate for each 3D input point
        :param [out]: w_out_vec vector<double> Output vector of the closest W (0 - 1) surface coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output vector of axis distances for each 3D point and the projected point of the surface
        """
        return _vsp.AxisProjVecPnt01(geom_id, surf_indx, iaxis, pts)
    
    @client_wrap
    def AxisProjVecPnt01Guess(self, geom_id, surf_indx, iaxis, pts, u0s, w0s):
        r"""
        Project an input array of 3D coordinate points onto a surface along a specified axis given initial guess arrays of surface parameter.  If the axis-aligned ray from the point intersects the surface multiple times, the nearest intersection is returned.  If the axis-aligned ray from the point does not intersect the surface, the original point is returned and -1 is returned in the other output parameters.  The surface parameter guess should allow this call to be faster than calling AxisProjVecPnt01 without a guess.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
            surf_indx = 0
    
            n = 5
    
            uvec = [0]*n
            wvec = [0]*n
    
            for i in range(n):
    
                uvec[i] = (i+1)*1.0/(n+1)
    
                wvec[i] = (n-i)*1.0/(n+1)
    
            ptvec = CompVecPnt01( geom_id, surf_indx, uvec, wvec )
    
            for i in range(n):
    
                ptvec[i].offset_y( -5.0 )
    
            u0v = [0]*n
            w0v = [0]*n
    
            for i in range(n):
    
                u0v[i] = uvec[i] + 0.01234
                w0v[i] = wvec[i] - 0.05678
    
            uoutv, woutv, doutv = AxisProjVecPnt01Guess( geom_id, surf_indx, Y_DIR, ptvec, u0v,  w0v )
    
            for i in range(n):
    
                print( i, False )
                print( "U delta ", False )
                print( uvec[i] - uoutv[i], False )
                print( "W delta ", False )
                print( wvec[i] - woutv[i] )
    
    
    
        See also: AxisProjPnt01, AxisProjPnt01Guess, AxisProjPnt01I, AxisProjVecPnt01
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: iaxis int Axis direction to project point along (X_DIR, Y_DIR, or Z_DIR)
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [in]: u0s vector<double> Input vector of U (0 - 1) surface coordinate guesses
        :param [in]: w0s vector<double> Input vector of W (0 - 1) surface coordinate guesses
        :param [out]: u_out_vec vector<double> Output vector of the closest U (0 - 1) surface coordinate for each 3D input point
        :param [out]: w_out_vec vector<double> Output vector of the closest W (0 - 1) surface coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output vector of axis distances for each 3D point and the projected point of the surface
        """
        return _vsp.AxisProjVecPnt01Guess(geom_id, surf_indx, iaxis, pts, u0s, w0s)
    
    @client_wrap
    def VecInsideSurf(self, geom_id, surf_indx, pts):
        r"""
        Test whether a vector of points are inside a specified surface.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            n = 5
    
            rvec = [0]*n
            svec = [0]*n
            tvec = [0]*n
    
            for i in range(n):
    
                rvec[i] = (i+1)*1.0/(n+1)
    
                svec[i] = (n-i)*1.0/(n+1)
    
                tvec[i] = (i+1)*1.0/(n+1)
    
            ptvec = CompVecPntRST( geom_id, 0, rvec, svec, tvec )
    
    
            res = VecInsideSurf( geom_id, surf_indx, ptvec )
    
    
    
        See also: VecInsideSurf
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :rtype: std::vector< bool,std::allocator< bool > >
        :return: Boolean vector for each point.  True if it is inside the surface, false otherwise.
        """
        return _vsp.VecInsideSurf(geom_id, surf_indx, pts)
    
    @client_wrap
    def CompVecPntRST(self, geom_id, surf_indx, r_in_vec, s_in_vec, t_in_vec):
        r"""
        Determine 3D coordinate for each volume coordinate point in the input arrays
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            rvec = [0]*n
            svec = [0]*n
            tvec = [0]*n
    
            for i in range(n):
    
                rvec[i] = (i+1)*1.0/(n+1)
    
                svec[i] = (n-i)*1.0/(n+1)
    
                tvec[i] = (i+1)*1.0/(n+1)
    
            ptvec = CompVecPntRST( geom_id, 0, rvec, svec, tvec )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: r_in_vec vector<double> Input vector of R (0 - 1.0) volume coordinates
        :param [in]: s_in_vec vector<double> Input vector of S (0 - 1.0) volume coordinates
        :param [in]: t_in_vec vector<double> Input vector of T (0 - 1.0) volume coordinates
        :rtype: std::vector< vec3d,std::allocator< vec3d > >
        :return: vector<vec3d> Vector of 3D coordinate points
        """
        return _vsp.CompVecPntRST(geom_id, surf_indx, r_in_vec, s_in_vec, t_in_vec)
    
    @client_wrap
    def FindRSTVec(self, geom_id, surf_indx, pts):
        r"""
        Determine the nearest volume coordinates for an input array of 3D coordinate points and calculate the distance between each
        3D point and the found point in the volume.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            rvec = [0]*n
            svec = [0]*n
            tvec = [0]*n
    
            for i in range(n):
    
                rvec[i] = (i+1)*1.0/(n+1)
    
                svec[i] = (n-i)*1.0/(n+1)
    
                tvec[i] = (i+1)*1.0/(n+1)
    
            ptvec = CompVecPntRST( geom_id, 0, rvec, svec, tvec )
    
    
    
            routv, soutv, toutv, doutv = FindRSTVec( geom_id, 0, ptvec )
    
    
        See also: FindRSTVecGuess
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [out]: r_out_vec vector<double> Output vector of the closest R (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: s_out_vec vector<double> Output vector of the closest S (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: t_out_vec vector<double> Output vector of the closest T (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output vector of distances for each 3D point and the closest point of the volume
        """
        return _vsp.FindRSTVec(geom_id, surf_indx, pts)
    
    @client_wrap
    def FindRSTVecGuess(self, geom_id, surf_indx, pts, r0s, s0s, t0s):
        r"""
        Determine the nearest volume coordinates for an input array of 3D coordinate points and calculate the distance between each
        3D point and the closest point of the volume. This function takes an input array of volume coordinate guesses for each 3D
        coordinate, offering a potential decrease in computation time compared to FindRSTVec.
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            rvec = [0]*n
            svec = [0]*n
            tvec = [0]*n
    
            for i in range(n):
    
                rvec[i] = (i+1)*1.0/(n+1)
    
                svec[i] = (n-i)*1.0/(n+1)
    
                tvec[i] = (i+1)*1.0/(n+1)
    
            ptvec = CompVecPntRST( geom_id, 0, rvec, svec, tvec )
    
            for i in range(n):
    
                ptvec[i].set_xyz(ptvec[i].x() * 0.9, ptvec[i].y() * 0.9, ptvec[i].z() * 0.9)
    
             routv, soutv, toutv, doutv = FindRSTVecGuess( geom_id, 0, ptvec, rvec, svec, tvec )
    
    
        See also: FindRSTVec,
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: pts vector<vec3d> Input vector of 3D coordinate points
        :param [in]: r0s vector<double> Input vector of U (0 - 1.0) volume coordinate guesses
        :param [in]: s0s vector<double> Input vector of S (0 - 1.0) volume coordinate guesses
        :param [in]: t0s vector<double> Input vector of T (0 - 1.0) volume coordinate guesses
        :param [out]: r_out_vec vector<double> Output vector of the closest R (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: s_out_vec vector<double> Output vector of the closest S (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: t_out_vec vector<double> Output vector of the closest T (0 - 1.0) volume coordinate for each 3D input point
        :param [out]: d_out_vec vector<double> Output vector of distances for each 3D point and the closest point of the volume
        """
        return _vsp.FindRSTVecGuess(geom_id, surf_indx, pts, r0s, s0s, t0s)
    
    @client_wrap
    def ConvertRSTtoLMNVec(self, geom_id, surf_indx, r_vec, s_vec, t_vec):
        r"""
        Convert vector of RST volumetric coordinates to LMN coordinates.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            rvec = [0]*n
            svec = [0]*n
            tvec = [0]*n
    
            for i in range(n):
    
                rvec[i] = (i+1)*1.0/(n+1)
                svec[i] = (n-i)*1.0/(n+1)
                tvec[i] = (i+1)*1.0/(n+1)
    
    
    
            lvec, mvec, nvec = ConvertRSTtoLMNVec( geom_id, 0, rvec, svec, tvec )
    
    
    
        See also: ConvertLMNtoRSTVec, ConvertRSTtoLMN, ConvertLMNtoRST
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: r_vec vector<double> Input vector of R (0 - 1) volumetric coordinate
        :param [in]: s_vec vector<double> Input vector of S (0 - 1) volumetric coordinate
        :param [in]: t_vec vector<double> Input vector of T (0 - 1) volumetric coordinate
        :param [out]: l_out_vec vector<double> Output vector of L (0 - 1) linear volumetric coordinate
        :param [out]: m_out_vec vector<double> Output vector of M (0 - 1) linear volumetric coordinate
        :param [out]: n_out_vec vector<double> Output vector of N (0 - 1) linear volumetric coordinate
        """
        return _vsp.ConvertRSTtoLMNVec(geom_id, surf_indx, r_vec, s_vec, t_vec)
    
    @client_wrap
    def ConvertLMNtoRSTVec(self, geom_id, surf_indx, l_vec, m_vec, n_vec):
        r"""
        Convert vector of LMN volumetric coordinates to RST coordinates.
    
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            n = 5
    
            lvec = [0]*n
            mvec = [0]*n
            nvec = [0]*n
    
            for i in range(n):
    
                lvec[i] = (i+1)*1.0/(n+1)
                mvec[i] = (n-i)*1.0/(n+1)
                nvec[i] = (i+1)*1.0/(n+1)
    
            rvec, svec, tvec = ConvertLMNtoRSTVec( geom_id, 0, lvec, mvec, nvec )
    
    
    
        See also: ConvertRSTtoLMNVec, ConvertRSTtoLMN, ConvertLMNtoRST
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [in]: l_vec vector<double> Input vector of L (0 - 1) linear volumetric coordinate
        :param [in]: m_vec vector<double> Input vector of M (0 - 1) linear volumetric coordinate
        :param [in]: n_vec vector<double> Input vector of N (0 - 1) linear volumetric coordinate
        :param [out]: r_out_vec vector<double> Output vector of R (0 - 1) volumetric coordinate
        :param [out]: s_out_vec vector<double> Output vector of S (0 - 1) volumetric coordinate
        :param [out]: t_out_vec vector<double> Output vector of T (0 - 1) volumetric coordinate
    
        """
        return _vsp.ConvertLMNtoRSTVec(geom_id, surf_indx, l_vec, m_vec, n_vec)
    
    @client_wrap
    def GetUWTess01(self, geom_id, surf_indx):
        r"""
        Get the surface coordinate point of each intersection of the tessellated wireframe for a particular surface
    
    
        .. code-block:: python
    
            # Add Pod Geom
            geom_id = AddGeom( "POD", "" )
    
            surf_indx = 0
    
            utess, wtess = GetUWTess01( geom_id, surf_indx )
    
    
        :param [in]: geom_id string Parent Geom ID
        :param [in]: surf_indx int Main surface index from the parent Geom
        :param [out]: u_out_vec vector<double> Output vector of U (0 - 1) surface coordinates
        :param [out]: w_out_vec vector<double> Output vector of W (0 - 1) surface coordinates
        """
        return _vsp.GetUWTess01(geom_id, surf_indx)
    
    @client_wrap
    def AddRuler(self, startgeomid, startsurfindx, startu, startw, endgeomid, endsurfindx, endu, endw, name):
        r"""
        Create a new Ruler and add it to the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            pid2 = AddGeom( "POD", "" )
    
            SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )
    
            rid = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )
    
            SetParmVal( FindParm( rid, "X_Offset", "Measure" ), 6.0 )
    
    
        :param [in]: startgeomid string Start parent Geom ID
        :param [in]: startsurfindx int Main surface index from the staring parent Geom
        :param [in]: startu double Surface u (0 - 1) start coordinate
        :param [in]: startw double Surface w (0 - 1) start coordinate
        :param [in]: endgeomid string End parent Geom ID
        :param [in]: endsurfindx int Main surface index on the end parent Geom
        :param [in]: endu double Surface u (0 - 1) end coordinate
        :param [in]: endw double Surface w (0 - 1) end coordinate
        :param [in]: name string Ruler name
        :rtype: string
        :return: string Ruler ID
        """
        return _vsp.AddRuler(startgeomid, startsurfindx, startu, startw, endgeomid, endsurfindx, endu, endw, name)
    
    @client_wrap
    def GetAllRulers(self, ):
        r"""
        Get an array of all Ruler IDs from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            pid2 = AddGeom( "POD", "" )
    
            SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )
    
            rid1 = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )
    
            rid2 = AddRuler( pid1, 0, 0.4, 0.6, pid1, 1, 0.8, 0.9, "Ruler 2" )
    
            ruler_array = GetAllRulers()
    
            print("Two Rulers")
    
            for n in range(len(ruler_array)):
    
                print( ruler_array[n] )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: vector<string> Vector of Ruler IDs
        """
        return _vsp.GetAllRulers()
    
    @client_wrap
    def DelRuler(self, id):
        r"""
        Delete a particular Ruler from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            pid2 = AddGeom( "POD", "" )
    
            SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )
    
            rid1 = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )
    
            rid2 = AddRuler( pid1, 0, 0.4, 0.6, pid1, 1, 0.8, 0.9, "Ruler 2" )
    
            ruler_array = GetAllRulers()
    
            DelRuler( ruler_array[0] )
    
    
        :param [in]: id string Ruler ID
        """
        return _vsp.DelRuler(id)
    
    @client_wrap
    def DeleteAllRulers(self, ):
        r"""
        Delete all Rulers from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            pid2 = AddGeom( "POD", "" )
    
            SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )
    
            rid1 = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )
    
            rid2 = AddRuler( pid1, 0, 0.4, 0.6, pid1, 1, 0.8, 0.9, "Ruler 2" )
    
            DeleteAllRulers()
    
    
        """
        return _vsp.DeleteAllRulers()
    
    @client_wrap
    def AddProbe(self, geomid, surfindx, u, w, name):
        r"""
        Create a new Probe and add it to the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            probe_id = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
    
            SetParmVal( FindParm( probe_id, "Len", "Measure" ), 3.0 )
    
    
        :param [in]: geomid string Parent Geom ID
        :param [in]: surfindx int Main surface index from the parent Geom
        :param [in]: u double Surface u (0 - 1) coordinate
        :param [in]: w double Surface w (0 - 1) coordinate
        :param [in]: name string Probe name
        :rtype: string
        :return: string Probe ID
        """
        return _vsp.AddProbe(geomid, surfindx, u, w, name)
    
    @client_wrap
    def GetAllProbes(self, ):
        r"""
        Get an array of all Probe IDs from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            probe_id = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
    
            probe_array = GetAllProbes()
    
            print( "One Probe: ", False )
    
            print( probe_array[0] )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: [in] Array of Probe IDs
        """
        return _vsp.GetAllProbes()
    
    @client_wrap
    def DelProbe(self, id):
        r"""
        Delete a specific Probe from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            probe_id_1 = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
            probe_id_2 = AddProbe( pid1, 0, 0.2, 0.3, "Probe 2" )
    
            DelProbe( probe_id_1 )
    
            probe_array = GetAllProbes()
    
            if  len(probe_array) != 1 : print( "Error: DelProbe" )
    
    
        :param [in]: id Probe ID
        """
        return _vsp.DelProbe(id)
    
    @client_wrap
    def DeleteAllProbes(self, ):
        r"""
        Delete all Probes from the Measure Tool
    
    
        .. code-block:: python
    
            pid1 = AddGeom( "POD", "" )
    
            SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )
    
            probe_id_1 = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
            probe_id_2 = AddProbe( pid1, 0, 0.2, 0.3, "Probe 2" )
    
            DeleteAllProbes()
    
            probe_array = GetAllProbes()
    
            if  len(probe_array) != 0 : print( "Error: DeleteAllProbes" )
    
    
        """
        return _vsp.DeleteAllProbes()
    
    @client_wrap
    def GetAdvLinkNames(self, ):
        r"""
        Get an array of all advanced link names
    
    
        .. code-block:: python
    
            link_array = GetAdvLinkNames()
    
            for n in range(len(link_array) ):
    
                print( link_array[n] )
    
    
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of advanced link names
        """
        return _vsp.GetAdvLinkNames()
    
    @client_wrap
    def GetLinkIndex(self, name):
        r"""
        Find the index of a specific advanced link.
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: name string Name for advanced link
        :rtype: int
        :return: index for advanced link
    
        """
        return _vsp.GetLinkIndex(name)
    
    @client_wrap
    def DelAdvLink(self, index):
        r"""
        Delete an advanced link specified by index
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            DelAdvLink( indx )
    
            link_array = GetAdvLinkNames()
    
            # Should print nothing.
            for n in range(len(link_array) ):
    
                print( link_array[n] )
    
    
    
        :param [in]: index Index for advanced link
        """
        return _vsp.DelAdvLink(index)
    
    @client_wrap
    def DelAllAdvLinks(self, ):
        r"""
        Delete all advanced links
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            DelAllAdvLinks()
    
            link_array = GetAdvLinkNames()
    
            # Should print nothing.
            for n in range( len(link_array) ):
    
                print( link_array[n] )
    
    
    
        """
        return _vsp.DelAllAdvLinks()
    
    @client_wrap
    def AddAdvLink(self, name):
        r"""
        Add an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: name string Name for advanced link
        """
        return _vsp.AddAdvLink(name)
    
    @client_wrap
    def AddAdvLinkInput(self, index, parm_id, var_name):
        r"""
        Add an input variable to an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Advanced link index
        :param [in]: parm_id string Parameter ID for advanced link input variable
        :param [in]: var_name string Name for advanced link input variable
        """
        return _vsp.AddAdvLinkInput(index, parm_id, var_name)
    
    @client_wrap
    def AddAdvLinkOutput(self, index, parm_id, var_name):
        r"""
        Add an output variable to an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Advanced link index
        :param [in]: parm_id string Parameter ID for advanced link output variable
        :param [in]: var_name string Name for advanced link output variable
        """
        return _vsp.AddAdvLinkOutput(index, parm_id, var_name)
    
    @client_wrap
    def DelAdvLinkInput(self, index, var_name):
        r"""
        Delete an input variable from an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
            y_pos = GetParm( pod, "Y_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
            AddAdvLinkInput( indx, y_pos, "y" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            DelAdvLinkInput( indx, "y" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Advanced link index
        :param [in]: var_name string Name for advanced link input variable to delete
        """
        return _vsp.DelAdvLinkInput(index, var_name)
    
    @client_wrap
    def DelAdvLinkOutput(self, index, var_name):
        r"""
        Delete an output variable from an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
            y_pos = GetParm( pod, "Y_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
            AddAdvLinkOutput( indx, y_pos, "y" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            DelAdvLinkOutput( indx, "y" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Advanced link index
        :param [in]: var_name string Name for advanced link output variable to delete
        """
        return _vsp.DelAdvLinkOutput(index, var_name)
    
    @client_wrap
    def GetAdvLinkInputNames(self, index):
        r"""
        Get the name of all the inputs to a specified advanced link index
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            name_array = GetAdvLinkInputNames( indx )
    
            for n in range(len(name_array) ):
    
                print( name_array[n] )
    
    
    
        :param [in]: index int Advanced link index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of advanced link input names
        """
        return _vsp.GetAdvLinkInputNames(index)
    
    @client_wrap
    def GetAdvLinkInputParms(self, index):
        r"""
        Get the Parm IDs of all the inputs to a specified advanced link index
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            parm_array = GetAdvLinkInputParms( indx )
    
            for n in range( len(parm_array) ):
    
                print( parm_array[n] )
    
    
    
        :param [in]: index int Advanced link index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of advanced link input Parm IDs
        """
        return _vsp.GetAdvLinkInputParms(index)
    
    @client_wrap
    def GetAdvLinkOutputNames(self, index):
        r"""
        Get the Parm IDs of all the outputs to a specified advanced link index
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            name_array = GetAdvLinkOutputNames( indx )
    
            for n in range( len(name_array) ):
    
                print( name_array[n] )
    
    
    
        :param [in]: index int Advanced link index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of advanced link output names
        """
        return _vsp.GetAdvLinkOutputNames(index)
    
    @client_wrap
    def GetAdvLinkOutputParms(self, index):
        r"""
        Get the Parm IDs of all the outputs to a specified advanced link index
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            parm_array = GetAdvLinkOutputParms( indx )
    
            for n in range( len(parm_array) ):
    
                print( parm_array[n] )
    
    
    
        :param [in]: index int Advanced link index
        :rtype: std::vector< std::string,std::allocator< std::string > >
        :return: Array of advanced link output Parm IDs
        """
        return _vsp.GetAdvLinkOutputParms(index)
    
    @client_wrap
    def ValidateAdvLinkParms(self, index):
        r"""
        Validate the input and output parameters for an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            valid = ValidateAdvLinkParms( indx )
    
            if  valid :
                print( "Advanced link Parms are valid." )
            else:
                print( "Advanced link Parms are not valid." )
    
    
    
        :param [in]: index int Index for advanced link
        :rtype: boolean
        :return: Flag indicating whether parms are valid
        """
        return _vsp.ValidateAdvLinkParms(index)
    
    @client_wrap
    def SetAdvLinkCode(self, index, code):
        r"""
        Get the code from an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Index for advanced link
        :param [in]: code string Code for advanced link
        """
        return _vsp.SetAdvLinkCode(index, code)
    
    @client_wrap
    def GetAdvLinkCode(self, index):
        r"""
        Get the code from an advanced link
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            BuildAdvLinkScript( indx )
    
            code = GetAdvLinkCode( indx )
    
            print( code )
    
    
    
        :param [in]: index int Index for advanced link
        :rtype: string
        :return: String containing advanced link code
        """
        return _vsp.GetAdvLinkCode(index)
    
    @client_wrap
    def SearchReplaceAdvLinkCode(self, index, _from, to):
        r"""
        Search and replace strings in the advanced link code
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
            SearchReplaceAdvLinkCode( indx, "10.0", "12.3" )
    
            code = GetAdvLinkCode( indx )
    
            print( code )
    
            BuildAdvLinkScript( indx )
    
    
    
        :param [in]: index int Index for advanced link
        :param [in]: from string Search token
        :param [in]: to string Replace token
        """
        return _vsp.SearchReplaceAdvLinkCode(index, _from, to)
    
    @client_wrap
    def BuildAdvLinkScript(self, index):
        r"""
        Build (ready for execution and perform syntax check) an advanced link.
    
    
        .. code-block:: python
    
    
            pod = AddGeom( "POD", "" )
            length = FindParm( pod, "Length", "Design" )
            x_pos = GetParm( pod, "X_Rel_Location", "XForm" )
    
            AddAdvLink( "ExampleLink" )
            indx = GetLinkIndex( "ExampleLink" )
            AddAdvLinkInput( indx, length, "len" )
            AddAdvLinkOutput( indx, x_pos, "x" )
    
            SetAdvLinkCode( indx, "x = 10.0 - len;" )
    
            success = BuildAdvLinkScript( indx )
    
            if  success :
                print( "Advanced link build successful." )
            else:
                print( "Advanced link build not successful." )
    
    
    
        :param [in]: index int Index for advanced link
        :rtype: boolean
        :return: Flag indicating whether advanced link build was successful
        """
        return _vsp.BuildAdvLinkScript(index)
    
    @client_wrap
    def AddVec3D(self, INOUT, x, y, z):
        r"""AddVec3D(Vec3dVec INOUT, double x, double y, double z)"""
        return _vsp.AddVec3D(INOUT, x, y, z)
    # Register vec3d in _vsp:
        self.cvar = _vsp.cvar
        
    @client_wrap
    def signed_angle(self, a, b, ref):
        r"""signed_angle(vec3d a, vec3d b, vec3d ref) -> double"""
        return _vsp.signed_angle(a, b, ref)
    
    @client_wrap
    def radius_of_circle(self, p1, p2, p3):
        r"""radius_of_circle(vec3d p1, vec3d p2, vec3d p3) -> double"""
        return _vsp.radius_of_circle(p1, p2, p3)
    
    @client_wrap
    def center_of_circle(self, p1, p2, p3, center):
        r"""center_of_circle(vec3d p1, vec3d p2, vec3d p3, vec3d center)"""
        return _vsp.center_of_circle(p1, p2, p3, center)
    
    @client_wrap
    def triangle_plane_intersect_test(self, org, norm, p1, p2, p3):
        r"""triangle_plane_intersect_test(vec3d org, vec3d norm, vec3d p1, vec3d p2, vec3d p3) -> bool"""
        return _vsp.triangle_plane_intersect_test(org, norm, p1, p2, p3)
    
    @client_wrap
    def triangle_plane_minimum_dist(self, org, norm, p1, p2, p3, pa, pb):
        r"""triangle_plane_minimum_dist(vec3d org, vec3d norm, vec3d p1, vec3d p2, vec3d p3, vec3d pa, vec3d pb) -> double"""
        return _vsp.triangle_plane_minimum_dist(org, norm, p1, p2, p3, pa, pb)
    
    @client_wrap
    def triangle_plane_maximum_dist(self, org, norm, p1, p2, p3, pa, pb):
        r"""triangle_plane_maximum_dist(vec3d org, vec3d norm, vec3d p1, vec3d p2, vec3d p3, vec3d pa, vec3d pb) -> double"""
        return _vsp.triangle_plane_maximum_dist(org, norm, p1, p2, p3, pa, pb)
    
    @client_wrap
    def plane_plane_intersection(self, p0, n0, p1, n1, p, v):
        r"""plane_plane_intersection(vec3d p0, vec3d n0, vec3d p1, vec3d n1, vec3d p, vec3d v) -> bool"""
        return _vsp.plane_plane_intersection(p0, n0, p1, n1, p, v)
    
    @client_wrap
    def angle_pnt_2_plane(self, ptplane, norm, ptaxis, axis, pt, ccw, prot):
        r"""angle_pnt_2_plane(vec3d ptplane, vec3d norm, vec3d ptaxis, vec3d axis, vec3d pt, int ccw, vec3d prot) -> double"""
        return _vsp.angle_pnt_2_plane(ptplane, norm, ptaxis, axis, pt, ccw, prot)
    
    @client_wrap
    def signed_dist_pnt_2_plane(self, org, norm, pnt):
        r"""signed_dist_pnt_2_plane(vec3d org, vec3d norm, vec3d pnt) -> double"""
        return _vsp.signed_dist_pnt_2_plane(org, norm, pnt)
    
    @client_wrap
    def dist_pnt_2_plane(self, org, norm, pnt):
        r"""dist_pnt_2_plane(vec3d org, vec3d norm, vec3d pnt) -> double"""
        return _vsp.dist_pnt_2_plane(org, norm, pnt)
    
    @client_wrap
    def dist_pnt_2_line(self, line_pt1, line_pt2, pnt):
        r"""dist_pnt_2_line(vec3d line_pt1, vec3d line_pt2, vec3d pnt) -> double"""
        return _vsp.dist_pnt_2_line(line_pt1, line_pt2, pnt)
    
    @client_wrap
    def dist_pnt_2_ray(self, line_pt1, dir_unit_vec, pnt):
        r"""dist_pnt_2_ray(vec3d line_pt1, vec3d dir_unit_vec, vec3d pnt) -> double"""
        return _vsp.dist_pnt_2_ray(line_pt1, dir_unit_vec, pnt)
    
    @client_wrap
    def proj_u_on_v(self, u, v):
        r"""proj_u_on_v(vec3d u, vec3d v) -> vec3d"""
        return _vsp.proj_u_on_v(u, v)
    
    @client_wrap
    def proj_pnt_on_ray(self, line_pt1, line_dir, pnt):
        r"""proj_pnt_on_ray(vec3d line_pt1, vec3d line_dir, vec3d pnt) -> vec3d"""
        return _vsp.proj_pnt_on_ray(line_pt1, line_dir, pnt)
    
    @client_wrap
    def proj_pnt_on_line(self, line_pt1, line_pt2, pnt):
        r"""proj_pnt_on_line(vec3d line_pt1, vec3d line_pt2, vec3d pnt) -> vec3d"""
        return _vsp.proj_pnt_on_line(line_pt1, line_pt2, pnt)
    
    @client_wrap
    def proj_pnt_to_plane(self, org, plane_ln1, plane_ln2, pnt):
        r"""proj_pnt_to_plane(vec3d org, vec3d plane_ln1, vec3d plane_ln2, vec3d pnt) -> vec3d"""
        return _vsp.proj_pnt_to_plane(org, plane_ln1, plane_ln2, pnt)
    
    @client_wrap
    def proj_vec_to_plane(self, vec, norm):
        r"""proj_vec_to_plane(vec3d vec, vec3d norm) -> vec3d"""
        return _vsp.proj_vec_to_plane(vec, norm)
    
    @client_wrap
    def tri_seg_intersect(self, A, B, C, D, E, u, w, t):
        r"""tri_seg_intersect(vec3d A, vec3d B, vec3d C, vec3d D, vec3d E, double & u, double & w, double & t) -> int"""
        return _vsp.tri_seg_intersect(A, B, C, D, E, u, w, t)
    
    @client_wrap
    def tri_ray_intersect(self, A, B, C, D, E, u, w, t):
        r"""tri_ray_intersect(vec3d A, vec3d B, vec3d C, vec3d D, vec3d E, double & u, double & w, double & t) -> int"""
        return _vsp.tri_ray_intersect(A, B, C, D, E, u, w, t)
    
    @client_wrap
    def plane_ray_intersect(self, *args):
        r"""
        plane_ray_intersect(vec3d A, vec3d B, vec3d C, vec3d D, vec3d E, double & t) -> int
        plane_ray_intersect(vec3d orig, vec3d norm, vec3d D, vec3d E, double & t) -> int
        """
        return _vsp.plane_ray_intersect(*args)
    
    @client_wrap
    def ray_ray_intersect(self, A, B, C, D, int_pnt1, int_pnt2):
        r"""ray_ray_intersect(vec3d A, vec3d B, vec3d C, vec3d D, vec3d int_pnt1, vec3d int_pnt2) -> int"""
        return _vsp.ray_ray_intersect(A, B, C, D, int_pnt1, int_pnt2)
    
    @client_wrap
    def tetra_volume(self, A, B, C):
        r"""tetra_volume(vec3d A, vec3d B, vec3d C) -> double"""
        return _vsp.tetra_volume(A, B, C)
    
    @client_wrap
    def area(self, A, B, C):
        r"""area(vec3d A, vec3d B, vec3d C) -> double"""
        return _vsp.area(A, B, C)
    
    @client_wrap
    def dist3D_Segment_to_Segment(self, *args):
        r"""
        dist3D_Segment_to_Segment(vec3d S1P0, vec3d S1P1, vec3d S2P0, vec3d S2P1) -> double
        dist3D_Segment_to_Segment(vec3d S1P0, vec3d S1P1, vec3d S2P0, vec3d S2P1, double * Lt, vec3d Ln, double * St, vec3d Sn) -> double
        """
        return _vsp.dist3D_Segment_to_Segment(*args)
    
    @client_wrap
    def nearSegSeg(self, L0, L1, S0, S1, Lt, Ln, St, Sn):
        r"""nearSegSeg(vec3d L0, vec3d L1, vec3d S0, vec3d S1, double * Lt, vec3d Ln, double * St, vec3d Sn) -> double"""
        return _vsp.nearSegSeg(L0, L1, S0, S1, Lt, Ln, St, Sn)
    
    @client_wrap
    def pointLineDistSquared(self, p, lp0, lp1, t, pon):
        r"""pointLineDistSquared(vec3d p, vec3d lp0, vec3d lp1, double & t, vec3d pon) -> double"""
        return _vsp.pointLineDistSquared(p, lp0, lp1, t, pon)
    
    @client_wrap
    def pointSegDistSquared(self, p, sp0, sp1, t, pon):
        r"""pointSegDistSquared(vec3d p, vec3d sp0, vec3d sp1, double & t, vec3d pon) -> double"""
        return _vsp.pointSegDistSquared(p, sp0, sp1, t, pon)
    
    @client_wrap
    def point_on_line(self, lp0, lp1, t):
        r"""point_on_line(vec3d lp0, vec3d lp1, double const & t) -> vec3d"""
        return _vsp.point_on_line(lp0, lp1, t)
    
    @client_wrap
    def MapToPlane(self, p, planeOrig, planeVec1, planeVec2):
        r"""MapToPlane(vec3d p, vec3d planeOrig, vec3d planeVec1, vec3d planeVec2) -> vec2d"""
        return _vsp.MapToPlane(p, planeOrig, planeVec1, planeVec2)
    
    @client_wrap
    def MapFromPlane(self, uw, planeOrig, planeVec1, planeVec2):
        r"""MapFromPlane(vec2d uw, vec3d planeOrig, vec3d planeVec1, vec3d planeVec2) -> vec3d"""
        return _vsp.MapFromPlane(uw, planeOrig, planeVec1, planeVec2)
    
    @client_wrap
    def plane_half_space(self, planeOrig, planeNorm, pnt):
        r"""plane_half_space(vec3d planeOrig, vec3d planeNorm, vec3d pnt) -> int"""
        return _vsp.plane_half_space(planeOrig, planeNorm, pnt)
    
    @client_wrap
    def line_line_intersect(self, p1, p2, p3, p4, s, t):
        r"""line_line_intersect(vec3d p1, vec3d p2, vec3d p3, vec3d p4, double * s, double * t) -> bool"""
        return _vsp.line_line_intersect(p1, p2, p3, p4, s, t)
    
    @client_wrap
    def RotateArbAxis(self, p, theta, r):
        r"""RotateArbAxis(vec3d p, double theta, vec3d r) -> vec3d"""
        return _vsp.RotateArbAxis(p, theta, r)
    
    @client_wrap
    def PtInTri(self, v0, v1, v2, p):
        r"""PtInTri(vec3d v0, vec3d v1, vec3d v2, vec3d p) -> bool"""
        return _vsp.PtInTri(v0, v1, v2, p)
    
    @client_wrap
    def BarycentricWeights(self, v0, v1, v2, p):
        r"""BarycentricWeights(vec3d v0, vec3d v1, vec3d v2, vec3d p) -> vec3d"""
        return _vsp.BarycentricWeights(v0, v1, v2, p)
    
    @client_wrap
    def BilinearWeights(self, p0, p1, p, weights):
        r"""BilinearWeights(vec3d p0, vec3d p1, vec3d p, DoubleVector weights)"""
        return _vsp.BilinearWeights(p0, p1, p, weights)
    
    @client_wrap
    def tri_tri_min_dist(self, v0, v1, v2, v3, v4, v5, p1, p2):
        r"""tri_tri_min_dist(vec3d v0, vec3d v1, vec3d v2, vec3d v3, vec3d v4, vec3d v5, vec3d p1, vec3d p2) -> double"""
        return _vsp.tri_tri_min_dist(v0, v1, v2, v3, v4, v5, p1, p2)
    
    @client_wrap
    def pnt_tri_min_dist(self, v0, v1, v2, pnt, pnearest):
        r"""pnt_tri_min_dist(vec3d v0, vec3d v1, vec3d v2, vec3d pnt, vec3d pnearest) -> double"""
        return _vsp.pnt_tri_min_dist(v0, v1, v2, pnt, pnearest)
    
    @client_wrap
    def slerp(self, a, b, t):
        r"""slerp(vec3d a, vec3d b, double const & t) -> vec3d"""
        return _vsp.slerp(a, b, t)
    
    @client_wrap
    def printpt(self, v):
        r"""printpt(vec3d v)"""
        return _vsp.printpt(v)
    
    @client_wrap
    def ToSpherical(self, v):
        r"""ToSpherical(vec3d v) -> vec3d"""
        return _vsp.ToSpherical(v)
    
    @client_wrap
    def ToSpherical2(self, v, vdet):
        r"""ToSpherical2(vec3d v, vec3d vdet) -> vec3d"""
        return _vsp.ToSpherical2(v, vdet)
    
    @client_wrap
    def ToCartesian(self, v):
        r"""ToCartesian(vec3d v) -> vec3d"""
        return _vsp.ToCartesian(v)
    
    @client_wrap
    def FitPlane(self, pts, cen, norm):
        r"""FitPlane(Vec3dVec pts, vec3d cen, vec3d norm)"""
        return _vsp.FitPlane(pts, cen, norm)
    
    
    @client_wrap
    def to_string(self, v):
        r"""to_string(vec3d v) -> std::string"""
        return _vsp.to_string(v)
    
    @client_wrap
    def compsum(self, x):
        r"""compsum(Vec3dVec x) -> vec3d"""
        return _vsp.compsum(x)
    # Register vec2d in _vsp:
    
    @client_wrap
    def dist(self, *args):
        r"""
        dist(vec3d a, vec3d b) -> double
        dist(vec2d a, vec2d b) -> double
        """
        return _vsp.dist(*args)
    
    @client_wrap
    def dist_squared(self, *args):
        r"""
        dist_squared(vec3d a, vec3d b) -> double
        dist_squared(vec2d a, vec2d b) -> double
        """
        return _vsp.dist_squared(*args)
    
    @client_wrap
    def cross(self, *args):
        r"""
        cross(vec3d a, vec3d b) -> vec3d
        cross(vec2d a, vec2d b) -> double
        """
        return _vsp.cross(*args)
    
    @client_wrap
    def dot(self, *args):
        r"""
        dot(vec3d a, vec3d b) -> double
        dot(vec2d a, vec2d b) -> double
        """
        return _vsp.dot(*args)
    
    @client_wrap
    def angle(self, *args):
        r"""
        angle(vec3d a, vec3d b) -> double
        angle(vec2d a, vec2d b) -> double
        """
        return _vsp.angle(*args)
    
    @client_wrap
    def cos_angle(self, *args):
        r"""
        cos_angle(vec3d a, vec3d b) -> double
        cos_angle(vec2d a, vec2d b) -> double
        """
        return _vsp.cos_angle(*args)
    
    @client_wrap
    def seg_seg_intersect(self, pnt_A, pnt_B, pnt_C, pnt_D, int_pnt, t1, t2):
        r"""seg_seg_intersect(vec2d pnt_A, vec2d pnt_B, vec2d pnt_C, vec2d pnt_D, vec2d int_pnt, double & t1, double & t2) -> int"""
        return _vsp.seg_seg_intersect(pnt_A, pnt_B, pnt_C, pnt_D, int_pnt, t1, t2)
    
    @client_wrap
    def proj_pnt_on_line_seg(self, *args):
        r"""
        proj_pnt_on_line_seg(vec3d line_pt1, vec3d line_pt2, vec3d pnt) -> vec3d
        proj_pnt_on_line_seg(vec2d line_A, vec2d line_B, vec2d pnt) -> vec2d
        """
        return _vsp.proj_pnt_on_line_seg(*args)
    
    @client_wrap
    def proj_pnt_on_line_u(self, line_A, line_B, pnt):
        r"""proj_pnt_on_line_u(vec2d line_A, vec2d line_B, vec2d pnt) -> double"""
        return _vsp.proj_pnt_on_line_u(line_A, line_B, pnt)
    
    @client_wrap
    def encode(self, x_min, y_min, x_max, y_max, pnt, code):
        r"""encode(double x_min, double y_min, double x_max, double y_max, vec2d pnt, int [4] code)"""
        return _vsp.encode(x_min, y_min, x_max, y_max, pnt, code)
    
    @client_wrap
    def clip_seg_rect(self, x_min, y_min, x_max, y_max, pnt1, pnt2, visible):
        r"""clip_seg_rect(double x_min, double y_min, double x_max, double y_max, vec2d pnt1, vec2d pnt2, int & visible)"""
        return _vsp.clip_seg_rect(x_min, y_min, x_max, y_max, pnt1, pnt2, visible)
    
    @client_wrap
    def PointInPolygon(self, R, pnts):
        r"""PointInPolygon(vec2d R, std::vector< vec2d,std::allocator< vec2d > > const & pnts) -> bool"""
        return _vsp.PointInPolygon(R, pnts)
    
    @client_wrap
    def det(self, p0, p1, offset):
        r"""det(vec2d p0, vec2d p1, vec2d offset) -> double"""
        return _vsp.det(p0, p1, offset)
    
    @client_wrap
    def poly_area(self, *args):
        r"""
        poly_area(Vec3dVec pnt_vec) -> double
        poly_area(std::vector< vec2d,std::allocator< vec2d > > const & pnt_vec) -> double
        """
        return _vsp.poly_area(*args)
    
    @client_wrap
    def poly_centroid(self, pnt_vec):
        r"""poly_centroid(std::vector< vec2d,std::allocator< vec2d > > const & pnt_vec) -> vec2d"""
        return _vsp.poly_centroid(pnt_vec)
    
    @client_wrap
    def orient2d(self, p0, p1, p):
        r"""orient2d(vec2d p0, vec2d p1, vec2d p) -> double"""
        return _vsp.orient2d(p0, p1, p)
    
    @client_wrap
    def bi_lin_interp(self, p0, p1, p2, p3, s, t, p):
        r"""bi_lin_interp(vec2d p0, vec2d p1, vec2d p2, vec2d p3, double s, double t, vec2d p)"""
        return _vsp.bi_lin_interp(p0, p1, p2, p3, s, t, p)
    
    @client_wrap
    def inverse_bi_lin_interp(self, p0, p1, p2, p3, p, s, t, s2, t2):
        r"""inverse_bi_lin_interp(vec2d p0, vec2d p1, vec2d p2, vec2d p3, vec2d p, double & s, double & t, double & s2, double & t2) -> int"""
        return _vsp.inverse_bi_lin_interp(p0, p1, p2, p3, p, s, t, s2, t2)
    
    # Register Matrix4d in _vsp:
    

    # function to send and receive data from the facade server
    def _send_receive(self, func_name, args, kwargs):
        b_data = pack_data([func_name, args, kwargs], True)
        self._sock.sendall(b_data)
        result = None
        b_result = []
        while True:
            packet = self._sock.recv(202400)
            if not packet: break
            b_result.append(packet)
            try:
                result = unpack_data(b_result)
                break
            except:
                pass
        if isinstance(result, list) and result[0] == "error":
            sys.excepthook = _exception_hook
            raise Exception(result[1])
        return result

    def IsFacade(self):
        """
        Returns True if the facade API is in use.


        .. code-block:: python

            is_facade = IsFacade()

        """

        return True
    def IsGUIRunning(self):
        """
        Returns True if the GUI event loop is running.


        .. code-block:: python

            is_gui_active = IsGUIRunning()

        """

        return self._send_receive('IsGUIRunning', [], {})

    def _run_func(self, func, *args, **kwargs):
        try:
            kwargs['vsp_instance'] = self
            return func(*args, **kwargs)
        except TypeError:
            kwargs.pop("vsp_instance")
            return func(*args, **kwargs)

    def _close_server(self):
        try:
            self._proc.terminate()
        except:
            pass
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
            self._sock.detach()
            del self._sock
        except:
            pass
        try:
            del self.t
        except:
            pass
    def __del__(self):
        try:
            self._proc.terminate()
        except:
            pass
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
            self._sock.detach()
            del self._sock
        except:
            pass
        try:
            del self.t
        except:
            pass


class _server_controller():
    def __init__(self) -> None:
        print("server controller initialized")
        self._name_to_server = {}
        self._port_to_name = {}
        self._name_to_port = {}
        self.name_num = 1
        self.funcs = []
    def start_vsp_instance(self, name=None, port=-1) -> _vsp_server:

        if not name:
            name = f"default_name_{self.name_num}"
            while name in self._name_to_server:
                self.name_num += 1
                name = f"default_name_{self.name_num}"

        assert isinstance(name,str), "Name must be a string"
        assert not name in self._name_to_server, f"Server with name {name} already exists"
        assert not port in self._port_to_name, f"Server with port {port} already exists"
        self._name_to_server[name] = new_server = _vsp_server(name, self.funcs, port=port)
        self._port_to_name[new_server.port] = name
        self._name_to_port[name] = new_server.port

        return new_server

    def get_vsp_instance(self, server):
        try:
            if isinstance(server, str):
                return self._name_to_server[server]
            elif server in self._name_to_server.values():
                    return server
        except:
            pass
        print("Warning: Could not find vsp_instance, returning singleton")
        return None

    def stop_vsp_instance(self, name=None, port=None):
        assert name or port, "please specify a name or a port"
        if port:
            server_name = self._port_to_name[port]
            server_port = port
        elif name:
            server_port = self._name_to_port[name]
            server_name = name
        if server_name == "vsp_singleton":
            print("Can't close vsp_singleton")
            return
        self._port_to_name.pop(server_port)
        self._name_to_port.pop(server_name)
        self._name_to_server[server_name]._close_server()
        del self._name_to_server[server_name]

    def set_functions(self, funcs):
        self.funcs = funcs

from openvsp.vsp import ErrorObj
from openvsp.vsp import ErrorMgrSingleton
from openvsp.vsp import vec3d
from openvsp.vsp import Matrix4d
vsp_servers = _server_controller()
