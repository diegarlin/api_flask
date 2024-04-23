import requests
import base64
BUID = "building_3f91a8fd-ca7b-4d7e-bc04-626e2623d229_1704557723480"

url_base = "https://ap.cs.ucy.ac.cy:44"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "access_token": "apGoogle_wyeF4kjtzt4565tUEZl1nRLflBpx4KfN5XKgpAaR0L18YePMZvzX3zCwSXT5QQAaTEsI5OD5p96mcAUAAgmWCqrjKcx77BTOcH6tCu9eIvzWtaeOr5ae1jlT8IedJw6miNsJvQUql5o9uOETekTpQ4DX04Svb6kTvacLkh7ym8mcIno7LvOf0cU2EWHvit8Y64MfbUrsnBB6zSHhGSZkageVvM3z9nxc4OlYo8tf9vu5MI2sMso77u27e5QTJPg35ZYMMh5MB171KGMxLSxoCg9hdK91AaHhS1JIXVQc9ZigHuqtH4Dm4vVNJfua5H0rewQOqmh7i9dj2sMTKKWdKTDy64DAh64Z9hHD0O0R9CC9fQxgcHGgq5e0j2RQyfLJOeoaiZY3ycKqFl0xcYKznsYWmBm0fBzhW1El6ySAKpLrcDjbO5wkcCOMgUxZcHq2ZBGNF0Ygu8CEsXgJUytXyS9V2ICXSrBgxx8B6LTneT7B0leYkPF2ap"
}


data = {
    #Building ID for ETSII
    "buid": BUID

    }

def post(url, data, headers):

    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Respuesta exitosa:")
            print(response.json())
            return response.json()
        else:
            print(f"Error en la solicitud: {response.status_code}")
    except Exception as e:
        print(f"Error en la solicitud: {e}")

def post_binary(url, data, headers):
    try:
        response = requests.post(url, json=data, headers=headers)
    
        if response.status_code == 200:
            base64_data = response.text

            # Decodificar el contenido base64
            binary_data = base64.b64decode(base64_data)

            # Guardar el contenido binario en un archivo local
            with open("archivo.png", "wb") as file:
                file.write(binary_data)

            print("Archivo decodificado y guardado exitosamente.")
        else:
            print(f"Error en la solicitud: {response.__attrs__}")
    except Exception as e:
        print(f"Error en la solicitud: {e}")
    
if __name__ == "__main__":
    # GET ETSII
    # post(url_base+"/api/mapping/space/get", data, headers)

    # EDIT ETSII
    # edit_data = {
    #     "buid": BUID,
    #     "name": "ETSIi"
    # }
    # post(url_base+"/api/auth/mapping/space/update", edit_data,headers)

    # GET ALL ETSII FLOORS
    # data = post(url_base+"/api/mapping/floor/all", data, headers)
    # for floor in data['floors']:
    #     print(f"Floor name: {floor.get('floor_name')}")
    #     print(f"FUID: {floor.get('fuid')}")
    #     print(f"BUID: {floor.get('buid')}")
    #     print(f"Is published: {floor.get('is_published')}")
    #     print(f"Description: {floor.get('description')}")
    #     print(f"Floor number: {floor.get('floor_number')}")
    #     print(f"Zoom: {floor.get('zoom')}")
    #     print(f"Bottom left latitude: {floor.get('bottom_left_lat')}")
    #     print(f"Bottom left longitude: {floor.get('bottom_left_lng')}")
    #     print(f"Top right latitude: {floor.get('top_right_lat')}")
    #     print(f"Top right longitude: {floor.get('top_right_lng')}")
    #     print()

    # DOWNLOAD FLOORPLAN PNG
    # post_binary(url_base+"/api/floorplans64/building_3f91a8fd-ca7b-4d7e-bc04-626e2623d229_1704557723480/0", {}, headers)

    # GET ALL POIS OF x FLOOR
    # get_pois_data = {
    #     "buid": BUID,
    #     "floor_number": "0"
    # }
    # data = post(url_base+"/api/mapping/pois/floor/all", get_pois_data, headers)

    # for poi in data['pois']:
    #     print(f"Poi name: {poi.get('name')}")
    #     print(f"Poi image: {poi.get('image')}")
    #     print(f"Poi floor_number: {poi.get('floor_number')}")
    #     print(f"Poi is_building_entrance: {poi.get('is_building_entrance')}")
    #     print(f"Poi floor_name: {poi.get('floor_name')}")
    #     print(f"Poi is_door: {poi.get('is_door')}")
    #     print(f"Poi puid: {poi.get('puid')}")
    #     print(f"Poi coordinates_lon: {poi.get('coordinates_lon')}")
    #     print(f"Poi coordinates_lat: {poi.get('coordinates_lat')}")
    #     print(f"Poi buid: {poi.get('buid')}")
    #     print(f"Poi pois_type: {poi.get('pois_type')}")
    #     print(f"Poi is_published: {poi.get('is_published')}")

    # SEARCH POI
    # search_poi_data = {
    #     "cuid": "cuid_6b0a3e34-9997-462c-2dec-7f0e76cce1ca_1708272924486",
    #     "letters": "Emergencia",
    #     "buid": BUID,
    #     "greeklish": "false"
    # }
    # data = post(url_base+"/api/mapping/pois/search", search_poi_data, headers)

    # for poi in data['pois']:
    #     print(f"Poi name: {poi.get('name')}")
    #     print(f"Poi image: {poi.get('image')}")
    #     print(f"Poi floor_number: {poi.get('floor_number')}")
    #     print(f"Poi is_building_entrance: {poi.get('is_building_entrance')}")
    #     print(f"Poi floor_name: {poi.get('floor_name')}")
    #     print(f"Poi is_door: {poi.get('is_door')}")
    #     print(f"Poi puid: {poi.get('puid')}")
    #     print(f"Poi coordinates_lon: {poi.get('coordinates_lon')}")
    #     print(f"Poi coordinates_lat: {poi.get('coordinates_lat')}")
    #     print(f"Poi buid: {poi.get('buid')}")
    #     print(f"Poi pois_type: {poi.get('pois_type')}")
    #     print(f"Poi is_published: {poi.get('is_published')}")

    # FIND FASTEST ROUTE ENTRE COORDENADAS
    # fastest_route_data = {
    #     "coordinates_lat": "37.35856484984483",
    #     "coordinates_lon": "-5.986675044027709",
    #     "floor_number": "1",
    #     "pois_to": "poi_9b57957a-332d-43c2-8ddd-4b01fabfc53d"
    # }

    # data = post(url_base+"/api/navigation/route/coordinates", fastest_route_data, headers)

    #FIND FASTETS ROUTE ENTRE POIS 

    # fastest_route_data =  {
    #     "pois_from": "poi_a8834a26-6e4b-460b-be6b-f027f5c58e52", # A0.13
    #     "pois_to": "poi_c2687321-0e4f-431b-92bd-0f537aff1f74" #A0.12
    # }
   
    # data = post(url_base+"/api/navigation/route", fastest_route_data, headers)

    

    # # UPDATE POI
    # update_poi_data =    {
    #     "buid": BUID,
    #     "puid": "poi_c2687321-0e4f-431b-92bd-0f537aff1f74",
    #     "name": "A0.12"
    # }

    # data = post(url_base+"/api/auth/mapping/pois/update", update_poi_data, headers)

    # # GET POI
    get_poi_data =    {
        "pois": "poi_c2687321-0e4f-431b-92bd-0f537aff1f74"
    }

    data = post(url_base+"/api/navigation/pois/id", get_poi_data, headers)