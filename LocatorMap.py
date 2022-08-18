import customtkinter
from tkintermapview import TkinterMapView
import googlemaps


class LocatorMap(customtkinter.CTk):
    customtkinter.set_default_color_theme("blue")
    __APP_NAME = "TkinterMapView with Locator"
    __WIDTH = 1000
    __HEIGHT = 800

    def __current_location(self):
        api_key = 'AIzaSyCJtIhU69bjx_0WbppAURYBbszX18GiCjg'
        gmaps = googlemaps.Client(key=api_key)
        loc = gmaps.geolocate()
        lat = loc["location"]["lat"]
        lng = loc["location"]["lng"]
        return lat, lng

    def __create_frames (self):
        self.grid_columnconfigure ( 0,weight=0 )
        self.grid_columnconfigure ( 1,weight=1 )
        self.grid_rowconfigure ( 0,weight=1 )
        self.__frame_left = customtkinter.CTkFrame ( master=self,width=150,corner_radius=0,fg_color=None )
        self.__frame_left.grid ( row=0,column=0,padx=0,pady=0,sticky="nsew" )
        self.__frame_right = customtkinter.CTkFrame ( master=self,corner_radius=0 )
        self.__frame_right.grid ( row=0,column=1,rowspan=1,pady=0,padx=0,sticky="nsew" )

    def __create_window_panels (self):
        self.__create_frames ()
        # ============ frame_left ============
        self.__frame_left.grid_rowconfigure ( 2,weight=1 )
        self.__button_1 = customtkinter.CTkButton ( master=self.__frame_left,
                                                  text="Set Marker",
                                                  command=self.__set_marker_event )
        self.__button_1.grid ( pady=(20,0),padx=(20,20),row=0,column=0 )
        self.__button_2 = customtkinter.CTkButton ( master=self.__frame_left,
                                                  text="Clear Markers",
                                                  command=self.__clear_marker_event )
        self.__button_2.grid ( pady=(20,0),padx=(20,20),row=1,column=0 )
        self.__map_label = customtkinter.CTkLabel ( self.__frame_left,text="Tile Server:",anchor="w" )
        self.__map_label.grid ( row=3,column=0,padx=(20,20),pady=(20,0) )
        self.__map_option_menu = customtkinter.CTkOptionMenu ( self.__frame_left, values=[ "OpenStreetMap","Google normal",
                                                                                      "Google satellite" ],
                                                             command=self.__change_map )
        self.__map_option_menu.grid ( row=4,column=0,padx=(20,20),pady=(10,0) )
        self.__appearance_mode_label = customtkinter.CTkLabel ( self.__frame_left,text="Appearance Mode:",anchor="w" )
        self.__appearance_mode_label.grid ( row=5,column=0,padx=(20,20),pady=(20,0) )
        self.__appearance_mode_optionemenu = customtkinter.CTkOptionMenu ( self.__frame_left,
                                                                         values=[ "Light","Dark","System" ],
                                                                         command=self.__change_appearance_mode )
        self.__appearance_mode_optionemenu.grid ( row=6,column=0,padx=(20,20),pady=(10,20) )
        # ============ frame_right ============
        self.__frame_right.grid_rowconfigure ( 1,weight=1 )
        self.__frame_right.grid_rowconfigure ( 0,weight=0 )
        self.__frame_right.grid_columnconfigure ( 0,weight=1 )
        self.__frame_right.grid_columnconfigure ( 1,weight=0 )
        self.__frame_right.grid_columnconfigure ( 2,weight=1 )
        self.__map_widget = TkinterMapView ( self.__frame_right,corner_radius=0 )
        self.__map_widget.grid ( row=1,rowspan=1,column=0,columnspan=3,sticky="nswe",padx=(0,0),pady=(0,0) )
        self.__entry = customtkinter.CTkEntry ( master=self.__frame_right,
                                              placeholder_text="type address" )
        self.__entry.grid ( row=0,column=0,sticky="we",padx=(12,0),pady=12 )
        self.__entry.entry.bind ( "<Return>",self.__search_event )
        self.__button_5 = customtkinter.CTkButton ( master=self.__frame_right,
                                                  text="Search",
                                                  width=90,
                                                  command=self.__search_event )
        self.__button_5.grid ( row=0,column=1,sticky="w",padx=(12,0),pady=12 )

    def __default_values (self):
        # set it to current city
        lat, lng = self.__current_location ()
        lat = str(lat)
        lng = str(lng)
        self.__map_widget.set_address(lat + "," + lng)
        self.__map_option_menu.set("Google satellite")
        self.__appearance_mode_optionemenu.set("System")

    def __init__(self, *args, **kwargs):
        super ().__init__ ( *args,**kwargs )
        self.title (LocatorMap.__APP_NAME )
        self.geometry ( str ( LocatorMap.__WIDTH ) + "x" + str ( LocatorMap.__HEIGHT ) )
        self.minsize ( LocatorMap.__WIDTH, LocatorMap.__HEIGHT )
        # things marks on the map
        self.__marker_list = [ ]
        # create windows panels for map and GUIs
        self.__create_window_panels ()
        # Set default values
        self.__default_values ()

    def __search_event(self, event=None):
        self.__map_widget.set_address(self.__entry.get (),bool=False)

    def __set_marker_event(self):
        current_position = self.__map_widget.get_position()
        self.__marker_list.append ( self.__map_widget.set_marker ( current_position [ 0 ],current_position [ 1 ] ) )

    def __clear_marker_event (self):
        for marker in self.__marker_list:
            marker.delete()

    def __change_appearance_mode (self,new_appearance_mode: str):
        customtkinter.set_appearance_mode ( new_appearance_mode )

    def __change_map (self,new_map: str):
        if new_map == "OpenStreetMap":
            self.__map_widget.set_tile_server ( "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom= 16 )
        elif new_map == "Google normal":
            self.__map_widget.set_tile_server ( "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                              max_zoom=16 )
        elif new_map == "Google satellite":
            self.__map_widget.set_tile_server ( "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                              max_zoom=16 )

    def __on_closing(self):
        self.destroy()

    def start (self):
        self.mainloop()

    def get_location(self):
        lat, lng = self.__current_location()
        return f'Lat: {lat}, Lng: {lng}'
