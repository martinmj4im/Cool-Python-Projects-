Title = ("\nCmpt103W21_X04L_MS1_JM.py 1.00 2021/3/14 Martin Mullappallil" 
         " Johney")

import pprint
import graphics420

"""
****************************************************************************
MS1 Topics: Text/mutability
            File Input
            Lists
            Theme: This milestone focuses on loading two of the ETS files
            (trips.txt and shapes.txt) into Python data structures
            and developing a text interface to access these data structures.

****************************************************************************
"""


def display_menu():
    """
    This function displays the main menu and returns the user's choice
    Parameters: None 
    Returns: menu_choice (string) - the user's input command
    
    """     
     
    print("""
     Edmonton Transit System
---------------------------------
(1) Load shape IDs from GTFS file 
(2) Load shapes from GTFS file 

(4) Print shape IDs for a route
(5) Print points for a shape ID

(7) Save shapes and shape IDs in a pickle 
(8) Load shapes and shape IDs from a pickle 

(9) Display interactive map 

(0) Quit""")    
    
    menu_choice = input("\nEnter command: ")
    while(not menu_choice.isdigit() or menu_choice > "5" or menu_choice < "0"\
          or len(menu_choice) > 1 ):
        menu_choice = input("Enter command: ")    
    
    return menu_choice  
    
#============================================================================

def get_filename(fName):
    '''
    prompts user for a file name, and if nothing is entered, this uses the file
    name fName provided, and returns that prefixed with "data/".; thus, the
    file is expected to be found in folder "data".  NOTE: NO error checking
    '''
    file_name = input("\nEnter a file name [data/trips.txt]: ")
    if file_name == "":
        file_name = "data/" + fName
    
    return file_name

#--------------------------------

def get_filename_shapes(fName):
    '''
    prompts user for a file name, and if nothing is entered, this uses the file
    name fName provided, and returns that prefixed with "data/".; thus, the
    file is expected to be found in folder "data".  NOTE: NO error checking
    '''
    file_name = input("\nEnter a file name [data/shapes.txt]: ")
    if file_name == "":
        file_name = "data/" + fName
    
    return file_name
        
#==========================================================================

def get_data(file_name="data/trips.txt"):
    '''
    This expects a file name, ex. Trips.txt:
       route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id
       1,1-Saturday-1-DEC16-0000010,12300994,"1",0,3271662,1-30-1
       ...
       113,113-Saturday-1-DEC16-0000010,12302515,"1",0,3271595,113-23-1
       ...
    and returns the file contents in a list of strings corresponding to each
    line in the file, or None if the file doesn't exist.
    
    --------------------------------------------------------------
    ['114,114-Weekday-1-DEC16-1111100,12294586,"1",0,3337925,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294587,"1",0,3338173,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294588,"1",0,3338293,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294589,"1",0,3338058,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294590,"1",0,3338324,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294591,"1",0,3338088,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294592,"1",0,3338095,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294593,"1",0,3337977,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294594,"1",0,3338238,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294595,"1",0,3337883,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294596,"1",0,3338238,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294597,"1",0,3337929,114-9-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294598,"1",0,3337830,114-8-1\n',
 '114,114-Weekday-1-DEC16-1111100,12294599,"1",0,3338082,114-9-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303127,"1",0,3271517,115-6-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303128,"1",0,3271517,115-7-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303129,"1",0,3271517,115-6-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303130,"1",0,3292619,115-6-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303131,"1",0,3292619,115-4-1\n',
 '115,115-Saturday-1-DEC16-0000010,12303132,"1",0,3292619,115-6-1\n',
 '115,115-Sunday-1-DEC16-0000001,12287476,"1",0,3271390,115-6-1\n',
    '''
        
    try:
        print("opening file...", end = "")
        file = open(file_name, "rt")
    except:
        print(f"\nThere was a problem opening the file {file_name}")
        return None 
    print("reading file...", end = "")
    data = file.readline()      # Skip 1st line
    data = file.readlines()
    print("done reading.")    
    file.close()
    return data


#--------------------------------------------


def get_shapes_coords(file_name = "data/shapes.txt"):
    '''
    This expects a file name, ex. Shapes.txt:
       shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
       1-30-1,53.53864,-113.42325,1
       ...
       113-22-1,53.51991,-113.62076,78
       ...
    loads the file contents, skips the first line, and returns a dictionary of
    <key, value> pairs, with key = value before the first comma, and value = 
    a list of 2-tuples consisting of two float values after the first comma; ex:
       { '1-30-1' : [ (53.53864, -113.42325), 
                      (53.53863, -113.42329) ... (53.5206, -113.62288) ]
         ...
         '113-22-1' : [ (53.52029, -113.62225), 
                        (53.52024, -113.62194), ... (53.52029, -113.62225) ]
         ... }
    '''

    try:
        print("opening file...", end = "")
        file = open(file_name, "rt")
    except:
        print(f"\nThere was a problem opening the file {file_name}")
        return None 
    print("reading file...", end = "")
    data = file.readline()        # Skip 1st line
    data = file.readlines()
    print("done reading.")    
    file.close()
    return data
    
    
