import sqlite3
import pandas as pd

LighRoomDB= sqlite3.connect(r"PATH TO YOUR LR CATALOGUE COPY")

#SECRET SAUCE RECIPE #1: Here is the long SQL command natively compatible with sqlite3 (Lr Catalogue db format)
LighRoomQuery = pd.read_sql_query("SELECT Adobe_images.captureTime as CaptureDateTime, AgLibraryFile.originalFilename as OriginalFilename, replace(AgLibraryFile.importHash, rtrim(AgLibraryFile.importHash, replace(AgLibraryFile.importHash, ':', '')), '') as FileSize, Adobe_images.fileFormat as Type, UPPER(AgLibraryFile.extension) AS Format, AgInternedExifCameraModel.value AS Camera, AgInternedExifLens.value AS Lens, AgHarvestedExifMetadata.focalLength AS Focal, AgHarvestedExifMetadata.isoSpeedRating AS ISO, AgHarvestedExifMetadata.shutterSpeed AS Speed, AgHarvestedExifMetadata.aperture AS Apperture, AgHarvestedExifMetadata.flashFired AS FlashFired, AgHarvestedExifMetadata.gpsLatitude as GPSLatitude, AgHarvestedExifMetadata.gpsLongitude as GPSLongitude FROM Adobe_images INNER JOIN AgHarvestedExifMetadata ON Adobe_images.id_local = AgHarvestedExifMetadata.image INNER JOIN AgLibraryFile ON Adobe_images.rootFile = AgLibraryFile.id_local LEFT OUTER JOIN AgInternedExifLens ON AgHarvestedExifMetadata.lensRef = AgInternedExifLens.id_local LEFT OUTER JOIN AgInternedExifCameraModel ON AgHarvestedExifMetadata.cameraModelRef = AgInternedExifCameraModel.id_local ORDER BY Adobe_images.captureTime", LighRoomDB)
#SECRET SAUCE RECIPE #2: After long research in the db structure, I cannot find the file size. Still it seems the last characters of AgLibraryFile.importHash are correct.
#SECRET SAUCE RECIPE #3: Adobe LightRoom is surely using other mechanisms to retrieve the file size. It can happen the AgLibraryFile.importHash is NULL. The file size will therefore NOT be exported. The only workaround I found is to delete and reimport the file (you may lose some settings!!!)
#SECRET SAUCE RECIPE #4: replace(AgLibraryFile.importHash, rtrim(AgLibraryFile.importHash, replace(AgLibraryFile.importHash, ':', '')), '') is the SQL query to retrieve the file size from the importHash string.

LightRoomDataFrame=pd.DataFrame(LighRoomQuery, columns=['CaptureDateTime','OriginalFilename','FileSize','Format','Type','Camera','Lens','Focal','ISO','Speed','Apperture','FlashFired','GPSLatitude','GPSLongitude'])
LightRoomDataFrame["FileSize"] = pd.to_numeric(LightRoomDataFrame["FileSize"])
LightRoomDataFrame["Focal"] = pd.to_numeric(LightRoomDataFrame["Focal"]).round(1)

#SECRET SAUCE RECIPE #5: The formula to "decode" the Shutter Speed from the Lr Catalogue.
LightRoomDataFrame['Speed']=pd.to_numeric((2**LightRoomDataFrame["Speed"]).round(0), downcast="integer")
#SECRET SAUCE RECIPE #6: 'Inf' could be returned for very long exposure or some video files

#SECRET SAUCE RECIPE #7: The formula to "decode" the Apperture from the Lr Catalogue 
LightRoomDataFrame['Apperture']=(LightRoomDataFrame['Apperture'].div(2)**2).round(1)

LightRoomDataFrame['ISO']=pd.to_numeric(LightRoomDataFrame['ISO'], downcast="integer")
LightRoomDataFrame['CaptureDateTime'] = pd.to_datetime(LightRoomDataFrame['CaptureDateTime'])

LightRoomDataFrame.to_csv(r"PATH TO THE EXPORT CSV FILE",index=False)
#SECRET SAUCE RECIPE #8: Export will use your computer locals you can force colum seperator and decimal seperator. For ie for France : LightRoomDataFrame.to_csv(r"PATH TO THE CSV FILE",sep=';',decimal=',',index=False)

#The LightRoomDataFrame is directly exported to CSV but nothing stops you to play with it using python panda data manipulation beauty !!
