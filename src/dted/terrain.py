import numpy as np 

class Terrain: 
    def __init__( self ): 
        pass 
    


class Terrain_1D(Terrain):
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
            
        else:
            raise ValueError("Out of bounds latitude slice")
        self.lower = self.bounds.bottom 
        self.upper = self.bounds.top 
        self.range = 'longitude'
    def longitude_slice( self , deg ):
        if( deg > self.bounds.left ) or (deg < self.bounds.right ):
            d = np.absolute( deg - self.long )
            k = np.argmin( d )
            self.x = self.lat
            self.h_slice = self.h[:,k]
            self.alt_slice = self.alt[:,k]
        else:
            raise ValueError("Out of bounds latitude slice")
        self.lower = self.bounds.left 
        self.upper = self.bounds.right 
        self.range = 'latitude'
        return alt_slice 
    def sample(self , deg  ):
        if (deg <= self.lower ) or (deg >= self.upper  ):
            raise IndexError( f"Requested sample at {self.range}={deg} is not in data range [{self.lower},{self.upper}] ")
        return  np.interp( deg , self.x, self.alt_slice )
    def as_matrix( self ):
        return self.h_slice 
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
class Terrain_2D(Terrain):
    def __init__( self, tiffFile , interp='linear'):
        # “linear”, “nearest”, “slinear”, “cubic”, “quintic” and “pchip” 
        
        super().__init__( tiffFile )
        self.grid = si.RegularGridInterpolator(  (self.lat, self.long), self.alt  , method=interp) 
    def show_map( self , figNum , map="map",show=False):
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
    def shape( self ):
        return self.alt.shape 
    def as_matrix( self ):
        return self.alt
    def sample( self , lat , long ):

        o = self.grid( (lat,long))
        return o  