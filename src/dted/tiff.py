import numpy as np
import os 
import rasterio as rio
import scipy.interpolate as si
import logging 
from urllib.parse import urlparse
import requests 

log = logging.getLog( __name__ ) 

class Terrain:
    def __init__( self , url , cache="/tmp"):    
        self.cache = cache 
        parsed_url = urlparse(url)
        if  parsed_url.scheme in ['http', 'https']:
            log.info(f"Loading URL from {url}")
            self.download_url( url )
        elif os.path.isfile(url):
            log.info(f"Loading file from {url}")
        else:
            raise FileNotFoundError(f"Not found: {url}")
        self.load_tiff( )
    def download_url( self,  url  ):
        try:
            # Get the file from the URL
            response = requests.get(url)
            response.raise_for_status()  # Will raise an error for bad responses
            print("Loaded content from URL")
            with open( savePath, 'wb') as f: 
                f.write( response.content )
        except requests.exceptions.RequestException as e:
            print(f"Error while fetching the URL: {e}")
    def load_tiff( self, filename ):
        with rio.open( filename ) as f:
            self.h=  f.read( 1 )
            self.bounds = f.bounds 
            self.long = np.linspace(  f.bounds.left , f.bounds.right,num=f.width )
            self.lat  = np.linspace( f.bounds.top , f.bounds.bottom ,num=f.height )
            self.water = np.isclose( self.h ,-9999,atol=10 )
            self.alt = np.copy( self.h ) 
            self.alt[self.water] = -1
            self.alt = self.alt / 1000.0 # km
class Terrain_1D(TiffTerrain):
    def __init__( self , tiffFile , deg,  axis ):
        super().__init__( tiffFile )
        self.deg = deg 
        if axis=="lat":
            self.latitude_slice( deg )
        elif axis=="long":
            self.longitude_slice( deg )
        else:
            raise ValueError("Axis must be 'lat' or 'long' to support latitude and longitude slicing")
    def latitude_slice( self , deg ):
        if( deg < self.bounds.bottom ) or ( deg < self.bounds.top ):
            d = np.absolute( deg - self.lat )
            k = np.argmin( d )
            self.h_slice = self.h[ k , :]
            self.alt_slice = self.alt[k,:]
            self.x = self.long
            self.xlabel = "Longitude (deg)"
        else:
            raise ValueError("Out of bounds latitude slice")
    def longitude_slice( self , deg ):
        if( deg > self.bounds.left ) or (deg < self.bounds.right ):
            d = np.absolute( deg - self.long )
            k = np.argmin( d )
            self.x = self.lat
            self.xlabel = "Latitude (deg)"
            self.h_slice = self.h[:,k]
            self.alt_slice = self.alt[:,k]
        else:
            raise ValueError("Out of bounds latitude slice")
    def sample(self , deg  ):
        return  np.interp( deg , self.x, self.alt_slice )
    def show_map( self , figNum, map="map" ):
        if map == "map":
            H = self.h_slice
        else:
            H = self.alt_slice
        plt.figure(figNum)
        plt.plot( self.x , H  )
        plt.xlabel(self.xlabel)
        plt.ylabel("Altitude")
        plt.show()
    
    def getProfile( self ):
        return self.h_slice
class Terrain_2D(TiffTerrain):
    def __init__( self, tiffFile ):
        super().__init__( tiffFile )
        self.grid = si.RegularGridInterpolator(  (self.lat, self.long), self.alt  , method="linear")
    def show( self , figNum , map="map",show=False):
        if map == "map":
            H = self.h
        else:
            H = self.alt
        plt.figure(figNum)
        plt.pcolormesh( self.long, self.lat , H,cmap='terrain' )
        plt.xlabel("Longitude (deg)")
        plt.ylabel("Latitude (deg)")
        if show:
            plt.show()
    def arg_lat( self , latitiude ):
        if( latitude >= self.bounds.lower ) and ( latitude =< self.bounds.upper ):
            pass
        else:
            raise IndexError(f"Latitude {latitiude} is not in range [{self.bounds.lower},{self.bounds.upper}]")
     def arg_long( self , longitude ): 
         if( longitude > self.bounds.left ) or (longitude < self.bounds.right ): 
    def shape( self ):
        return self.alt.shape 
    def as_matrix( self ):
        return self.alt
    def sample( self , lat , long ):

        o = self.grid( (lat,long))
        return o  