#========================================================================


def create_routes_dict(data):
    '''
    This expects  data list, which is a list of strings corresponding to each 
    line in the file, It skips the first line, and returns a dictionary of
    <key, value> pairs, with key = value before the first comma, and a 
    list a list of strings consisting of the unique element after the 6th comma
    from every line starting with the same key; ex.:
      { '1'  : ["1-30-1", "1-32-1"," 1-31-1"...]
        '113': [113-22-1, 113-24-1, 113-23-1' ... ]
    '''
    routes = {}   # to be returned: routes dict shown above
    
    for line in data:
        
        line = line.strip()
        strpd_line = line.split(",")
        route = strpd_line[0]
        shape_ID = strpd_line[-1]
        if route not in routes:
            routes[route] = [shape_ID]
        else:
            if shape_ID not in routes[route]:
                routes[route].append(shape_ID)
        
        
    return routes


#----------------------------------


def create_coords_dict(data):
    '''
   This expects a list of string and return a dictionary that looks like this:
     { '1-30-1'   : [ (53.53864, -113.42325), (53.53863, -113.42329), 
                      (53.5386, -113.42332), ... (53.5206, -113.62288) ]
       ...
       '977-14-1' : [ (53.45622, -113.42523), (53.45623, -113.42524), 
                      (53.45693, -113.42644), ... (53.45786, -113.42803) ] }
   prompts user for 
   '''
    shapes = {}      # to be returned
    
    for line in data:
        
        line = line.strip()
        shape_ID, lat, lon, seq_no = line.split(",")
        if shape_ID not in shapes:
            #routes[route] = [shape_ID]
            shapes[shape_ID] = [(float(lat), float(lon))]
        else:
            if lat not in shapes[shape_ID]:
                shapes[shape_ID].append((float(lat), float(lon)))
        
        
    return shapes

#========================================================================

def display_ShapeIDs(routes):
    '''
    This expects a dictionary structured as follows:
     {'98': ['98-5-1', '98-6-1'],
      '99': ['99-26-1', '99-25-1', '99-8-1', '99-21-1']}
    prompts user for for a route no., ex. 98, and then displays something like:
       ShapeIDs for 98:
	  98-5-1
          98-6-1
    returns : None
    '''
    usr_route = input("Route?: ")
    if usr_route not in routes:
        print(f"Shape IDs for {usr_route}:\n** NOT FOUND **")
    else:
        for item in routes[usr_route]:
            print(item)
    
    return


#------------------------------------------


def display_coords(shapes):
    '''
    This expects a dictionary structured as follows:
     {'98': ['98-5-1', '98-6-1'],
      '99': ['99-26-1', '99-25-1', '99-8-1', '99-21-1']}
    prompts user for for a route no., ex. 98, and then displays something like:
       ShapeIDs for 98:
	  98-5-1
          98-6-1
    returns : None

    '''
    usr_shapeID = input("Shape ID?: ")
    if usr_shapeID not in shapes:
        print(f"Shape IDs for {usr_shapeID}:\n** NOT FOUND **")
    else:
        print(f"Shape for {usr_shapeID}:")
        for item in shapes[usr_shapeID]:
            print(item)
    
    return

#=========================================================================



def main():
    """
    This is the main function. It calls helper functions to display a menu, 
    open a file, create a dictionary and display specific ShapeIDs for routes,
    or specific co-ordinates within a shapeID.
    Parameters: None 
    Returns: None
    
    """     
    data = "" # data within in either a shapes or trips file
    routes_dict = {}     #dictionary with routes as keys
    coords_dict = {}     #dictionary with shapes as keys
    
    menu_choice = display_menu()
        
    
    while menu_choice != "0":      
        
        if menu_choice == "1":
            file_name = get_filename("trips.txt") 
            data = get_data(file_name)
            
            if data != None:
                routes_dict = create_routes_dict(data)
                
            #pprint.pprint(data)   #test code: if you want to see the data
            #pprint.pprint(routes_dict)#test code: if you want to see the routes
        
        elif menu_choice == "2":
            file_name = get_filename_shapes("shapes.txt")  
            coords_data = get_shapes_coords(file_name)
            #pprint.pprint(coords_data) #Test code to see the structure of
                                        #co-ords data

            if data != None:
                coords_dict = create_coords_dict(coords_data)
                #pprint.pprint(coords_dict)  # test code to make sure the
                                     # co-ordinates data is structures properly
        
        elif menu_choice == "4":
            display_ShapeIDs(routes_dict) 
        
        elif menu_choice == "5":
            display_coords(coords_dict) 
            
        elif menu_choice == "7":
            pass
        
        elif menu_choice == "8":
            pass
        
        elif menu_choice == "9":
            pass        
    
        menu_choice = display_menu() 
    
    if menu_choice == "0":
        print("Goodbye") 
        return    
    
   
   
    
if __name__ == "__main__":
    #Test Code
    print(Title)
    main() 