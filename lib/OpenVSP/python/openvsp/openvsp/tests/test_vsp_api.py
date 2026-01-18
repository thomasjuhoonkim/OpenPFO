
import unittest
import os, sys

curr_path = os.path.dirname(os.path.realpath(__file__))
vsp_path = os.path.join(curr_path, '../..')
sys.path.insert(1, vsp_path)

from openvsp import *

class TestOpenVSP(unittest.TestCase):
	def setUp(self):
		VSPRenew()
	def test_VSPCheckSetup(self):

		VSPCheckSetup()

		# Continue to do things...


	def test_VSPRenew(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		SetParmVal( pod_id, "Y_Rel_Location", "XForm", 2.0 )

		VSPRenew()

		if  len(FindGeoms()) != 0 : print( "ERROR: VSPRenew" )

	def test_Update(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf

		num_xsecs = GetNumXSec( xsec_surf )

		#==== Set Tan Angles At Nose/Tail
		SetXSecTanAngles( GetXSec( xsec_surf, 0 ), XSEC_BOTH_SIDES, 90, -1.0e12, -1.0e12, -1.0e12 )
		SetXSecTanAngles( GetXSec( xsec_surf, num_xsecs - 1 ), XSEC_BOTH_SIDES, -90, -1.0e12, -1.0e12, -1.0e12 )

		Update()       # Force Surface Update


	def test_GetVSPVersion(self):
		print( "The current OpenVSP version is: ", False )

		print( GetVSPVersion() )

	def test_GetVSPVersionMajor(self):
		print( "The current OpenVSP version is: ", False )

		major = GetVSPVersionMajor()
		minor = GetVSPVersionMinor()
		change = GetVSPVersionChange()

		print( f"{major}.{minor}.{change}" )

	def test_GetVSPVersionMinor(self):
		print( "The current OpenVSP version is: ", False )

		major = GetVSPVersionMajor()
		minor = GetVSPVersionMinor()
		change = GetVSPVersionChange()

		print( f"{major}.{minor}.{change}" )

	def test_GetVSPVersionChange(self):
		print( "The current OpenVSP version is: ", False )

		major = GetVSPVersionMajor()
		minor = GetVSPVersionMinor()
		change = GetVSPVersionChange()

		print( f"{major}.{minor}.{change}" )

	def test_GetVSPExePath(self):
		print( "The current VSP executable path is: ", False )

		print( GetVSPExePath() )

	def test_SetVSPAEROPath(self):
		if  not CheckForVSPAERO( GetVSPExePath() ) :
			vspaero_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5"
			SetVSPAEROPath( vspaero_path )

	def test_GetVSPAEROPath(self):
		if  not CheckForVSPAERO( GetVSPAEROPath() ) :
			print( "VSPAERO is not where OpenVSP thinks it is. I should move the VSPAERO executable or call SetVSPAEROPath." )

	def test_CheckForVSPAERO(self):
		vspaero_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5"

		if  CheckForVSPAERO( vspaero_path ) :
			SetVSPAEROPath( vspaero_path )

	def test_SetVSPHelpPath(self):
		if  not CheckForVSPHelp( GetVSPExePath() ) :
			vsphelp_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5/help"
			SetVSPHelpPath( vsphelp_path )

	def test_GetVSPHelpPath(self):
		if  not CheckForVSPHelp( GetVSPHelpPath() ) :
			print( "VSPAERO is not where OpenVSP thinks it is. I should move the VSPAERO executable or call SetVSPAEROPath." )

	def test_CheckForVSPHelp(self):
		vsphelp_path = "C:/Users/example_user/Documents/OpenVSP_3.4.5/help"

		if  CheckForVSPHelp( vsphelp_path ) :
			SetVSPHelpPath( vsphelp_path )

	def test_ReadVSPFile(self):
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

	def test_WriteVSPFile(self):
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

	def test_SetVSP3FileName(self):
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

	def test_GetVSPFileName(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		fname = "example_fuse.vsp3"

		SetVSP3FileName( fname )

		Update()

		#==== Save Vehicle to File ====//
		print( "\tSaving vehicle file to: ", False )

		print( fname )

		WriteVSPFile( GetVSPFileName(), SET_ALL )

	def test_ClearVSPModel(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		#==== Reset Geometry ====//
		print( "--->Resetting VSP model to blank slate\n" )
		ClearVSPModel()

	def test_ExportFile(self):
		wid = AddGeom( "WING" )             # Add Wing

		ExportFile( "Airfoil_Metadata.csv", SET_ALL, EXPORT_SELIG_AIRFOIL )

		mesh_id = ExportFile( "Example_Mesh.msh", SET_ALL, EXPORT_GMSH )
		DeleteGeom( mesh_id ) # Delete the mesh generated by the GMSH export

	def test_SetBEMPropID(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		SetBEMPropID( prop_id )

		ExportFile( "ExampleBEM.bem", SET_ALL, EXPORT_BEM )

	def test_SetComputationFileName(self):
		#==== Set File Name ====//
		SetComputationFileName( DEGEN_GEOM_CSV_TYPE, "TestDegenScript.csv" )

		#==== Run Degen Geom ====//
		ComputeDegenGeom( SET_ALL, DEGEN_GEOM_CSV_TYPE )

	def test_ComputeMassProps(self):
		#==== Test Mass Props ====//
		pid = AddGeom( "POD", "" )

		mesh_id = ComputeMassProps( SET_ALL, 20, X_DIR )

		mass_res_id = FindLatestResultsID( "Mass_Properties" )

		double_arr = GetDoubleResults( mass_res_id, "Total_Mass" )

		if  len(double_arr) != 1 : print( "---> Error: API ComputeMassProps" )

	def test_ComputeCompGeom(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		#==== Run CompGeom And Get Results ====//
		mesh_id = ComputeCompGeom( SET_ALL, False, 0 )                      # Half Mesh false and no file export

		comp_res_id = FindLatestResultsID( "Comp_Geom" )                    # Find Results ID

		double_arr = GetDoubleResults( comp_res_id, "Wet_Area" )    # Extract Results

	def test_ComputePlaneSlice(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		#==== Test Plane Slice ====//
		slice_mesh_id = ComputePlaneSlice( 0, 6, vec3d( 0.0, 0.0, 1.0 ), True )

		pslice_results = FindLatestResultsID( "Slice" )

		double_arr = GetDoubleResults( pslice_results, "Slice_Area" )

		if  len(double_arr) != 6 : print( "---> Error: API ComputePlaneSlice" )

	def test_ComputeDegenGeom(self):
		#==== Set File Name ====//
		SetComputationFileName( DEGEN_GEOM_CSV_TYPE, "TestDegenScript.csv" )

		#==== Run Degen Geom ====//
		ComputeDegenGeom( SET_ALL, DEGEN_GEOM_CSV_TYPE )

	def test_ComputeCFDMesh(self):
		#==== CFDMesh Method Facet Export =====//
		SetComputationFileName( CFD_FACET_TYPE, "TestCFDMeshFacet_API.facet" )

		print( "\tComputing CFDMesh..." )

		ComputeCFDMesh( SET_ALL, SET_NONE, CFD_FACET_TYPE )

	def test_SetCFDMeshVal(self):
		SetCFDMeshVal( CFD_MIN_EDGE_LEN, 1.0 )

	def test_SetCFDWakeFlag(self):
		#==== Add Wing Geom ====//
		wid = AddGeom( "WING", "" )

		SetCFDWakeFlag( wid, True )
		# This is equivalent to SetParmValUpdate( wid, "Wake", "Shape", 1.0 )
		# To change the scale: SetParmValUpdate( wid, "WakeScale", "WakeSettings", 10.0 )
		# To change the angle: SetParmValUpdate( wid, "WakeAngle", "WakeSettings", -5.0 )

	def test_DeleteAllCFDSources(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		AddCFDSource( POINT_SOURCE, pid, 0, 0.25, 2.0, 0.5, 0.5 )      # Add A Point Source

		DeleteAllCFDSources()

	def test_AddDefaultSources(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		AddDefaultSources() # 3 Sources: Def_Fwd_PS, Def_Aft_PS, Def_Fwd_Aft_LS

	def test_AddCFDSource(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		AddCFDSource( POINT_SOURCE, pid, 0, 0.25, 2.0, 0.5, 0.5 )      # Add A Point Source

	def test_SetVSPAERORefWingID(self):
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

	def test_GetNumAnalysis(self):
		nanalysis = GetNumAnalysis()

		print( f"Number of registered analyses: {nanalysis}" )

	def test_ListAnalysis(self):
		analysis_array = ListAnalysis()

		print( "List of Available Analyses: " )

		for i in range(int( len(analysis_array) )):

			print( "    " + analysis_array[i] )

	def test_GetAnalysisInputNames(self):
		analysis_name = "VSPAEROComputeGeometry"

		in_names =  GetAnalysisInputNames( analysis_name )

		print("Analysis Inputs: ")

		for i in range(int( len(in_names) )):

			print( ( "\t" + in_names[i] + "\n" ) )

	def test_GetAnalysisDoc(self):
		analysis_name = "VSPAEROComputeGeometry"

		doc = GetAnalysisDoc( analysis_name )

	def test_ExecAnalysis(self):
		analysis_name = "VSPAEROComputeGeometry"

		res_id = ExecAnalysis( analysis_name )

	def test_GetAnalysisInputType(self):
		analysis = "VSPAEROComputeGeometry"

		inp_array = GetAnalysisInputNames( analysis )

		for j in range(int( len(inp_array) )):

			typ = GetAnalysisInputType( analysis, inp_array[j] )

	def test_GetIntAnalysisInput(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# Set to panel method
		thick_set = GetIntAnalysisInput( analysis_name, "GeomSet" )
		thin_set = GetIntAnalysisInput( analysis_name, "ThinGeomSet" )

		thick_set = [vsp.SET_NONE]
		thin_set = [vsp.SET_ALL]

		SetIntAnalysisInput( analysis_name, "GeomSet", thick_set )
		SetIntAnalysisInput( analysis_name, "ThinGeomSet", thin_set )

	def test_GetDoubleAnalysisInput(self):
		vinfFCinput = list( GetDoubleAnalysisInput( "ParasiteDrag", "Vinf" ) )

		vinfFCinput[0] = 629

		SetDoubleAnalysisInput( "ParasiteDrag", "Vinf", vinfFCinput )

	def test_GetStringAnalysisInput(self):
		fileNameInput = GetStringAnalysisInput( "ParasiteDrag", "FileName" )

		fileNameInput = ["ParasiteDragExample"]

		SetStringAnalysisInput( "ParasiteDrag", "FileName", fileNameInput )

	def test_GetVec3dAnalysisInput(self):
		# PlanarSlice
		norm = GetVec3dAnalysisInput( "PlanarSlice", "Norm" )

		norm[0].set_xyz( 0.23, 0.6, 0.15 )

		SetVec3dAnalysisInput( "PlanarSlice", "Norm", norm )

	def test_SetAnalysisInputDefaults(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# Set defaults
		SetAnalysisInputDefaults( analysis_name )

	def test_SetIntAnalysisInput(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# Set to panel method
		thick_set = GetIntAnalysisInput( analysis_name, "GeomSet" )
		thin_set = GetIntAnalysisInput( analysis_name, "ThinGeomSet" )

		thick_set = [vsp.SET_NONE]
		thin_set = [vsp.SET_ALL]

		SetIntAnalysisInput( analysis_name, "GeomSet", thick_set )
		SetIntAnalysisInput( analysis_name, "ThinGeomSet", thin_set )

	def test_SetDoubleAnalysisInput(self):
		#==== Analysis: CpSlicer ====//
		analysis_name = "CpSlicer"

		# Setup cuts
		ycuts = []
		ycuts.append( 2.0 )
		ycuts.append( 4.5 )
		ycuts.append( 8.0 )

		SetDoubleAnalysisInput( analysis_name, "YSlicePosVec", ycuts, 0 )

	def test_SetStringAnalysisInput(self):
		fileNameInput = GetStringAnalysisInput( "ParasiteDrag", "FileName" )

		fileNameInput = ["ParasiteDragExample"]

		SetStringAnalysisInput( "ParasiteDrag", "FileName", fileNameInput )

	def test_SetVec3dAnalysisInput(self):
		# PlanarSlice
		norm = GetVec3dAnalysisInput( "PlanarSlice", "Norm" )

		norm[0].set_xyz( 0.23, 0.6, 0.15 )

		SetVec3dAnalysisInput( "PlanarSlice", "Norm", norm )

	def test_PrintAnalysisInputs(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# list inputs, type, and current values
		PrintAnalysisInputs( analysis_name )

	def test_PrintAnalysisDocs(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# list inputs, type, and documentation
		PrintAnalysisDocs( analysis_name )

	def test_SummarizeAttributes(self):
		##==== Attributes: SummarizeAttributes ====##
		SummaryText = SummarizeAttributes()
		print( SummaryText )

	def test_SummarizeAttributesAsTree(self):
		##==== Attributes: SummarizeAttributesAsTree ====##
		SummaryTextTree = SummarizeAttributesAsTree();
		print( SummaryTextTree )

	def test_FindAllAttributes(self):
		##==== Attributes: FindAllAttributes ====##
		AttrIDs = FindAllAttributes()
		for AttrID in AttrIDs:
			print( AttrID )

	def test_FindAttributesByName(self):
		##==== Attributes: FindAttributesByName ====##
		AttrIDs = FindAttributesByName( "Watermark" )
		for AttrID in AttrIDs:
			print( AttrID )

	def test_FindAttributeByName(self):
		##==== Attributes: FindAttributeByName ====##
		AttrID = FindAttributeByName( "Watermark", 0 )
		print( AttrID )

	def test_FindAttributeInCollection(self):
		##==== Attributes: FindAttributeInCollection ====##
		VehID = GetVehicleID()
		AttrID = FindAttributeInCollection( VehID, 'Watermark', 0 )
		print( AttrID )

	def test_FindAttributeNamesInCollection(self):
		##==== Attributes: FindAttributeNamesInCollection ====##
		VehID = GetVehicleID()
		CollID = GetChildCollection( VehID )
		AttrNames = FindAttributeNamesInCollection( CollID )
		for AttrName in AttrNames:
			print( AttrName )

	def test_FindAttributesInCollection(self):
		##==== Attributes: FindAttributesInCollection ====##
		VehID = GetVehicleID()
		CollID = GetChildCollection( VehID )
		AttrIDs = FindAttributesInCollection( CollID )
		for AttrID in AttrIDs:
			print( AttrID )

	def test_FindAttributedObjects(self):
		##==== Attributes: FindAttributedObjects ====##
		AttachIDs = FindAttributedObjects()
		for AttachID in AttachIDs:
			print( AttachID )

	def test_GetObjectType(self):
		##==== Attributes: GetObjectType ====##
		AttachIDs = FindAttributedObjects()
		for AttachID in AttachIDs:
			ObjType = GetObjectType( AttachID )
			print( ObjType )

	def test_GetObjectTypeName(self):
		AttachIDs = FindAttributedObjects()
		for AttachID in AttachIDs:
			ObjTypeName = GetObjectTypeName( AttachID )
			print( ObjTypeName )

	def test_GetObjectName(self):
		##==== Attributes: GetObjectName ====##
		AttachIDs = FindAttributedObjects()
		for AttachID in AttachIDs:
			ObjName = GetObjectName( AttachID )
			print( ObjName )

	def test_GetObjectParent(self):
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

	def test_GetChildCollection(self):
		##==== Attributes: GetChildCollection =====##
		VehID = GetVehicleID()
		CollID = GetChildCollection( VehID )
		print( CollID )


	def test_GetGeomSetCollection(self):
		##==== Attributes: GetGeomSetCollection =====##
		CollID = GetGeomSetCollection( 0 )
		print( CollID )

	def test_GetAttributeName(self):
		##==== Attributes: GetAttributeName =====##

		AttrIDs = FindAllAttributes()

		for AttrID in AttrIDs:
			AttrName = GetAttributeName( AttrID )
			print( AttrName )

	def test_GetAttributeID(self):
		##==== Attributes: GetAttributeID =====##

		VehID = GetVehicleID()
		CollID = GetChildCollection( VehID )
		AttrNames = FindAttributeNamesInCollection( CollID )
		for AttrName in AttrNames:
			AttrID = GetAttributeID( CollID, AttrName, 0 )
			print( AttrID )


	def test_GetAttributeDoc(self):
		##==== Attributes: GetAttributeDoc =====##
		AttrID = FindAllAttributes()[0]
		AttrDoc = GetAttributeDoc(AttrID)
		print( AttrDoc )

	def test_GetAttributeType(self):
		##==== Attributes: GetAttributeType =====##
		AttrID = FindAllAttributes()[0]
		AttrType = GetAttributeType( AttrID )
		print( AttrType )

	def test_GetAttributeTypeName(self):
		##==== Attributes: GetAttributeTypeName =====##
		AttrID = FindAllAttributes()[0]
		AttributeTypeName = GetAttributeTypeName( AttrID )
		print( AttributeTypeName )


	def test_GetAttributeBoolVal(self):
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

	def test_GetAttributeIntVal(self):
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

	def test_GetAttributeDoubleVal(self):
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

	def test_GetAttributeStringVal(self):
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

	def test_GetAttributeParmID(self):
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

	def test_GetAttributeParmVal(self):
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


	def test_GetAttributeParmName(self):
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


	def test_GetAttributeVec3dVal(self):
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

	def test_GetAttributeIntMatrixVal(self):
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


	def test_GetAttributeDoubleMatrixVal(self):
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

	def test_SetAttributeName(self):
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

	def test_SetAttributeDoc(self):
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

	def test_SetAttributeBool(self):
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

	def test_SetAttributeInt(self):
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

	def test_SetAttributeDouble(self):
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

	def test_SetAttributeString(self):
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

	def test_SetAttributeParmID(self):
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

	def test_SetAttributeVec3d(self):
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

	def test_SetAttributeIntMatrix(self):
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

	def test_SetAttributeDoubleMatrix(self):
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

	def test_DeleteAttribute(self):
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

	def test_AddAttributeBool(self):
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

	def test_AddAttributeInt(self):
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

	def test_AddAttributeDouble(self):
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

	def test_AddAttributeString(self):
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

	def test_AddAttributeParm(self):
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


	def test_AddAttributeVec3d(self):
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

	def test_AddAttributeIntMatrix(self):
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

	def test_AddAttributeDoubleMatrix(self):
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

	def test_AddAttributeGroup(self):
		##==== Attribute: AddAttributeGroup  =====##

		VehID = GetVehicleID()
		CollID = GetChildCollection( VehID )
		AttrName = 'Example_Attr_Group'
		AttrID = AddAttributeGroup( CollID, AttrName )
		if GetAttributeType( AttrID ) == ATTR_COLLECTION_DATA:
			print( "Added Attribute Group" )
		else:
			print( "AddAttributeGroup error!" )


	def test_CopyAttribute(self):
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
	def test_CutAttribute(self):
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

	def test_PasteAttribute(self):
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

	def test_GetAllResultsNames(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		results_array = GetAllResultsNames()

		for i in range(int( len(results_array) )):

			resid = FindLatestResultsID( results_array[i] )
			PrintResults( resid )

	def test_GetAllDataNames(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		data_names = GetAllDataNames( res_id )

		if  len(data_names) != 5 : print( "---> Error: API GetAllDataNames" )

	def test_GetNumResults(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		if ( GetNumResults( "Test_Results" ) != 2 ): print( "---> Error: API GetNumResults" )

	def test_GetResultsName(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# Set defaults
		SetAnalysisInputDefaults( analysis_name )

		res_id = ( ExecAnalysis( analysis_name ) )

		print( "Results Name: ", False )

		print( GetResultsName( res_id ) )

	def test_GetResultsSetDoc(self):
		#==== Analysis: VSPAero Compute Geometry ====//
		analysis_name = "VSPAEROComputeGeometry"

		# Set defaults
		SetAnalysisInputDefaults( analysis_name )

		res_id = ( ExecAnalysis( analysis_name ) )

		print( "Results doc: ", False )

		print( GetResultsSetDoc( res_id ) )

	def test_FindResultsID(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		if  len(res_id) == 0 : print( "---> Error: API FindResultsID" )

	def test_FindLatestResultsID(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		results_array = GetAllResultsNames()

		for i in range(int( len(results_array) )):

			resid = FindLatestResultsID( results_array[i] )
			PrintResults( resid )

	def test_GetNumData(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		if ( GetNumData( res_id, "Test_Int" ) != 2 ): print( "---> Error: API GetNumData " )

		int_arr = GetIntResults( res_id, "Test_Int", 0 )

		if  int_arr[0] != 1 : print( "---> Error: API GetIntResults" )

		int_arr = GetIntResults( res_id, "Test_Int", 1 )

		if  int_arr[0] != 2 : print( "---> Error: API GetIntResults" )

	def test_GetResultsType(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		res_array = GetAllDataNames( res_id )

		for j in range(int( len(res_array) )):

			typ = GetResultsType( res_id, res_array[j] )

	def test_GetIntResults(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		if ( GetNumData( res_id, "Test_Int" ) != 2 ): print( "---> Error: API GetNumData " )

		int_arr = GetIntResults( res_id, "Test_Int", 0 )

		if  int_arr[0] != 1 : print( "---> Error: API GetIntResults" )

		int_arr = GetIntResults( res_id, "Test_Int", 1 )

		if  int_arr[0] != 2 : print( "---> Error: API GetIntResults" )

	def test_GetDoubleResults(self):
		#==== Add Pod Geom ====//
		pid = AddGeom( "POD", "" )

		#==== Run CompGeom And View Results ====//
		mesh_id = ComputeCompGeom( SET_ALL, False, 0 )                      # Half Mesh false and no file export

		comp_res_id = FindLatestResultsID( "Comp_Geom" )                    # Find Results ID

		double_arr = GetDoubleResults( comp_res_id, "Wet_Area" )    # Extract Results

	def test_GetStringResults(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		res_id = FindResultsID( "Test_Results" )

		str_arr = GetStringResults( res_id, "Test_String" )

		if ( str_arr[0] != "This Is A Test" ): print( "---> Error: API GetStringResults" )

	def test_GetVec3dResults(self):
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

	def test_CreateGeomResults(self):
		#==== Test Comp Geom ====//
		gid1 = AddGeom( "POD", "" )

		mesh_id = ComputeCompGeom( 0, False, 0 )

		#==== Test Comp Geom Mesh Results ====//
		mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )

		int_arr = GetIntResults( mesh_geom_res_id, "Num_Tris" )

		if  int_arr[0] < 4 : print( "---> Error: API CreateGeomResults" )

	def test_DeleteAllResults(self):
		#==== Test Comp Geom ====//
		gid1 = AddGeom( "POD", "" )

		mesh_id = ComputeCompGeom( 0, False, 0 )

		#==== Test Comp Geom Mesh Results ====//
		mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )

		DeleteAllResults()

		if ( GetNumResults( "Comp_Mesh" ) != 0 ): print( "---> Error: API DeleteAllResults" )

	def test_DeleteResult(self):
		#==== Test Comp Geom ====//
		gid1 = AddGeom( "POD", "" )

		mesh_id = ComputeCompGeom( 0, False, 0 )

		#==== Test Comp Geom Mesh Results ====//
		mesh_geom_res_id = CreateGeomResults( mesh_id, "Comp_Mesh" )

		DeleteResult( mesh_geom_res_id )

		if ( GetNumResults( "Comp_Mesh" ) != 0 ): print( "---> Error: API DeleteResult" )

	def test_WriteResultsCSVFile(self):
		# Add Pod Geom
		pid = AddGeom( "POD" )

		analysis_name = "VSPAEROComputeGeometry"

		rid = ExecAnalysis( analysis_name )

		WriteResultsCSVFile( rid, "CompGeomRes.csv" )

	def test_PrintResults(self):
		# Add Pod Geom
		pid = AddGeom( "POD" )

		analysis_name = "VSPAEROComputeGeometry"

		rid = ExecAnalysis( analysis_name )

		# Get & Display Results
		PrintResults( rid )

	def test_PrintResultsDocs(self):
		# Add Pod Geom
		pid = AddGeom( "POD" )

		analysis_name = "VSPAEROComputeGeometry"

		rid = ExecAnalysis( analysis_name )

		# Get & Display Results Docs
		PrintResultsDocs( rid )

	def test_WriteTestResults(self):
		#==== Write Some Fake Test Results =====//
		WriteTestResults()

		results_array = GetAllResultsNames()

		for i in range( len( results_array ) ):
			resid = FindLatestResultsID( results_array[i] )
			PrintResults( resid )

	def test_InitGUI(self):

		InitGUI()

	def test_StartGUI(self):

		StartGUI()

	def test_EnableStopGUIMenuItem(self):

		EnableStopGUIMenuItem()
		StartGUI()


	def test_DisableStopGUIMenuItem(self):

		EnableStopGUIMenuItem()
		DisableStopGUIMenuItem()
		StartGUI()


	def test_StopGUI(self):

		StartGUI()

		StopGUI()

		StartGUI()


	def test_PopupMsg(self):

		StartGUI()

		PopupMsg( "This is a popup message." )


	def test_UpdateGUI(self):

		StartGUI()

		pod_id = AddGeom( "POD" )

		length = FindParm( pod_id, "Length", "Design" )

		SetParmVal( length, 13.0 )

		UpdateGUI()


	def test_IsGUIBuild(self):

		if ( IsGUIBuild() ):
			print( "OpenVSP build is graphics capable." )
		else:
			print( "OpenVSP build is not graphics capable." )


	def test_Lock(self):

		StartGUI()

		pod_id = AddGeom( "POD" )

		Lock()
		rid = ExecAnalysis( "CompGeom" )

		mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )

		DeleteGeomVec( mesh_id_vec )
		Unlock()


	def test_Unlock(self):

		StartGUI()

		pod_id = AddGeom( "POD" )

		Lock()
		rid = ExecAnalysis( "CompGeom" )

		mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )

		DeleteGeomVec( mesh_id_vec )
		Unlock()


	def test_IsEventLoopRunning(self):

		StartGUI()

		if ( IsEventLoopRunning() ):
			print( "Event loop is running." )

	def test_ScreenGrab(self):
		screenw = 2000                                             # Set screenshot width and height
		screenh = 2000

		fname = "test_screen_grab.png"

		ScreenGrab( fname, screenw, screenh, True, True )                # Take PNG screenshot

	def test_SetViewAxis(self):
		SetViewAxis( False )                                           # Turn off axis marker in corner of viewscreen

	def test_SetShowBorders(self):
		SetShowBorders( False )                                        # Turn off red/black border on active window

	def test_SetGeomDrawType(self):
		pid = AddGeom( "POD", "" )                             # Add Pod for testing

		SetGeomDrawType( pid, GEOM_DRAW_SHADE )                       # Make pod appear as shaded

	def test_SetGeomWireColor(self):
		pid = AddGeom( "POD", "" )

		SetGeomWireColor( pid, 0, 0, 255 )

	def test_SetGeomDisplayType(self):
		pid = AddGeom( "POD" )                             # Add Pod for testing

		SetGeomDisplayType( pid, DISPLAY_DEGEN_PLATE )                       # Make pod appear as Bezier plate (Degen Geom)

	def test_SetGeomMaterialName(self):
		pid = AddGeom( "POD" )

		SetGeomMaterialName( pid, "Ruby" )
	def test_AddMaterial(self):
		pid = AddGeom( "POD" )

		AddMaterial( "RedGlass", vec3d( 44, 2, 2 ), vec3d( 156, 10, 10 ), vec3d( 185, 159, 159 ), vec3d( 44, 2, 2 ), 30, 0.4 )

		SetGeomMaterialName( pid, "RedGlass" )
	def test_GetMaterialNames(self):
		mat_array = GetMaterialNames()

		for i in range(int( len(mat_array) )):
			print( mat_array[i] )

	def test_SetBackground(self):
		SetBackground( 1.0, 1.0, 1.0 )                                 # Set background to bright white

	def test_SetAllViews(self):
		SetAllViews( CAM_CENTER )

	def test_SetView(self):
		SetView( 0, CAM_CENTER )

	def test_FitAllViews(self):
		FitAllViews()

	def test_ResetViews(self):
		ResetViews()

	def test_SetWindowLayout(self):
		SetWindowLayout( 2, 2 )

	def test_SetGUIElementDisable(self):
		SetGUIElementDisable( GDEV_INPUT, True )
	def test_SetGUIScreenDisable(self):
		SetGUIScreenDisable( VSP_CFD_MESH_SCREEN, True )
	def test_SetGeomScreenDisable(self):
		SetGeomScreenDisable( ALL_GEOM_SCREENS, True )
	def test_HideScreen(self):
		HideScreen( VSP_INTERFERENCE_SCREEN )
	def test_ShowScreen(self):
		ShowScreen( VSP_INTERFERENCE_SCREEN )
	def test_GetGeomTypes(self):
		#==== Add Pod Geometries ====//
		pod1 = AddGeom( "POD", "" )
		pod2 = AddGeom( "POD", "" )

		type_array = GetGeomTypes()

		if ( type_array[0] != "POD" ): print( "---> Error: API GetGeomTypes  " )

	def test_AddGeom(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

	def test_UpdateGeom(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		SetParmVal( pod_id, "X_Rel_Location", "XForm", 5.0 )

		UpdateGeom( pod_id ) # Faster than updating the whole vehicle

	def test_DeleteGeom(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		DeleteGeom( wing_id )

	def test_DeleteGeomVec(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		rid = ExecAnalysis( "CompGeom" )

		mesh_id_vec = GetStringResults( rid, "Mesh_GeomID" )

		DeleteGeomVec( mesh_id_vec )

	def test_CutGeomToClipboard(self):
		#==== Add Pod Geometries ====//
		pid1 = AddGeom( "POD", "" )
		pid2 = AddGeom( "POD", "" )

		CutGeomToClipboard( pid1 )

		PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2

		geom_ids = FindGeoms()

		if  len(geom_ids) != 2 : print( "---> Error: API Cut/Paste Geom  " )

	def test_CopyGeomToClipboard(self):
		#==== Add Pod Geometries ====//
		pid1 = AddGeom( "POD", "" )
		pid2 = AddGeom( "POD", "" )

		CopyGeomToClipboard( pid1 )

		PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2

		geom_ids = FindGeoms()

		if  len(geom_ids) != 3 : print( "---> Error: API Copy/Paste Geom  " )

	def test_PasteGeomClipboard(self):
		#==== Add Pod Geometries ====//
		pid1 = AddGeom( "POD", "" )
		pid2 = AddGeom( "POD", "" )

		CutGeomToClipboard( pid1 )

		PasteGeomClipboard( pid2 ) # Paste Pod 1 as child of Pod 2

		geom_ids = FindGeoms()

		if  len(geom_ids) != 2 : print( "---> Error: API Cut/Paste Geom  " )

	def test_FindGeoms(self):
		#==== Add Pod Geometries ====//
		pod1 = AddGeom( "POD", "" )
		pod2 = AddGeom( "POD", "" )

		#==== There Should Be Two Geoms =====//
		geom_ids = FindGeoms()

		if  len(geom_ids) != 2 : print( "---> Error: API FindGeoms " )

	def test_FindGeomsWithName(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		SetGeomName( pid, "ExamplePodName" )

		geom_ids = FindGeomsWithName( "ExamplePodName" )

		if  len(geom_ids) != 1 :
			print( "---> Error: API FindGeomsWithName " )

	def test_FindGeom(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		SetGeomName( pid, "ExamplePodName" )

		geom_id = FindGeom( "ExamplePodName", 0 )

		geom_ids = FindGeomsWithName( "ExamplePodName" )

		if  geom_ids[0] != geom_id :
			print( "---> Error: API FindGeom & FindGeomsWithName" )

	def test_SetGeomName(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		SetGeomName( pid, "ExamplePodName" )

		geom_ids = FindGeomsWithName( "ExamplePodName" )

		if  len(geom_ids) != 1 :
			print( "---> Error: API FindGeomsWithName " )

	def test_GetGeomName(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		SetGeomName( pid, "ExamplePodName" )

		name_str = "Geom Name: " + GetGeomName( pid )

		print( name_str )

	def test_GetGeomParmIDs(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD", "" )

		print( "---> Test Get Parm Arrays" )

		parm_array = GetGeomParmIDs( pid )

		if  len(parm_array) < 1 : print( "---> Error: API GetGeomParmIDs " )

	def test_GetGeomTypeName(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		print( "Geom Type Name: ", False )

		print( GetGeomTypeName( wing_id ) )

	def test_GetParm(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		lenid = GetParm( pid, "Length", "Design" )

		if  not ValidParm( lenid ) : print( "---> Error: API GetParm  " )

	def test_SetGeomParent(self):
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

	def test_GetGeomParent(self):
		#==== Add Parent and Child Geometry ====//
		pod1 = AddGeom( "POD" )

		pod2 = AddGeom( "POD", pod1 )

		print( "Parent ID of Pod #2: ", False )

		print( GetGeomParent( pod2 ) )

	def test_GetGeomChildren(self):
		#==== Add Parent and Child Geometry ====//
		pod1 = AddGeom( "POD" )

		pod2 = AddGeom( "POD", pod1 )

		pod3 = AddGeom( "POD", pod2 )

		print( "Children of Pod #1: " )

		children = GetGeomChildren( pod1 )

		for i in range(int( len(children) )):

			print( "\t", False )
			print( children[i] )

	def test_GetNumXSecSurfs(self):
		#==== Add Fuselage Geometry ====//
		fuseid = AddGeom( "FUSELAGE", "" )

		num_xsec_surfs = GetNumXSecSurfs( fuseid )

		if  num_xsec_surfs != 1 : print( "---> Error: API GetNumXSecSurfs  " )

	def test_GetNumMainSurfs(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		num_surf = 0

		num_surf = GetNumMainSurfs( prop_id ) # Should be the same as the number of blades

		print( "Number of Propeller Surfaces: ", False )

		print( num_surf )

	def test_GetTotalNumSurfs(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		num_surf = 0

		num_surf = GetTotalNumSurfs( wing_id ) # Wings default with XZ symmetry on -> 2 surfaces

		print( "Total Number of Wing Surfaces: ", False )

		print( num_surf )

	def test_GetGeomVSPSurfType(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		if  GetGeomVSPSurfType( wing_id ) != WING_SURF :
			print( "---> Error: API GetGeomVSPSurfType " )

	def test_GetGeomVSPSurfCfdType(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		if  GetGeomVSPSurfCfdType( wing_id ) != CFD_NORMAL :
			print( "---> Error: API GetGeomVSPSurfCfdType " )

	def test_GetGeomBBoxMax(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		SetParmVal( FindParm( pid, "Y_Rotation", "XForm" ), 45 )
		SetParmVal( FindParm( pid, "Z_Rotation", "XForm" ), 25 )

		Update()

		max_pnt = GetGeomBBoxMax( pid, 0, False )

	def test_GetGeomBBoxMin(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		SetParmVal( FindParm( pid, "Y_Rotation", "XForm" ), 45 )
		SetParmVal( FindParm( pid, "Z_Rotation", "XForm" ), 25 )

		Update()

		min_pnt = GetGeomBBoxMin( pid, 0, False )

	def test_AddSubSurf(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		# Note: Parm Group for SubSurfaces in the form: "SS_" + type + "_" + count (initialized at 1)
		ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line

		SetParmVal( wid, "Const_Line_Value", "SubSurface_1", 0.4 )     # Change Location

	def test_GetSubSurf(self):
		wid = AddGeom( "WING", "" ) # Add Wing

		ss_rec_1 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #1

		ss_rec_2 = AddSubSurf( wid, SS_RECTANGLE ) # Add Sub Surface Rectangle #2

		print( ss_rec_2, False )

		print( " = ", False )

		print( GetSubSurf( wid, 1 ) )

	def test_DeleteSubSurf(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
		ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle

		print("Delete SS_Line\n")

		DeleteSubSurf( wid, ss_line_id )

		num_ss = GetNumSubSurf( wid )

		num_str = f"Number of SubSurfaces: {num_ss}\n"

		print( num_str )

	def test_SetSubSurfName(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle

		new_name = "New_SS_Rec_Name"

		SetSubSurfName( wid, ss_rec_id, new_name )

	def test_GetSubSurfName(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle

		rec_name = GetSubSurfName( wid, ss_rec_id )

		name_str = "Current Name of SS_Rectangle: " + rec_name + "\n"

		print( name_str )

	def test_GetSubSurfIndex(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
		ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle

		ind = GetSubSurfIndex( ss_rec_id )

		ind_str = f"Index of SS_Rectangle: {ind}"

		print( ind_str )

	def test_GetSubSurfIDVec(self):
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

	def test_GetNumSubSurf(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line
		ss_rec_id = AddSubSurf( wid, SS_RECTANGLE )                        # Add Sub Surface Rectangle

		num_ss = GetNumSubSurf( wid )

		num_str = "Number of SubSurfaces: {num_ss}"

		print( num_str )

	def test_GetSubSurfType(self):
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

	def test_GetSubSurfParmIDs(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		ss_line_id = AddSubSurf( wid, SS_LINE )                      # Add Sub Surface Line

		# Get and list all Parm info for SS_Line
		parm_id_vec = GetSubSurfParmIDs( ss_line_id )

		for i in range(len(parm_id_vec)):

			id_name_str = "\tName: " + GetParmName(parm_id_vec[i]) + ", Group: " + GetParmDisplayGroupName(parm_id_vec[i]) + ", ID: " + str(parm_id_vec[i]) + "\n"


			print( id_name_str )

	def test_AddFeaStruct(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

	def test_SetFeaMeshStructIndex(self):

		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		SetFeaMeshStructIndex( struct_ind )

		if  len(FindGeoms()) != 0 : print( "ERROR: VSPRenew" )

	def test_DeleteFeaStruct(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind_1 = AddFeaStruct( pod_id )

		struct_ind_2 = AddFeaStruct( pod_id )

		DeleteFeaStruct( pod_id, struct_ind_1 )

	def test_GetFeaStructID(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind )

	def test_GetFeaStructIndex(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind_1 = AddFeaStruct( pod_id )

		struct_ind_2 = AddFeaStruct( pod_id )

		struct_id_2 = GetFeaStructID( pod_id, struct_ind_2 )

		DeleteFeaStruct( pod_id, struct_ind_1 )

		struct_ind_2_new = GetFeaStructIndex( struct_id_2 )

	def test_GetFeaStructParentGeomID(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind )

		#==== Get Parent Geom ID and Index ====//
		parent_id = GetFeaStructParentGeomID( struct_id )

	def test_GetFeaStructName(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Get Structure Name ====//
		parm_container_name = GetFeaStructName( pod_id, struct_ind )

		display_name = "Current Structure Parm Container Name: " + parm_container_name + "\n"

		print( display_name )

	def test_SetFeaStructName(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Change the Structure Name ====//
		SetFeaStructName( pod_id, struct_ind, "Example_Struct" )

		parm_container_id = FindContainer( "Example_Struct", struct_ind )

		display_id = "New Structure Parm Container ID: " + parm_container_id + "\n"

		print( display_id )

	def test_GetFeaStructIDVec(self):
		#==== Add Geometries ====//
		pod_id = AddGeom( "POD" )
		wing_id = AddGeom( "WING" )

		#==== Add FeaStructures ====//
		pod_struct_ind = AddFeaStruct( pod_id )
		wing_struct_ind = AddFeaStruct( wing_id )

		struct_id_vec = GetFeaStructIDVec()

	def test_SetFeaPartName(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Add Bulkead ====//
		bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )

		SetFeaPartName( bulkhead_id, "Bulkhead" )

	def test_AddFeaPart(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Add Bulkead ====//
		bulkhead_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )

		SetParmVal( FindParm( bulkhead_id, "IncludedElements", "FeaPart" ), FEA_SHELL_AND_BEAM )

		SetParmVal( FindParm( bulkhead_id, "RelCenterLocation", "FeaPart" ), 0.15 )

	def test_DeleteFeaPart(self):
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

	def test_GetFeaPartID(self):
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

	def test_GetFeaPartName(self):
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

	def test_GetFeaPartType(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Add Slice ====//
		slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )

		if  FEA_SLICE != GetFeaPartType( slice_id ) : # These should be equivalent

			print( "Error: GetFeaPartType" )

	def test_GetFeaPartIDVec(self):
		#==== Add Geometries ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind )

		#==== Add FEA Parts ====//
		slice_id = AddFeaPart( pod_id, struct_ind, FEA_SLICE )
		dome_id = AddFeaPart( pod_id, struct_ind, FEA_DOME )

		part_id_vec = GetFeaPartIDVec( struct_id ) # Should include slice_id & dome_id

	def test_GetFeaSubSurfIDVec(self):
		#==== Add Geometries ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind )

		#==== Add SubSurfaces ====//
		line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )
		rectangle_id = AddFeaSubSurf( pod_id, struct_ind, SS_RECTANGLE )

		part_id_vec = GetFeaSubSurfIDVec( struct_id ) # Should include line_array_id & rectangle_id

	def test_SetFeaPartPerpendicularSparID(self):
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

	def test_GetFeaPartPerpendicularSparID(self):
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

	def test_SetFeaSubSurfName(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Add LineArray ====//
		line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )

		SetFeaSubSurfName( line_array_id, "Stiffener_array" )

	def test_GetFeaSubSurfName(self):
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

	def test_AddFeaSubSurf(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Add LineArray ====//
		line_array_id = AddFeaSubSurf( pod_id, struct_ind, SS_LINE_ARRAY )

		SetParmVal( FindParm( line_array_id, "ConstLineType", "SS_LineArray" ), 1 ) # Constant W

		SetParmVal( FindParm( line_array_id, "Spacing", "SS_LineArray" ), 0.25 )

	def test_DeleteFeaSubSurf(self):
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

	def test_GetFeaSubSurfIndex(self):
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

	def test_NumFeaStructures(self):
		#==== Add Pod Geometry ====//
		wing_id = AddGeom( "WING" )

		#==== Add FeaStructure to Pod ====//
		struct_1 = AddFeaStruct( wing_id )
		struct_2 = AddFeaStruct( wing_id )

		if  NumFeaStructures() != 2 :
			print( "Error: NumFeaStructures" )

	def test_NumFeaParts(self):
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

	def test_NumFeaSubSurfs(self):
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

	def test_AddFeaBC(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind );

		#==== Add BC ====//
		bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )

	def test_DelFeaBC(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind );

		#==== Add BC ====//
		bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )

		DelFeaBC( struct_id, bc_id )

	def test_GetFeaBCIDVec(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind );

		#==== Add BC ====//
		bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )

		bc_id_vec = GetFeaBCIDVec( struct_id )

	def test_NumFeaBCs(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		struct_id = GetFeaStructID( pod_id, struct_ind );

		#==== Add BC ====//
		bc_id = AddFeaBC( struct_id, FEA_BC_STRUCTURE )

		nbc = NumFeaBCs( struct_id )

	def test_AddFeaMaterial(self):
		#==== Create FeaMaterial ====//
		mat_id = AddFeaMaterial()

		SetParmVal( FindParm( mat_id, "MassDensity", "FeaMaterial" ), 0.016 )

	def test_AddFeaProperty(self):
		#==== Create FeaProperty ====//
		prop_id = AddFeaProperty()

		SetParmVal( FindParm( prop_id, "Thickness", "FeaProperty" ), 0.01 )

	def test_SetFeaMeshVal(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		#==== Add FeaStructure to Pod ====//
		struct_ind = AddFeaStruct( pod_id )

		#==== Adjust FeaMeshSettings ====//
		SetFeaMeshVal( pod_id, struct_ind, CFD_MAX_EDGE_LEN, 0.75 )

		SetFeaMeshVal( pod_id, struct_ind, CFD_MIN_EDGE_LEN, 0.2 )

	def test_SetFeaMeshFileName(self):
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

	def test_ComputeFeaMesh(self):
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

	def test_SetXSecAlias(self):
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

	def test_GetXSecAlias(self):
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

	def test_SetXSecCurveAlias(self):
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

	def test_GetXSecCurveAlias(self):
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

	def test_CutXSec(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		#==== Insert, Cut, Paste Example ====//
		InsertXSec( fid, 1, XS_ROUNDED_RECTANGLE )         # Insert A Cross-Section

		CopyXSec( fid, 2 )                                 # Copy Just Created XSec To Clipboard

		PasteXSec( fid, 1 )                                # Paste Clipboard

		CutXSec( fid, 2 )                                  # Cut Created XSec

	def test_CopyXSec(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Copy XSec To Clipboard
		CopyXSec( sid, 1 )

		# Paste To XSec 3
		PasteXSec( sid, 3 )

	def test_PasteXSec(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Copy XSec To Clipboard
		CopyXSec( sid, 1 )

		# Paste To XSec 3
		PasteXSec( sid, 3 )

	def test_InsertXSec(self):
		wing_id = AddGeom( "WING" )

		#===== Add XSec ====//
		InsertXSec( wing_id, 1, XS_SIX_SERIES )

	def test_SplitWingXSec(self):
		wing_id = AddGeom( "WING", "" )

		#==== Set Wing Section Controls ====//
		SplitWingXSec( wing_id, 1 )

		Update()
	def test_SetDriverGroup(self):
		#==== Add Wing Geometry and Set Parms ====//
		wing_id = AddGeom( "WING", "" )

		#==== Set Wing Section Controls ====//
		SetDriverGroup( wing_id, 1, AR_WSECT_DRIVER, ROOTC_WSECT_DRIVER, TIPC_WSECT_DRIVER )

		Update()

		#==== Set Parms ====//
		SetParmVal( wing_id, "Root_Chord", "XSec_1", 2 )
		SetParmVal( wing_id, "Tip_Chord", "XSec_1", 1 )

		Update()

	def test_GetXSecSurf(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

	def test_GetNumXSec(self):
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

	def test_GetXSec(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Identify XSec 1
		xsec_1 = GetXSec( xsec_surf, 1 )

	def test_ChangeXSecShape(self):
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

	def test_GetXSecShape(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )

		xsec = GetXSec( xsec_surf, 1 )

		if  GetXSecShape( xsec ) != XS_EDIT_CURVE : print( "ERROR: GetXSecShape" )

	def test_GetXSecWidth(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 2 ) # Get 2nd to last XSec

		SetXSecWidthHeight( xsec, 3.0, 6.0 )

		if  abs( GetXSecWidth( xsec ) - 3.0 ) > 1e-6 : print( "---> Error: API Get/Set Width " )

	def test_GetXSecHeight(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 2 ) # Get 2nd to last XSec

		SetXSecWidthHeight( xsec, 3.0, 6.0 )

		if  abs( GetXSecHeight( xsec ) - 6.0 ) > 1e-6 : print( "---> Error: API Get/Set Width " )

	def test_SetXSecWidthHeight(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Identify XSec 2
		xsec_2 = GetXSec( xsec_surf, 2 )

		SetXSecWidthHeight( xsec_2, 1.5, 1.5 )

	def test_SetXSecWidth(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Identify XSec 2
		xsec_2 = GetXSec( xsec_surf, 2 )

		SetXSecWidth( xsec_2, 1.5 )

	def test_SetXSecHeight(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Identify XSec 2
		xsec_2 = GetXSec( xsec_surf, 2 )

		SetXSecHeight( xsec_2, 1.5 )

	def test_GetXSecParmIDs(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		parm_array = GetXSecParmIDs( xsec )

		if  len(parm_array) < 1 : print( "---> Error: API GetXSecParmIDs " )

	def test_GetXSecParm(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		if  not ValidParm( wid ) : print( "---> Error: API GetXSecParm " )

	def test_ReadFileXSec(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, 2, XS_FILE_FUSE )

		xsec = GetXSec( xsec_surf, 2 )

		vec_array = ReadFileXSec(xsec, "TestXSec.fxs")


	def test_SetXSecPnts(self):
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

	def test_ComputeXSecPnt(self):
		#==== Add Geom ====//
		stack_id = AddGeom( "STACK" )

		#==== Get The XSec Surf ====//
		xsec_surf = GetXSecSurf( stack_id, 0 )

		xsec = GetXSec( xsec_surf, 2 )

		u_fract = 0.25

		pnt = ComputeXSecPnt(xsec, u_fract)


	def test_ComputeXSecTan(self):
		#==== Add Geom ====//
		stack_id = AddGeom( "STACK" )

		#==== Get The XSec Surf ====//
		xsec_surf = GetXSecSurf( stack_id, 0 )

		xsec = GetXSec( xsec_surf, 2 )

		u_fract = 0.25

		tan = ComputeXSecTan( xsec, u_fract )

	def test_ResetXSecSkinParms(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf

		num_xsecs = GetNumXSec( xsec_surf )

		xsec = GetXSec( xsec_surf, 1 )

		SetXSecTanAngles( xsec, XSEC_BOTH_SIDES, 0.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Angles At Cross Section
		SetXSecContinuity( xsec, 1 )                       # Set Continuity At Cross Section

		ResetXSecSkinParms( xsec )

	def test_SetXSecContinuity(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		xsec_surf = GetXSecSurf( fid, 0 )           # Get First (and Only) XSec Surf

		num_xsecs = GetNumXSec( xsec_surf )

		for i in range(num_xsecs):

			xsec = GetXSec( xsec_surf, i )

			SetXSecContinuity( xsec, 1 )                       # Set Continuity At Cross Section

	def test_SetXSecTanAngles(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		num_xsecs = GetNumXSec( xsec_surf )

		for i in range(num_xsecs):

			xsec = GetXSec( xsec_surf, i )

			SetXSecTanAngles( xsec, XSEC_BOTH_SIDES, 10.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Angles At Cross Section

	def test_SetXSecTanSlews(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		num_xsecs = GetNumXSec( xsec_surf )

		for i in range(num_xsecs):

			xsec = GetXSec( xsec_surf, i )

			SetXSecTanSlews( xsec, XSEC_BOTH_SIDES, 5.0, -1.0e12, -1.0e12, -1.0e12 )       # Set Tangent Slews At Cross Section

	def test_SetXSecTanStrengths(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Flatten ends
		num_xsecs = GetNumXSec( xsec_surf )

		for i in range(num_xsecs):

			xsec = GetXSec( xsec_surf, i )

			SetXSecTanStrengths( xsec, XSEC_BOTH_SIDES, 0.8, -1.0e12, -1.0e12, -1.0e12 )  # Set Tangent Strengths At Cross Section

	def test_SetXSecCurvatures(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		# Flatten ends
		num_xsecs = GetNumXSec( xsec_surf )

		for i in range(num_xsecs):

			xsec = GetXSec( xsec_surf, i )

			SetXSecCurvatures( xsec, XSEC_BOTH_SIDES, 0.2, -1.0e12, -1.0e12, -1.0e12 )  # Set Tangent Strengths At Cross Section

	def test_ReadFileAirfoil(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )

		xsec = GetXSec( xsec_surf, 1 )

		ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )

	def test_SetAirfoilUpperPnts(self):
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

	def test_SetAirfoilLowerPnts(self):
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

	def test_SetAirfoilPnts(self):
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

	def test_GetHersheyBarLiftDist(self):
		pi = 3.14159265358979323846
		# Compute theoretical lift and drag distributions using 100 points
		Vinf = 100

		halfAR = 20

		alpha_deg = 10

		n_pts = 100

		cl_dist_theo = GetHersheyBarLiftDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )

		cd_dist_theo = GetHersheyBarDragDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )

	def test_GetHersheyBarDragDist(self):
		pi = 3.14159265358979323846
		# Compute theoretical lift and drag distributions using 100 points
		Vinf = 100

		halfAR = 20

		alpha_deg = 10

		n_pts = 100

		cl_dist_theo = GetHersheyBarLiftDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )

		cd_dist_theo = GetHersheyBarDragDist( int( n_pts ), alpha_deg*pi/180, Vinf, ( 2 * halfAR ), False )

	def test_GetVKTAirfoilPnts(self):
		pi = 3.14159265358979323846

		npts = 122

		alpha = 0.0

		epsilon = 0.1

		kappa = 0.1

		tau = 10

		xyz_airfoil = GetVKTAirfoilPnts(npts, alpha, epsilon, kappa, tau*(pi/180) )

		cp_dist = GetVKTAirfoilCpDist( alpha, epsilon, kappa, tau*(pi/180), xyz_airfoil )

	def test_GetVKTAirfoilCpDist(self):
		pi = 3.14159265358979323846

		npts = 122

		alpha = 0.0

		epsilon = 0.1

		kappa = 0.1

		tau = 10

		xyz_airfoil = GetVKTAirfoilPnts(npts, alpha, epsilon, kappa, tau*(pi/180) )

		cp_dist = GetVKTAirfoilCpDist( alpha, epsilon, kappa, tau*(pi/180), xyz_airfoil )

	def test_GetEllipsoidCpDist(self):
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

	def test_GetAirfoilUpperPnts(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )

		xsec = GetXSec( xsec_surf, 1 )

		ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )

		up_array = GetAirfoilUpperPnts( xsec )

	def test_GetAirfoilLowerPnts(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, 1, XS_FILE_AIRFOIL )

		xsec = GetXSec( xsec_surf, 1 )

		ReadFileAirfoil( xsec, "airfoil/N0012_VSP.af" )

		low_array = GetAirfoilLowerPnts( xsec )

	def test_AddBackground3D(self):
		nbg = GetNumBackground3Ds()

		# Add Background3D
		bg_id = AddBackground3D()

		if GetNumBackground3Ds() != nbg + 1 :
			print( "ERROR: AddBackground3D" )

		DelBackground3D( bg_id )
	def test_GetNumBackground3Ds(self):
		nbg = GetNumBackground3Ds()

		# Add Background3D
		bg_id = AddBackground3D()

		if GetNumBackground3Ds() != nbg + 1 :
			print( "ERROR: AddBackground3D" )

		DelBackground3D( bg_id )
	def test_GetAllBackground3Ds(self):
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
	def test_ShowAllBackground3Ds(self):
		# Add Background3D
		AddBackground3D()
		AddBackground3D()
		AddBackground3D()

		ShowAllBackground3Ds()

		DelAllBackground3Ds()
	def test_HideAllBackground3Ds(self):
		# Add Background3D
		AddBackground3D()
		AddBackground3D()
		AddBackground3D()

		HideAllBackground3Ds()

		DelAllBackground3Ds()
	def test_DelAllBackground3Ds(self):
		# Add Background3D
		AddBackground3D()
		AddBackground3D()
		AddBackground3D()

		DelAllBackground3Ds()

		nbg = GetNumBackground3Ds()

		if nbg != 0 :
			print( "ERROR: DelAllBackground3Ds" )

	def test_DelBackground3D(self):
		# Add Background3D
		AddBackground3D()
		bg_id = AddBackground3D()
		AddBackground3D()

		nbg = GetNumBackground3Ds()

		DelBackground3D( bg_id )

		if GetNumBackground3Ds() != nbg -1 :
			print( "ERROR: DelBackground3D" )

	def test_GetAllBackground3DRelativePaths(self):
		# Add Background3D
		AddBackground3D()
		AddBackground3D()
		AddBackground3D()

		bg_file_array = GetAllBackground3DRelativePaths()

		for n in range( len( bg_file_array ) ):
			print( bg_file_array[n] )

		DelAllBackground3Ds()
	def test_GetAllBackground3DAbsolutePaths(self):
		# Add Background3D
		AddBackground3D()
		AddBackground3D()
		AddBackground3D()

		bg_file_array = GetAllBackground3DAbsolutePaths()

		for n in range( len( bg_file_array ) ):
			print( bg_file_array[n] )

		DelAllBackground3Ds()
	def test_GetBackground3DRelativePath(self):
		# Add Background3D
		bg_id = AddBackground3D()

		SetBackground3DRelativePath( bg_id, "front.png" )
		bg_file = GetBackground3DRelativePath( bg_id )

		print( bg_file )

		DelAllBackground3Ds()
	def test_GetBackground3DAbsolutePath(self):
		# Add Background3D
		bg_id = AddBackground3D()

		SetBackground3DAbsolutePath( bg_id, "/user/me/vsp_work/front.png" )
		bg_file = GetBackground3DAbsolutePath( bg_id )

		print( bg_file )

		DelAllBackground3Ds()
	def test_SetBackground3DRelativePath(self):
		# Add Background3D
		bg_id = AddBackground3D()

		SetBackground3DRelativePath( bg_id, "front.png" )
		bg_file = GetBackground3DRelativePath( bg_id )

		print( bg_file )

		DelAllBackground3Ds()
	def test_SetBackground3DAbsolutePath(self):
		# Add Background3D
		bg_id = AddBackground3D()

		SetBackground3DAbsolutePath( bg_id, "front.png" )
		bg_file = GetBackground3DAbsolutePath( bg_id )

		print( bg_file )

		DelAllBackground3Ds()
	def test_GetNumRoutingPts(self):
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
	def test_AddRoutingPt(self):
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
	def test_InsertRoutingPt(self):
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
	def test_DelRoutingPt(self):
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
	def test_DelAllRoutingPt(self):
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
	def test_MoveRoutingPt(self):
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
	def test_GetRoutingPtID(self):
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
	def test_GetAllRoutingPtIds(self):
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
	def test_GetRoutingPtParentID(self):
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
	def test_SetRoutingPtParentID(self):
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
	def test_GetMainRoutingPtCoord(self):
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
	def test_GetRoutingPtCoord(self):
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
	def test_GetAllRoutingPtCoords(self):
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
	def test_GetRoutingCurve(self):
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
	def test_ChangeBORXSecShape(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_ROUNDED_RECTANGLE )

		if  GetBORXSecShape( bor_id ) != XS_ROUNDED_RECTANGLE : print( "ERROR: ChangeBORXSecShape" )

	def test_GetBORXSecShape(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_ROUNDED_RECTANGLE )

		if  GetBORXSecShape( bor_id ) != XS_ROUNDED_RECTANGLE : print( "ERROR: GetBORXSecShape" )

	def test_ReadBORFileXSec(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_FUSE )

		vec_array = ReadBORFileXSec( bor_id, "TestXSec.fxs" )

	def test_SetBORXSecPnts(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_FUSE )

		vec_array = ReadBORFileXSec( bor_id, "TestXSec.fxs" )

		if  len(vec_array) > 0 :
			vec_array[1] = vec_array[1] * 2.0
			vec_array[3] = vec_array[3] * 2.0

			SetBORXSecPnts( bor_id, vec_array )

	def test_ComputeBORXSecPnt(self):
		#==== Add Geom ====//
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		u_fract = 0.25

		pnt = ComputeBORXSecPnt( bor_id, u_fract )

	def test_ComputeBORXSecTan(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		u_fract = 0.25

		tan = ComputeBORXSecTan( bor_id, u_fract )

	def test_ReadBORFileAirfoil(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )

		ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )

	def test_SetBORAirfoilUpperPnts(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )

		ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )

		up_array = GetBORAirfoilUpperPnts( bor_id )

		for i in range(int( len(up_array) )):

			up_array[i].scale_y( 2.0 )

		SetBORAirfoilUpperPnts( bor_id, up_array )

	def test_SetBORAirfoilLowerPnts(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )

		ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )

		low_array = GetBORAirfoilLowerPnts( bor_id )

		for i in range(int( len(low_array) )):

			low_array[i].scale_y( 0.5 )

		SetBORAirfoilLowerPnts( bor_id, low_array )

	def test_SetBORAirfoilPnts(self):
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

	def test_GetBORAirfoilUpperPnts(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )

		ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )

		up_array = GetBORAirfoilUpperPnts( bor_id )

	def test_GetBORAirfoilLowerPnts(self):
		# Add Body of Recolution
		bor_id = AddGeom( "BODYOFREVOLUTION", "" )

		ChangeBORXSecShape( bor_id, XS_FILE_AIRFOIL )

		ReadBORFileAirfoil( bor_id, "airfoil/N0012_VSP.af" )

		low_array = GetBORAirfoilLowerPnts( bor_id )

	def test_WriteBezierAirfoil(self):
		#==== Add Wing Geometry and Set Parms ====//
		wing_id = AddGeom( "WING", "" )

		u = 0.5 # export airfoil at mid span location

		#==== Write Bezier Airfoil File ====//
		WriteBezierAirfoil( "Example_Bezier.bz", wing_id, u )

	def test_WriteSeligAirfoil(self):
		#==== Add Wing Geometry and Set Parms ====//
		wing_id = AddGeom( "WING", "" )

		u = 0.5 # export airfoil at mid span location

		#==== Write Selig Airfoil File ====//
		WriteSeligAirfoil( "Example_Selig.dat", wing_id, u )

	def test_EditXSecInitShape(self):
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

	def test_EditXSecConvertTo(self):
		# Add Stack
		sid = AddGeom( "STACK", "" )

		# Get First (and Only) XSec Surf
		xsec_surf = GetXSecSurf( sid, 0 )

		ChangeXSecShape( xsec_surf, 1, XS_EDIT_CURVE )

		# Identify XSec 1
		xsec_1 = GetXSec( xsec_surf, 1 )

		# Set XSec 1 to Linear
		EditXSecConvertTo( xsec_1, LINEAR )

	def test_GetEditXSecUVec(self):
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

	def test_GetEditXSecCtrlVec(self):
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

	def test_SetEditXSecPnts(self):
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

	def test_EditXSecDelPnt(self):
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

	def test_EditXSecSplit01(self):
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

	def test_MoveEditXSecPnt(self):
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

	def test_ConvertXSecToEdit(self):
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

	def test_GetEditXSecFixedUVec(self):
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

	def test_SetEditXSecFixedUVec(self):
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

	def test_ReparameterizeEditXSec(self):
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

	def test_GetNumSets(self):
		if  GetNumSets() <= 0 : print( "---> Error: API GetNumSets " )

	def test_SetSetName(self):
		SetSetName( 3, "SetFromScript" )

		if GetSetName(3) != "SetFromScript":
			print("---> Error: API Get/Set Set Name")


	def test_GetSetName(self):
		SetSetName( 3, "SetFromScript" )

		if GetSetName(3) != "SetFromScript":
			print("---> Error: API Get/Set Set Name")

	def test_GetGeomSetAtIndex(self):
		SetSetName( 3, "SetFromScript" )

		geom_arr1 = GetGeomSetAtIndex( 3 )

		geom_arr2 = GetGeomSet( "SetFromScript" )

		if  len(geom_arr1) != len(geom_arr2) : print( "---> Error: API GetGeomSet " )

	def test_GetGeomSet(self):
		SetSetName( 3, "SetFromScript" )

		geom_arr1 = GetGeomSetAtIndex( 3 )

		geom_arr2 = GetGeomSet( "SetFromScript" )

		if  len(geom_arr1) != len(geom_arr2) : print( "---> Error: API GetGeomSet " )

	def test_GetSetIndex(self):
		SetSetName( 3, "SetFromScript" )

		if GetSetIndex("SetFromScript") != 3:
			print("ERROR: GetSetIndex")


	def test_GetSetFlag(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		SetSetFlag( fuseid, 3, True )

		if not GetSetFlag(fuseid, 3):
			print("---> Error: API Set/Get Set Flag")


	def test_SetSetFlag(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		SetSetFlag( fuseid, 3, True )

		if not GetSetFlag(fuseid, 3):
			print("---> Error: API Set/Get Set Flag")


	def test_CopyPasteSet(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		#set fuseid's state for set 3 to true
		SetSetFlag( fuseid, 3, True )

		#Copy set 3 and Paste into set 4
		CopyPasteSet( 3, 4 )

		#get fuseid's state for set 4
		flag_value = GetSetFlag( fuseid, 4 )

		if  flag_value != True: print( "---> Error: API CopyPasteSet " )

	def test_GetBBoxSet(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		Update()

		sethasmembers, xmin, ymin, zmin, xlen, ylen, zlen = GetBBoxSet( SET_ALL )
	def test_GetScaleIndependentBBoxSet(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		Update()

		sethasmembers, xmin, ymin, zmin, xlen, ylen, zlen = GetScaleIndependentBBoxSet( SET_ALL );
	def test_ScaleSet(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE" )

		SetSetFlag( fuseid, 3, True )

		# Scale by a factor of 2
		ScaleSet( 3, 2.0 )

	def test_RotateSet(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE" )

		SetSetFlag( fuseid, 3, True )

		# Rotate 90 degrees about Y
		RotateSet( 3, 0, 90, 0 )

	def test_TranslateSet(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE" )

		SetSetFlag( fuseid, 3, True )

		# Translate 2 units in X and 3 units in Y
		TranslateSet( 3, vec3d( 2, 3, 0 ) )

	def test_TransformSet(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE" )

		SetSetFlag( fuseid, 3, True )

		# Translate 2 units in X and 3 units in Y, rotate 90 degrees about Y, and scale by a factor of 2
		TransformSet( 3, vec3d( 2, 3, 0 ), 0, 90, 0, 2.0, True )

	def test_ValidParm(self):
		#==== Add Pod Geometry ====//
		pid = AddGeom( "POD" )

		lenid = GetParm( pid, "Length", "Design" )

		if  not ValidParm( lenid ) : print( "---> Error: API GetParm  " )

	def test_SetParmVal(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		SetParmVal( wid, 23.0 )

		if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )

	def test_SetParmValLimits(self):
		pod_id = AddGeom( "POD" )

		length = FindParm( pod_id, "Length", "Design" )

		SetParmValLimits( length, 10.0, 0.001, 1.0e12 )

		SetParmDescript( length, "Total Length of Geom" )

	def test_SetParmValUpdate(self):
		#==== Add Pod Geometry ====//
		pod_id = AddGeom( "POD" )

		parm_id = GetParm( pod_id, "X_Rel_Location", "XForm" )

		SetParmValUpdate( parm_id, 5.0 )

	def test_GetParmVal(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		SetParmVal( wid, 23.0 )

		if  abs( GetParmVal( wid ) - 23 ) > 1e-6 : print( "---> Error: API Parm Val Set/Get " )

	def test_GetIntParmVal(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		num_blade_id = GetParm( prop_id, "NumBlade", "Design" )

		num_blade = GetIntParmVal( num_blade_id )

	def test_GetBoolParmVal(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		rev_flag_id = GetParm( prop_id, "ReverseFlag", "Design" )

		reverse_flag = GetBoolParmVal( rev_flag_id )

	def test_SetParmUpperLimit(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		SetParmVal( wid, 23.0 )

		SetParmUpperLimit( wid, 13.0 )

		if  abs( GetParmVal( wid ) - 13 ) > 1e-6 : print( "---> Error: API SetParmUpperLimit " )

	def test_GetParmUpperLimit(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		num_blade_id = GetParm( prop_id, "NumBlade", "Design" )

		max_blade = GetParmUpperLimit( num_blade_id )

	def test_SetParmLowerLimit(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		SetParmVal( wid, 13.0 )

		SetParmLowerLimit( wid, 15.0 )

		if  abs( GetParmVal( wid ) - 15 ) > 1e-6 : print( "---> Error: API SetParmLowerLimit " )

	def test_GetParmLowerLimit(self):
		#==== Add Prop Geometry ====//
		prop_id = AddGeom( "PROP" )

		num_blade_id = GetParm( prop_id, "NumBlade", "Design" )

		min_blade = GetParmLowerLimit( num_blade_id )

	def test_GetParmType(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		if  GetParmType( wid ) != PARM_DOUBLE_TYPE : print( "---> Error: API GetParmType " )

	def test_GetParmName(self):
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

	def test_GetParmGroupName(self):
		veh_id = FindContainer( "Vehicle", 0 )

		#==== Get and List All Parms in the Container ====//
		parm_ids = FindContainerParmIDs( veh_id )

		print( "Parm Groups and IDs in Vehicle Parm Container: " )

		for i in range(len(parm_ids)):

			group_str = GetParmGroupName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"

			print( group_str )

	def test_GetParmDisplayGroupName(self):
		veh_id = FindContainer( "Vehicle", 0 )

		#==== Get and List All Parms in the Container ====//
		parm_ids = FindContainerParmIDs( veh_id )

		print( "Parm Group Display Names and IDs in Vehicle Parm Container: " )

		for i in range(len(parm_ids)):

			group_str = GetParmDisplayGroupName( parm_ids[i] ) + ": " + parm_ids[i] + "\n"

			print( group_str )

	def test_GetParmContainer(self):
		# Add Fuselage Geom
		fuseid = AddGeom( "FUSELAGE", "" )

		xsec_surf = GetXSecSurf( fuseid, 0 )

		ChangeXSecShape( xsec_surf, GetNumXSec( xsec_surf ) - 1, XS_ROUNDED_RECTANGLE )

		xsec = GetXSec( xsec_surf, GetNumXSec( xsec_surf ) - 1 )

		wid = GetXSecParm( xsec, "RoundedRect_Width" )

		cid = GetParmContainer( wid )

		if  len(cid) == 0 : print( "---> Error: API GetParmContainer " )

	def test_SetParmDescript(self):
		pod_id = AddGeom( "POD" )

		length = FindParm( pod_id, "Length", "Design" )

		SetParmValLimits( length, 10.0, 0.001, 1.0e12 )

		SetParmDescript( length, "Total Length of Geom" )

	def test_GetParmDescript(self):
		pod_id = AddGeom( "POD" )

		length = FindParm( pod_id, "Length", "Design" )

		SetParmValLimits( length, 10.0, 0.001, 1.0e12 )

		desc = GetParmDescript( length )
		print( desc )

	def test_FindParm(self):
		#==== Add Wing Geometry ====//
		wing_id = AddGeom( "WING" )

		#==== Turn Symmetry OFF ====//
		sym_id = FindParm( wing_id, "Sym_Planar_Flag", "Sym")

		SetParmVal( sym_id, 0.0 ) # Note: bool input not supported in SetParmVal

	def test_FindContainers(self):
		ctr_arr = FindContainers()

		print( "---> API Parm Container IDs: " )

		for i in range(int( len(ctr_arr) )):

			message = "\t" + ctr_arr[i] + "\n"

			print( message )

	def test_FindContainersWithName(self):
		ctr_arr = FindContainersWithName( "UserParms" )

		if  len(ctr_arr) > 0 : print( ( "UserParms Parm Container ID: " + ctr_arr[0] ) )

	def test_FindContainer(self):
		#===== Get Vehicle Parm Container ID ====//
		veh_id = FindContainer( "Vehicle", 0 )

	def test_GetContainerName(self):
		veh_id = FindContainer( "Vehicle", 0 )

		if  GetContainerName( veh_id) != "Vehicle":       print( "---> Error: API GetContainerName" )

	def test_FindContainerGroupNames(self):
		user_ctr = FindContainer( "UserParms", 0 )

		grp_arr = FindContainerGroupNames( user_ctr )

		print( "---> UserParms Container Group IDs: " )
		for i in range(int( len(grp_arr) )):

			message = "\t" + grp_arr[i] + "\n"

			print( message )

	def test_FindContainerParmIDs(self):
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

	def test_GetVehicleID(self):
		#===== Get Vehicle Parm Container ID ====//
		veh_id = GetVehicleID()

	def test_GetNumUserParms(self):
		n = GetNumUserParms()


	def test_GetNumPredefinedUserParms(self):
		n = GetNumPredefinedUserParms()


	def test_GetAllUserParms(self):
		id_arr = GetAllUserParms()

		print( "---> User Parm IDs: " )

		for i in range(int( len(id_arr) )):

			message = "\t" + id_arr[i] + "\n"

			print( message )

	def test_GetUserParmContainer(self):
		up_id = GetUserParmContainer()

	def test_AddUserParm(self):
		length = AddUserParm( PARM_DOUBLE_TYPE, "Length", "Design" )

		SetParmValLimits( length, 10.0, 0.001, 1.0e12 )

		SetParmDescript( length, "Length user parameter" )

	def test_DeleteUserParm(self):

		n = GetNumPredefinedUserParms()
		id_arr = GetAllUserParms()

		if  len(id_arr) > n :
			DeleteUserParm( id_arr[n] )

	def test_DeleteAllUserParm(self):
		DeleteAllUserParm()

	def test_ComputeMinClearanceDistance(self):
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		pid = AddGeom( "POD", "" )                     # Add Pod

		x = GetParm( pid, "X_Rel_Location", "XForm" )

		SetParmVal( x, 3.0 )

		Update()

		min_dist = ComputeMinClearanceDistance( pid, SET_ALL )

	def test_SnapParm(self):
		#Add Geoms
		fid = AddGeom( "FUSELAGE", "" )             # Add Fuselage

		pid = AddGeom( "POD", "" )                     # Add Pod

		x = GetParm( pid, "X_Rel_Location", "XForm" )

		SetParmVal( x, 3.0 )

		Update()

		min_dist = SnapParm( x, 0.1, True, SET_ALL )

	def test_AddVarPresetGroup(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )
	def test_AddVarPresetSetting(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

	def test_AddVarPresetParm(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

	def test_DeleteVarPresetGroup(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		DeleteVarPresetGroup( gid )

	def test_DeleteVarPresetSetting(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		DeleteVarPresetSetting( gid, sid )

	def test_DeleteVarPresetParm(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		DeleteVarPresetParm( gid, p1 )

	def test_SetVarPresetParmVal(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		SetVarPresetParmVal( gid, sid, p1, 51 )

	def test_GetVarPresetParmVal(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		val = GetVarPresetParmVal( gid, sid, p1 )

	def test_GetGroupName(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		name = GetGroupName( gid )

	def test_GetSettingName(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		name = GetSettingName( sid )

	def test_SetGroupName(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		SetGroupName( gid, "Resolution" )

	def test_SetSettingName(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		SetSettingName( sid, "Low" )

	def test_GetVarPresetGroups(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		group_ids = GetVarPresetGroups()

	def test_GetVarPresetSettings(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		settingds = GetVarPresetSettings( gid )

	def test_GetVarPresetParmIDs(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		parmids = GetVarPresetParmIDs( gid )

	def test_GetVarPresetParmVals(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		parmval_vec = GetVarPresetParmVals( sid )

	def test_SetVarPresetParmVals(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		vals = [ 45 ]

		SetVarPresetParmVals( sid, vals )

	def test_SaveVarPresetParmVals(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		SaveVarPresetParmVals( gid, sid )

	def test_ApplyVarPresetSetting(self):
		# Add Pod Geom
		pod1 = AddGeom( "POD", "" )

		gid = AddVarPresetGroup( "Tess" )

		sid = AddVarPresetSetting( gid, "Coarse" )

		p1 = FindParm( pod1, "Tess_U", "Shape" )

		AddVarPresetParm( gid, p1 )

		ApplyVarPresetSetting( gid, sid )

		Update()

	def test_CreateAndAddMode(self):
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

	def test_GetNumModes(self):
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

	def test_GetAllModes(self):
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

	def test_DelMode(self):
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

	def test_DelAllModes(self):
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

	def test_ApplyModeSettings(self):
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

	def test_ShowOnlyMode(self):
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

	def test_ModeAddGroupSetting(self):
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

	def test_ModeGetGroup(self):
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

	def test_ModeGetSetting(self):
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

	def test_ModeGetAllGroups(self):
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

	def test_ModeGetAllSettings(self):
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

	def test_RemoveGroupSetting(self):
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

	def test_RemoveAllGroupSettings(self):
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

	def test_ApproximateAllPropellerPCurves(self):
		# Add Propeller
		prop = AddGeom( "PROP", "" )

		ApproximateAllPropellerPCurves( prop )


	def test_ResetPropellerThicknessCurve(self):
		# Add Propeller
		prop = AddGeom( "PROP", "" )

		ResetPropellerThicknessCurve( prop )


	def test_AutoGroupVSPAEROControlSurfaces(self):
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

	def test_CreateVSPAEROControlSurfaceGroup(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		num_group = GetNumControlSurfaceGroups()

		if  num_group != 1 : print( "Error: CreateVSPAEROControlSurfaceGroup" )

	def test_AddAllToVSPAEROControlSurfaceGroup(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		AddAllToVSPAEROControlSurfaceGroup( group_index )

	def test_RemoveAllFromVSPAEROControlSurfaceGroup(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		AddAllToVSPAEROControlSurfaceGroup( group_index )

		RemoveAllFromVSPAEROControlSurfaceGroup( group_index ) # Empty control surface group

	def test_GetActiveCSNameVec(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		AddAllToVSPAEROControlSurfaceGroup( group_index )

		cs_name_vec = GetActiveCSNameVec( group_index )

		print( "Active CS in Group Index #", False )
		print( group_index )

		for i in range(int( len(cs_name_vec) )):

			print( cs_name_vec[i] )

	def test_GetCompleteCSNameVec(self):
		wid = AddGeom( "WING", "" )                             # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL )                      # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		cs_name_vec = GetCompleteCSNameVec()

		print( "All Control Surfaces: ", False )

		for i in range(int( len(cs_name_vec) )):

			print( cs_name_vec[i] )

	def test_GetAvailableCSNameVec(self):
		wid = AddGeom( "WING", "" ) # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		cs_name_vec = GetAvailableCSNameVec( group_index )

		cs_ind_vec = [1]

		AddSelectedToCSGroup( cs_ind_vec, group_index ) # Add the first available control surface to the group

	def test_SetVSPAEROControlGroupName(self):
		wid = AddGeom( "WING", "" ) # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		SetVSPAEROControlGroupName( "Example_CS_Group", group_index )

		print( "CS Group name: ", False )

		print( GetVSPAEROControlGroupName( group_index ) )

	def test_GetVSPAEROControlGroupName(self):
		wid = AddGeom( "WING", "" ) # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		SetVSPAEROControlGroupName( "Example_CS_Group", group_index )

		print( "CS Group name: ", False )

		print( GetVSPAEROControlGroupName( group_index ) )

	def test_AddSelectedToCSGroup(self):
		wid = AddGeom( "WING", "" ) # Add Wing

		aileron_id = AddSubSurf( wid, SS_CONTROL ) # Add Control Surface Sub-Surface

		group_index = CreateVSPAEROControlSurfaceGroup() # Empty control surface group

		cs_name_vec = GetAvailableCSNameVec( group_index )

		cs_ind_vec = [0] * len(cs_name_vec)

		for i in range(int( len(cs_name_vec) )):

			cs_ind_vec[i] = i + 1

		AddSelectedToCSGroup( cs_ind_vec, group_index ) # Add all available control surfaces to the group

	def test_RemoveSelectedFromCSGroup(self):
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

	def test_GetNumControlSurfaceGroups(self):
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

	def test_FindActuatorDisk(self):
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

	def test_GetNumActuatorDisks(self):
		# Set VSPAERO set index to SET_ALL
		SetParmVal( FindParm( FindContainer( "VSPAEROSettings", 0 ), "GeomSet", "VSPAERO" ), SET_ALL )

		# Add a propeller
		prop_id = AddGeom( "PROP", "" )
		SetParmValUpdate( prop_id, "PropMode", "Design", PROP_BLADES )

		num_disk = GetNumActuatorDisks() # Should be 0

		SetParmValUpdate( prop_id, "PropMode", "Design", PROP_DISK )

		num_disk = GetNumActuatorDisks() # Should be 1

	def test_FindUnsteadyGroup(self):
		wing_id = AddGeom( "WING" )
		pod_id = AddGeom( "POD" )

		# Create an actuator disk
		prop_id = AddGeom( "PROP", "" )
		SetParmVal( prop_id, "PropMode", "Design", PROP_BLADES )

		Update()

		# Setup the unsteady group VSPAERO parms
		disk_id = FindUnsteadyGroup( 1 ) # fixed components are in group 0 (wing & pod)

		SetParmVal( FindParm( disk_id, "RPM", "UnsteadyGroup" ), 1234.0 )

	def test_GetUnsteadyGroupName(self):
		# Add a pod and wing
		pod_id = AddGeom( "POD", "" )
		wing_id = AddGeom( "WING", pod_id )

		SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
		Update()

		print( GetUnsteadyGroupName( 0 ) )

	def test_GetUnsteadyGroupCompIDs(self):
		# Add a pod and wing
		pod_id = AddGeom( "POD", "" )
		wing_id = AddGeom( "WING", pod_id ) # Default with symmetry on -> 2 surfaces

		SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
		Update()

		comp_ids = GetUnsteadyGroupCompIDs( 0 )

		if  len(comp_ids) != 3 :
			print( "ERROR: GetUnsteadyGroupCompIDs" )

	def test_GetUnsteadyGroupSurfIndexes(self):
		# Add a pod and wing
		pod_id = AddGeom( "POD", "" )
		wing_id = AddGeom( "WING", pod_id ) # Default with symmetry on -> 2 surfaces

		SetParmVal( wing_id, "X_Rel_Location", "XForm", 2.5 )
		Update()

		surf_indexes = GetUnsteadyGroupSurfIndexes( 0 )

		if  len(surf_indexes) != 3 :
			print( "ERROR: GetUnsteadyGroupSurfIndexes" )

	def test_GetNumUnsteadyGroups(self):
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

	def test_GetNumUnsteadyRotorGroups(self):
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

	def test_AddExcrescence(self):
		AddExcrescence( "Miscellaneous", EXCRESCENCE_COUNT, 8.5 )

		AddExcrescence( "Cowl Boattail", EXCRESCENCE_CD, 0.0003 )

	def test_DeleteExcrescence(self):
		AddExcrescence( "Miscellaneous", EXCRESCENCE_COUNT, 8.5 )

		AddExcrescence( "Cowl Boattail", EXCRESCENCE_CD, 0.0003 )

		AddExcrescence( "Percentage Example", EXCRESCENCE_PERCENT_GEOM, 5 )

		DeleteExcrescence( 2 ) # Last Index

	def test_WriteAtmosphereCSVFile(self):
		print( "Starting USAF Atmosphere 1966 Table Creation. \n" )

		WriteAtmosphereCSVFile( "USAFAtmosphere1966Data.csv", ATMOS_TYPE_HERRINGTON_1966 )

	def test_CalcAtmosphere(self):

		alt = 4000

		delta_temp = 0

		temp, pres, pres_ratio, rho_ratio = CalcAtmosphere( alt, delta_temp, ATMOS_TYPE_US_STANDARD_1976)

	def test_WriteBodyFFCSVFile(self):
		print( "Starting Body Form Factor Data Creation. \n" )
		WriteBodyFFCSVFile( "BodyFormFactorData.csv" )

	def test_WriteWingFFCSVFile(self):
		print( "Starting Wing Form Factor Data Creation. \n" )
		WriteWingFFCSVFile( "WingFormFactorData.csv" )

	def test_WriteCfEqnCSVFile(self):
		print( "Starting Turbulent Friciton Coefficient Data Creation. \n" )
		WriteCfEqnCSVFile( "FrictionCoefficientData.csv" )

	def test_WritePartialCfMethodCSVFile(self):
		print( "Starting Partial Friction Method Data Creation. \n" )
		WritePartialCfMethodCSVFile( "PartialFrictionMethodData.csv" )

	def test_CompPnt01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		u = 0.12345
		w = 0.67890

		pnt = CompPnt01( geom_id, surf_indx, u, w )

		print( f"Point: ( {pnt.x()}, {pnt.y()}, {pnt.z()} )" )

	def test_CompNorm01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		u = 0.12345
		w = 0.67890

		norm = CompNorm01( geom_id, surf_indx, u, w )

		print( "Point: ( {norm.x()}, {norm.y()}, {norm.z()} )" )

	def test_CompTanU01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		u = 0.12345
		w = 0.67890

		tanu = CompTanU01( geom_id, surf_indx, u, w )

		print( f"Point: ( {tanu.x()}, {tanu.y()}, {tanu.z()} )" )

	def test_CompTanW01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		u = 0.12345
		w = 0.67890

		tanw = CompTanW01( geom_id, surf_indx, u, w )

		print( f"Point: ( {tanw.x()}, {tanw.y()}, {tanw.z()} )" )

	def test_CompCurvature01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0


		u = 0.25
		w = 0.75

		k1, k2, ka, kg = CompCurvature01( geom_id, surf_indx, u, w )

		print( f"Curvature : k1 {k1} k2 {k2} ka {ka} kg {kg}" )

	def test_ProjPnt01(self):
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

	def test_ProjPnt01I(self):
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

	def test_ProjPnt01Guess(self):
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

	def test_AxisProjPnt01(self):
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

	def test_AxisProjPnt01I(self):
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

	def test_AxisProjPnt01Guess(self):
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

	def test_InsideSurf(self):
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


	def test_CompPntRST(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		r = 0.12
		s = 0.68
		t = 0.56

		pnt = CompPntRST( geom_id, surf_indx, r, s, t )

		print( f"Point: ( {pnt.x()}, {pnt.y()}, {pnt.z()} )" )

	def test_FindRST(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		r = 0.12
		s = 0.68
		t = 0.56

		pnt = CompPntRST( geom_id, surf_indx, r, s, t )


		d, rout, sout, tout = FindRST( geom_id, surf_indx, pnt )

		print( f"Dist {d} r {rout} s {sout} t {tout}" )

	def test_FindRSTGuess(self):
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

	def test_ConvertRSTtoLMN(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		r = 0.12
		s = 0.68
		t = 0.56

		l_out, m_out, n_out = ConvertRSTtoLMN( geom_id, surf_indx, r, s, t )


	def test_ConvertRtoL(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		r = 0.12

		l_out = ConvertRtoL( geom_id, surf_indx, r )


	def test_ConvertLMNtoRST(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		l = 0.12
		m = 0.34
		n = 0.56

		r_out, s_out, t_out = ConvertLMNtoRST( geom_id, surf_indx, l, m, n )


	def test_ConvertLtoR(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		l = 0.12

		r_out = ConvertLtoR( geom_id, surf_indx, l )


	def test_ConvertUtoEta(self):
		# Add Wing Geom
		geom_id = AddGeom( "WING", "" )

		surf_indx = 0

		u = 0.25

		eta_out = ConvertUtoEta( geom_id, u )


	def test_ConvertEtatoU(self):
		# Add Wing Geom
		geom_id = AddGeom( "WING", "" )

		surf_indx = 0

		eta= 0.25

		u = ConvertEtatoU( geom_id, eta )


	def test_CompVecPnt01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		n = 5

		uvec = [0]*n
		wvec = [0]*n

		for i in range(n):

			uvec[i] = (i+1)*1.0/(n+1)

			wvec[i] = (n-i)*1.0/(n+1)

		ptvec = CompVecPnt01( geom_id, 0, uvec, wvec )

	def test_CompVecDegenPnt01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		n = 5

		uvec = [0]*n
		wvec = [0]*n

		for i in range(n):

			uvec[i] = (i+1)*1.0/(n+1)

			wvec[i] = (n-i)*1.0/(n+1)

		ptvec = CompVecDegenPnt01( geom_id, 0, 0, uvec, wvec )

	def test_CompVecNorm01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		n = 5

		uvec = [0]*n
		wvec = [0]*n

		for i in range(n):

			uvec[i] = (i+1)*1.0/(n+1)

			wvec[i] = (n-i)*1.0/(n+1)

		normvec = CompVecNorm01( geom_id, 0, uvec, wvec )

	def test_CompVecCurvature01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		n = 5

		uvec = [0]*n
		wvec = [0]*n

		for i in range(n):

			uvec[i] = (i+1)*1.0/(n+1)

			wvec[i] = (n-i)*1.0/(n+1)



		k1vec, k2vec, kavec, kgvec = CompVecCurvature01( geom_id, 0, uvec, wvec )

	def test_ProjVecPnt01(self):
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

	def test_ProjVecPnt01Guess(self):
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

	def test_AxisProjVecPnt01(self):
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


	def test_AxisProjVecPnt01Guess(self):
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


	def test_VecInsideSurf(self):
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


	def test_CompVecPntRST(self):
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

	def test_FindRSTVec(self):
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

	def test_FindRSTVecGuess(self):
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

	def test_ConvertRSTtoLMNVec(self):
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


	def test_ConvertLMNtoRSTVec(self):
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


	def test_GetUWTess01(self):
		# Add Pod Geom
		geom_id = AddGeom( "POD", "" )

		surf_indx = 0

		utess, wtess = GetUWTess01( geom_id, surf_indx )

	def test_AddRuler(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		pid2 = AddGeom( "POD", "" )

		SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )

		rid = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )

		SetParmVal( FindParm( rid, "X_Offset", "Measure" ), 6.0 )

	def test_GetAllRulers(self):
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

	def test_DelRuler(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		pid2 = AddGeom( "POD", "" )

		SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )

		rid1 = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )

		rid2 = AddRuler( pid1, 0, 0.4, 0.6, pid1, 1, 0.8, 0.9, "Ruler 2" )

		ruler_array = GetAllRulers()

		DelRuler( ruler_array[0] )

	def test_DeleteAllRulers(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		pid2 = AddGeom( "POD", "" )

		SetParmVal( pid2, "Z_Rel_Location", "XForm", 4.0 )

		rid1 = AddRuler( pid1, 1, 0.2, 0.3, pid2, 0, 0.2, 0.3, "Ruler 1" )

		rid2 = AddRuler( pid1, 0, 0.4, 0.6, pid1, 1, 0.8, 0.9, "Ruler 2" )

		DeleteAllRulers()

	def test_AddProbe(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		probe_id = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )

		SetParmVal( FindParm( probe_id, "Len", "Measure" ), 3.0 )

	def test_GetAllProbes(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		probe_id = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )

		probe_array = GetAllProbes()

		print( "One Probe: ", False )

		print( probe_array[0] )

	def test_DelProbe(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		probe_id_1 = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
		probe_id_2 = AddProbe( pid1, 0, 0.2, 0.3, "Probe 2" )

		DelProbe( probe_id_1 )

		probe_array = GetAllProbes()

		if  len(probe_array) != 1 : print( "Error: DelProbe" )

	def test_DeleteAllProbes(self):
		pid1 = AddGeom( "POD", "" )

		SetParmVal( pid1, "Y_Rel_Location", "XForm", 2.0 )

		probe_id_1 = AddProbe( pid1, 0, 0.5, 0.8, "Probe 1" )
		probe_id_2 = AddProbe( pid1, 0, 0.2, 0.3, "Probe 2" )

		DeleteAllProbes()

		probe_array = GetAllProbes()

		if  len(probe_array) != 0 : print( "Error: DeleteAllProbes" )

	def test_GetAdvLinkNames(self):
		link_array = GetAdvLinkNames()

		for n in range(len(link_array) ):

			print( link_array[n] )

	def test_GetLinkIndex(self):

		pod = AddGeom( "POD", "" )
		length = FindParm( pod, "Length", "Design" )
		x_pos = GetParm( pod, "X_Rel_Location", "XForm" )

		AddAdvLink( "ExampleLink" )
		indx = GetLinkIndex( "ExampleLink" )
		AddAdvLinkInput( indx, length, "len" )
		AddAdvLinkOutput( indx, x_pos, "x" )

		SetAdvLinkCode( indx, "x = 10.0 - len;" )

		BuildAdvLinkScript( indx )


	def test_DelAdvLink(self):

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


	def test_DelAllAdvLinks(self):

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


	def test_AddAdvLink(self):

		pod = AddGeom( "POD", "" )
		length = FindParm( pod, "Length", "Design" )
		x_pos = GetParm( pod, "X_Rel_Location", "XForm" )

		AddAdvLink( "ExampleLink" )
		indx = GetLinkIndex( "ExampleLink" )
		AddAdvLinkInput( indx, length, "len" )
		AddAdvLinkOutput( indx, x_pos, "x" )

		SetAdvLinkCode( indx, "x = 10.0 - len;" )

		BuildAdvLinkScript( indx )


	def test_AddAdvLinkInput(self):

		pod = AddGeom( "POD", "" )
		length = FindParm( pod, "Length", "Design" )
		x_pos = GetParm( pod, "X_Rel_Location", "XForm" )

		AddAdvLink( "ExampleLink" )
		indx = GetLinkIndex( "ExampleLink" )
		AddAdvLinkInput( indx, length, "len" )
		AddAdvLinkOutput( indx, x_pos, "x" )

		SetAdvLinkCode( indx, "x = 10.0 - len;" )

		BuildAdvLinkScript( indx )


	def test_AddAdvLinkOutput(self):

		pod = AddGeom( "POD", "" )
		length = FindParm( pod, "Length", "Design" )
		x_pos = GetParm( pod, "X_Rel_Location", "XForm" )

		AddAdvLink( "ExampleLink" )
		indx = GetLinkIndex( "ExampleLink" )
		AddAdvLinkInput( indx, length, "len" )
		AddAdvLinkOutput( indx, x_pos, "x" )

		SetAdvLinkCode( indx, "x = 10.0 - len;" )

		BuildAdvLinkScript( indx )


	def test_DelAdvLinkInput(self):

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


	def test_DelAdvLinkOutput(self):

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


	def test_GetAdvLinkInputNames(self):

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


	def test_GetAdvLinkInputParms(self):

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


	def test_GetAdvLinkOutputNames(self):

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


	def test_GetAdvLinkOutputParms(self):

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


	def test_ValidateAdvLinkParms(self):

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


	def test_SetAdvLinkCode(self):

		pod = AddGeom( "POD", "" )
		length = FindParm( pod, "Length", "Design" )
		x_pos = GetParm( pod, "X_Rel_Location", "XForm" )

		AddAdvLink( "ExampleLink" )
		indx = GetLinkIndex( "ExampleLink" )
		AddAdvLinkInput( indx, length, "len" )
		AddAdvLinkOutput( indx, x_pos, "x" )

		SetAdvLinkCode( indx, "x = 10.0 - len;" )

		BuildAdvLinkScript( indx )


	def test_GetAdvLinkCode(self):

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


	def test_SearchReplaceAdvLinkCode(self):

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


	def test_BuildAdvLinkScript(self):

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


	def test_IsFacade(self):
		is_facade = IsFacade()
	def test_IsGUIRunning(self):
		is_gui_active = IsGUIRunning()

if __name__ == '__main__':
    unittest.main()
