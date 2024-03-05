
import sys
import os

from ij import IJ
from ij import WindowManager

from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import DogDetectorFactory
from fiji.plugin.trackmate.tracking.kalman import KalmanTrackerFactory
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackerProvider
from fiji.plugin.trackmate.providers import DetectorProvider
from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackAnalyzerProvider
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
from fiji.plugin.trackmate.io import TmXmlWriter
import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML
from java.io import File

# We have to do the following to avoid errors with UTF8 chars generated in 
# TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding('utf-8')


# Get currently selected image
#imp = WindowManager.getCurrentImage()
folder_path = r'X:\microscopy data\2024_01_17_GEM_timecourse\wrong delay\gaussian (26 frames)'

# List all files in the folder
tif_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.tif')]


for image_path in tif_files: 
	imp = IJ.openImage(image_path)

	if imp is not None:
	    # Get the filename from the image path
	    filename = os.path.basename(image_path)
	    dirname = os.path.dirname(image_path)
	    print("Directory of the image:", dirname)
	    
	    print("Opened image with filename:", filename)
	else:
	    print("Failed to open the image.")
	    continue
    
	# define the name of the directory to be created	
	print("Current directory:" + dirname)
	
	#== define the name of the directory to be created
	newdir = os.path.join (dirname, "TRACKS")
	if os.path.exists(newdir):
		print ("Found directory " + newdir)
	else:
		#== define the access rights
		access_rights = 0o755
		try:
			os.mkdir(newdir, access_rights)
		except OSError:
			print ("Creation of the directory %s failed" % newdir)
		else:
			print ("Successfully created the directory %s" % newdir)
	    
	imp.show()
	
	
	# Swap Z and T dimensions if T=1
	dims = imp.getDimensions() # default order: XYCZT
	print(str(dims[4]))
	if (dims[4] == 1):
		imp.setDimensions( dims[ 2 ], dims[ 4 ], dims[ 3 ] )
		modified_dims = imp.getDimensions()
		print("Modified Image Dimensions:" + str(modified_dims))
		
	
	#-------------------------
	# Instantiate model object
	#-------------------------
	
	model = Model()
	
	# Set logger
	model.setLogger(Logger.IJ_LOGGER)
	
	#------------------------
	# Prepare settings object
	#------------------------
	
	settings = Settings(imp)
	
	# Configure detector
	settings.detectorFactory = DogDetectorFactory()
	settings.detectorSettings = {
	    'DO_SUBPIXEL_LOCALIZATION' : True,
	    'RADIUS' : 0.5,
	    'TARGET_CHANNEL' : 1,
	    'THRESHOLD' : 0.284729560645851,
	    'DO_MEDIAN_FILTERING' : True,
	}
	
	# Configure tracker
	settings.trackerFactory = KalmanTrackerFactory()
	settings.trackerSettings = settings.trackerFactory.getDefaultSettings()
	settings.trackerSettings['LINKING_MAX_DISTANCE'] = 0.5
	settings.trackerSettings['KALMAN_SEARCH_RADIUS'] = 0.5
	settings.trackerSettings['MAX_FRAME_GAP'] = 2
	settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
	settings.trackerSettings['ALLOW_TRACK_MERGING'] = False
	
	# Add the analyzers for some spot features.
	# Here we decide brutally to add all of them.
	settings.addAllAnalyzers()
	
	# We configure the initial filtering to discard spots 
	# with a quality lower than x .
	settings.initialSpotFilterValue = 0.6
	
	#configure spot filter 
	#filter1_spot = FeatureFilter('MIN_INTENSITY', 110, True)
	#settings.addSpotFilter(filter1_spot)
	
	#configure track filter
	filter1_track = FeatureFilter('NUMBER_SPOTS', 9, True)
	settings.addTrackFilter(filter1_track)
	#filter2_track = FeatureFilter('CONFINEMENT_RATIO', -0.0776, True)
	#settings.addTrackFilter(filter2_track)
	#filter3 = FeatureFilter('TRACK_DISPLACEMENT', 10.0, False);
	#settings.addTrackFilter(filter3)
	
	print(str(settings))
	
	#----------------------
	# Instantiate trackmate
	#----------------------
	
	trackmate = TrackMate(model, settings)
	trackmate.getModel().getLogger().log( settings.toStringFeatureAnalyzersInfo() )
	trackmate.computeSpotFeatures( True )
	trackmate.computeEdgeFeatures( True )
	trackmate.computeTrackFeatures( True )
	
	#------------
	# Execute all
	#------------
	
	
	ok = trackmate.checkInput()
	if not ok:
	    sys.exit(str(trackmate.getErrorMessage()))
	
	ok = trackmate.process()
	if not ok:
	    sys.exit(str(trackmate.getErrorMessage()))
	
	
	
	#----------------
	# Display results
	#----------------
	
	model.getLogger().log('Found ' + str(model.getTrackModel().nTracks(True)) + ' tracks.')
	
	# A selection.
	sm = SelectionModel( model )
	
	# Read the default display settings.
	ds = DisplaySettingsIO.readUserDefault()
	
	# The viewer.
	displayer =  HyperStackDisplayer( model, sm, imp, ds ) 
	displayer.render()
	
	# The feature model, that stores edge and track features.
	fm = model.getFeatureModel()
	
	# Iterate over all the tracks that are visible.
	for id in model.getTrackModel().trackIDs(True):
	
	    # Fetch the track feature from the feature model.
	    v = fm.getTrackFeature(id, 'TRACK_MEAN_SPEED')
	    model.getLogger().log('')
	    model.getLogger().log('Track ' + str(id) + ': mean velocity = ' + str(v) + ' ' + model.getSpaceUnits() + '/' + model.getTimeUnits())
	
		# Get all the spots of the current track.
	    track = model.getTrackModel().trackSpots(id)
	    for spot in track:
	        sid = spot.ID()
	        # Fetch spot features directly from spot.
	        # Note that for spots the feature values are not stored in the FeatureModel
	        # object, but in the Spot object directly. This is an exception; for tracks
	        # and edges, you have to query the feature model.
	        x=spot.getFeature('POSITION_X')
	        y=spot.getFeature('POSITION_Y')
	        t=spot.getFeature('FRAME')
	        q=spot.getFeature('QUALITY')
	        snr=spot.getFeature('SNR_CH1')
	        mean=spot.getFeature('MEAN_INTENSITY_CH1')
	        model.getLogger().log('\tspot ID = ' + str(sid) + ': x='+str(x)+', y='+str(y)+', t='+str(t)+', q='+str(q) + ', snr='+str(snr) + ', mean = ' + str(mean))
	
	#---------------
	# Export results
	#---------------
	
	#fileout = java.io.File(newdir + "\" + filename + ".xml")
	fileout = File(os.path.join(newdir, filename + ".xml"))
	ExportTracksToXML.export(model, settings, fileout)
	IJ.run("Close")
	imp.close()
	#i += 1

	
