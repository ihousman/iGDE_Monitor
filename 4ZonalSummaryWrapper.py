#Script to take Landsat and DAYMET composites and run Landtrendr over them
####################################################################################################
from iGDE_lib import *
####################################################################################################
#Define user parameters:


outputTrainingTableDir = 'projects/igde-work/raster-zonal-stats-data/RF-Training-Tables';
outputTrainingTableName = 'dgwRFModelingTrainingTable3_{}_{}'.format(startTrainingYear,endTrainingYear)
outputTrainingTablePath = outputTrainingTableDir + '/'+outputTrainingTableName

outputApplyTableDir = 'projects/igde-work/raster-zonal-stats-data/RF-Apply-Tables'
outputApplyTableName = 'dgwRFModelingApplyTable4_'
outputApplyTablePath = outputApplyTableDir + '/'+outputApplyTableName

def getLT(ltCollection):
  c = ee.ImageCollection(ltCollection)
  ids = c.aggregate_array('system:index').getInfo()
  outC = None
  for id in ids:
    startYear = int(id.split('_')[-2])
    endYear = int(id.split('_')[-1])
    indexName = id.split('_')[-3]
    ltStack = c.filter(ee.Filter.eq('system:index',id)).first()
    fit = simpleLTFit(ltStack,startYear,endYear,indexName).select(['.*_fitted','.*_mag','.*_diff'])

    if outC  == None:
      outC = fit
    else:
      outC = ee.ImageCollection(joinCollections(outC,fit))
  print(outC.size().getInfo())
  print(outC.first().bandNames().getInfo())
  Map.addLayer(outC,{},'all fits',True)
  Map.view()


getLT(ltCollection)
# var durFitMagSlope = rfLib.getLT();
# // var strataRaster = rfLib.getStrataRaster();
# var trainingGDEs = rfLib.trainingGDEs;
# Map.addLayer(trainingGDEs)
# var applyGDEs = rfLib.applyGDEs;
# print(applyGDEs.size())
# // Map.addLayer(strataRaster)
# // var strataZonalMode= strataRaster.reduceRegions(applyGDEs, ee.Reducer.first(),null,'EPSG:5070',[30,0,-2361915.0,0,-30,3177735.0],4);
# // print(strataZonalMode.first())

# // Map.addLayer(applyGDEs)
# // var rasterFields = ee.Image(durFitMagSlope.first()).bandNames();

# # function getTrainingTable(){
#   var dgwLTJoined = ee.List.sequence(startTrainingYear,endTrainingYear).getInfo().map(function(yr){
        
#         //Set up fields to select
#         var yearDGWField = 'Depth'+yr.toString();//ee.String('Depth').cat(yr.format());
#         var fromFields = ee.List([yearDGWField,'unique_id','POLYGON_ID']);
#         var toFields = fromFields.replace(yearDGWField,'dgw');
        
#         var igdesYr = trainingGDEs.select(fromFields,toFields);
       
#         igdesYr = igdesYr.filter(ee.Filter.neq('dgw',dgwNullValue));
#         igdesYr = igdesYr.filter(ee.Filter.lte('dgw',maxDGW));
#         igdesYr = igdesYr.filter(ee.Filter.gte('dgw',minDGW));
        
#         // print(igdesYr.size())
#         var applyTrainingTableYr = ee.FeatureCollection(outputApplyTablePath+ yr.toString());
#         igdesYr = getImagesLib.joinFeatureCollectionsReverse(igdesYr,applyTrainingTableYr,'POLYGON_ID');
        
#         // print(igdesYr.size())
        
    
#         return igdesYr;
#       });
#       dgwLTJoined = ee.FeatureCollection(dgwLTJoined).flatten();
#       // dgwLTJoined = dgwLTJoined.filter(ee.Filter.notNull(rfLib.ltFittedIndexList));
#       print(dgwLTJoined.size())
#       Map.addLayer(dgwLTJoined)
#   Export.table.toAsset(dgwLTJoined, outputTrainingTableName,outputTrainingTablePath);
# }
# getTrainingTable()
# function exportApplyTables(){
#   var applyTableExtracted = ee.List.sequence(startApplyYear,endApplyYear).getInfo().map(function(yr){
#         // yr = ee.Number(yr).int16();
        
#         var durFitMagSlopeYr = ee.Image(durFitMagSlope.filter(ee.Filter.calendarRange(yr,yr,'year')).first());
#         durFitMagSlopeYr = durFitMagSlopeYr;
        
#         var igdesYr = durFitMagSlopeYr.reduceRegions(applyGDEs, ee.Reducer.mean(),null,'EPSG:5070',[30,0,-2361915.0,0,-30,3177735.0],4);
#         // igdesYr = getImagesLib.joinFeatureCollections(igdesYr,strataZonalMode,'POLYGON_ID');
#         // print(applyGDEs.size())
        
#         igdesYr = igdesYr.map(function(f){return f.set('year',yr)});
#         // igdesYr = igdesYr.filter(ee.Filter.notNull(rasterFields));
  
#         var yrEnding =+yr.toString();
#         Export.table.toAsset(igdesYr, outputApplyTableName+ yrEnding,outputApplyTablePath + yrEnding);
#         return igdesYr;
#      });
#       // applyTableExtracted = ee.FeatureCollection(applyTableExtracted).flatten();
#       // applyTableExtracted = applyTableExtracted.filter(ee.Filter.notNull(rasterFields));
#   // print(applyTableExtracted)
#   // Export.table.toAsset(dgwLTJoined, outputApplyTableName,outputApplyTablePath);
# }