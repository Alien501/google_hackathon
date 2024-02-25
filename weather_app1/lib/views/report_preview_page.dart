import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:open_file/open_file.dart';
import 'package:screenshot/screenshot.dart';

import '../constants/popup.dart';
import '../constants/severity_widget.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:share/share.dart';
import 'package:permission_handler/permission_handler.dart';


class ReportPreviewPage extends StatefulWidget {
  final User user;

  ReportPreviewPage({required this.user});
  @override
  _ReportPreviewPageState createState() => _ReportPreviewPageState();
}

class _ReportPreviewPageState extends State<ReportPreviewPage> {

  final GlobalKey<ScreenshotState> screenshotKey = GlobalKey<ScreenshotState>();
  final ScreenshotController screenshotController = ScreenshotController();
  bool isPopupVisible = false;
  String doubleToStringAsFixed(double value, int fractionDigits) {
    return value.toStringAsFixed(fractionDigits);
  }

  void onPopupClick(String title, String content, double value) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return PopupContent(title: title, content: content,value: value);
      },
    );
  }
  String getPlantImageUrl(String plantName) {
    switch (plantName.toLowerCase()) {
      case 'apples':
        return 'https://images.pexels.com/photos/102104/pexels-photo-102104.jpeg?cs=srgb&dl=pexels-mali-maeder-102104.jpg&fm=jpg';
      case 'apricots':
        return 'https://us.images.westend61.de/0000195211pw/apricots-on-white-background-close-up-CSF016147.jpg';
      case 'blackberries':
        return 'https://img.freepik.com/premium-photo/sweet-blackberries-berries-with-leaves-white-background_183352-864.jpg';
      case 'tomato':
        return 'https://i.pinimg.com/736x/b0/e5/d0/b0e5d0f0b275f9c420fed1ae16ea7f08.jpg';
      case 'lettuce':
        return 'https://img.freepik.com/premium-photo/lettuce-leaves-isolated-white-background_62856-5407.jpg';
      case 'carrot':
        return 'https://st2.depositphotos.com/2577341/9531/i/450/depositphotos_95313678-stock-photo-fresh-carrot-on-white.jpg';
      default:
        return '';
    }
  }

  Future<void> _saveDataToFile() async {
    String jsonData = json.encode(data);
    var status = await Permission.storage.status;
    if (status.isDenied) {
      await Permission.storage.request();
    }

    Directory? appDocDir = await getExternalStorageDirectory();
    if (appDocDir != null) {
      String appDocPath = appDocDir.path;
      File file = File('$appDocPath/report_data.json');

      await file.writeAsString(jsonData);
      OpenFile.open(file.path);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Data downloaded successfully'),
        ),
      );
      print('File path: ${file.path}');
    } else {
      print('Error getting external storage directory');
    }
  }


  File? _image;
  Future<void> _getImageFromCamera() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  void _shareImage() async {
    Uint8List? imageBytes = await screenshotController.capture();

    if (imageBytes != null) {
      final tempDir = await getTemporaryDirectory();
      final tempFile = File('${tempDir.path}/screenshot.png');
      await tempFile.writeAsBytes(imageBytes);
      Share.shareFiles([tempFile.path], text: 'Check out my environmental report!');
    } else {
      print('Failed to capture screenshot.');
    }
  }

  void onClosePopup() {
    setState(() {
      isPopupVisible = false;
    });
  }

  final Map<String, dynamic> data = {
    "co": {
      "etc": {
        "severity": "normal",
        "source": "The presence of CO, SO2, and formaldehyde could indicate pollution from sources like traffic, industry"
      },
      "value": 0.047780553080211174
    },
    "era5": {
      "etc": "NA",
      "value": {
        "res": {
          "temperature": 1.1767428749486157,
          "total_precipitation": 0.0013581420279012348,
          "wind_direction": "East"
        }
      }
    },
    "formaldehyde": {
      "etc": {
        "severity": "low",
        "source": "Formaldehyde is a volatile organic compound that can be emitted from various sources, including combustion processes and certain industrial activities"
      },
      "value": 0.00011456657342659141
    },
    "ozone": {
      "etc": {
        "severity": "low",
        "source": " Air quality is generally good and these levels are considered safe for general population"
      },
      "value": 0.13963791430409556
    },
    "plant_data": [
      "Apples",
      "Apricots",
      "Blackberries",
      "Tomato",
      "Lettuce",
      "Carrot"
    ],
    "population": {
      "etc": {
        "severity": "normal",
        "source": "Strikes a balance between community resources and demand, supporting a mix of economic activities, infrastructure, and social services"
      },
      "value": 245.15034415301153
    },
    "so2": {
      "etc": {
        "severity": "normal",
        "source": "Elevated SO2 levels may indicate industrial processes or combustion of sulfur-containing fuels, potentially contributing to air pollution"
      },
      "value": 0.00024554517028597874
    },
    "soil_data": {
      "etc": {
        "Sensible_heat_net_flux_surface_6_Hour_Average_stat": {
          "severity": "low",
          "source": "Represents the average net flux of sensible heat at the Earth's surface over a 6-hour period. Higher values indicate increased heat transfer from the surface to the atmosphere, while lower values suggest reduced heat transfer"
        },
        "Specific_humidity_height_above_ground_stat": {
          "severity": "low",
          "source": "Represents the specific humidity (moisture content) at a certain height above the ground. Higher values indicate higher moisture content in the air, while lower values suggest drier condition"
        },
        "Temperature_height_above_ground_stat": {
          "severity": "low",
          "source": "Represents the temperature at a certain height above the ground. Higher values indicate warmer temperatures, while lower values suggest cooler temperatures"
        },
        "Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat": {
          "severity": "normal",
          "source": "Represents the average upward long-wave radiation flux at the Earth's surface over a 6-hour period. Higher values indicate increased heat emitted from the Earth's surface, while lower values suggest reduced heat emission"
        },
        "Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat": {
          "severity": "normal",
          "source": "Represents the average upward short-wave radiation flux at the Earth's surface over a 6-hour period. Higher values indicate increased sunlight reflected from the Earth's surface, while lower values suggest reduced sunlight reflection."
        },
        "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat": {
          "severity": "normal",
          "source": "Represents the volumetric soil moisture content at a depth of 150cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions"
        },
        "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat": {
          "severity": "high",
          "source": "Represents the volumetric soil moisture content at a depth of 25cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions."
        },
        "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat": {
          "severity": "high",
          "source": "Represents the volumetric soil moisture content at a depth of 5cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions"
        },
        "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat": {
          "severity": "high",
          "source": "Represents the volumetric soil moisture content at a depth of 70cm below the surface layer. : Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions."
        },
        "u_component_of_wind_height_above_ground_stat": {
          "severity": "high",
          "source": "Represents the east-west component of wind velocity at a certain height above the ground. Positive values indicate eastward wind flow, while negative values suggest westward wind flow"
        },
        "v_component_of_wind_height_above_ground_stat": {
          "severity": "normal",
          "source": "Represents the north-south component of wind velocity at a certain height above the ground. Positive values indicate northward wind flow, while negative values suggest southward wind flow"
        }
      },
      "value": {
        "res": [
          {
            "Downward_Long-Wave_Radp_Flux_surface_6_Hour_Average": 279.86810203200866
          },
          {
            "Downward_Short-Wave_Radiation_Flux_surface_6_Hour_Average": 124.06800596316732
          },
          {
            "Geopotential_height_surface": 7.283279677581637
          },
          {
            "Latent_heat_net_flux_surface_6_Hour_Average": 37.34717449573548
          },
          {
            "Maximum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval": 0.004486508774242517
          },
          {
            "Maximum_temperature_height_above_ground_6_Hour_Interval": 278.74934301849504
          },
          {
            "Minimum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval": 0.003851255038064647
          },
          {
            "Minimum_temperature_height_above_ground_6_Hour_Interval": 275.3193511812082
          },
          {
            "Potential_Evaporation_Rate_surface_6_Hour_Average": 75.13827433513545
          },
          {
            "Precipitation_rate_surface_6_Hour_Average": 3.378713781010495e-05
          },
          {
            "Pressure_surface": 102535.42305173949
          },
          {
            "Sensible_heat_net_flux_surface_6_Hour_Average": 5.736452822393995
          },
          {
            "Specific_humidity_height_above_ground": 0.00415349383323937
          },
          {
            "Temperature_height_above_ground": 277.120471544901
          },
          {
            "u-component_of_wind_height_above_ground": 0.2416082489311424
          },
          {
            "Upward_Long-Wave_Radp_Flux_surface_6_Hour_Average": 334.1174768469366
          },
          {
            "Upward_Short-Wave_Radiation_Flux_surface_6_Hour_Average": 18.617749329729264
          },
          {
            "v-component_of_wind_height_above_ground": -1.4056331777223887
          },
          {
            "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm": 0.35863299929098924
          },
          {
            "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm": 0.3607088901304307
          },
          {
            "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm": 0.3606587783353417
          },
          {
            "Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm": 0.34510671364905254
          }
        ]
      }
    },
    "vegetation": {
      "etc": {
        "NDVI": {
          "severity": "low",
          "source": "Sparse or no vegetation cover. Often associated with barren land, deserts, urban areas, or water bodies"
        },
        "NDWI": {
          "severity": "normal",
          "source": "Moderate water content, including water bodies such as rivers, lakes, and wetlands. Also includes areas with some moisture in the soil or vegetation"
        }
      },
      "value": {
        "res": {
          "EVI Value": 0.01394745676508789,
          "NDVI Value": -0.0022599191384962912,
          "NDWI Value": -0.0237010992812586
        }
      }
    },
    "water": {
      "value": {
        "res": {
          "lwe_thickness_csr": -0.3799036145210266
        }
      }
    }
  };

  @override
  Widget build(BuildContext context) {
    // print(data['soil_data']['value']['res'].length);
    return Scaffold(
      backgroundColor: Color(0xff7461e5),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(height: 20,),
              Container(
                padding: EdgeInsets.all(8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Image.asset('assets/logo.png'),
                    Text('Welcome \n${widget.user.displayName}',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.right,
                    ),
                  ],
                ),
              ),
              SizedBox(height: 10,),
              Text(
                'Basic parameter for your location',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 10,),
              SizedBox(height: 16.0),
              Row(
                children: [
                  Container(
                    height: MediaQuery.sizeOf(context).width/2.3,
                    width: MediaQuery.sizeOf(context).width/2.3,
                    child: GestureDetector(
                      onTap: () {
                        print(data['co']['etc']);
                        onPopupClick('CO', data['co']['etc']['source'], data['co']['value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['co']['etc']['severity'],
                          label: 'CO',
                        ),
                      ),
                    ),
                  ),
                  SizedBox(width: 16.0),
                  Container(
                    height: MediaQuery.sizeOf(context).width / 2.3,
                    width: MediaQuery.sizeOf(context).width / 2.3,
                    child: GestureDetector(
                      onTap: () {
                        onPopupClick('Formaldehyde', data['formaldehyde']['etc']['source'],data['formaldehyde']['value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['formaldehyde']['etc']['severity'],
                          label: 'Formaldehyde',
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16.0),
              Row(
                children: [
                  Container(
                    height: MediaQuery.sizeOf(context).width / 2.3,
                    width: MediaQuery.sizeOf(context).width / 2.3,
                    child: GestureDetector(
                      onTap: () {
                        onPopupClick('Ozone', data['ozone']['etc']['source'],data['ozone']['value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['ozone']['etc']['severity'],
                          label: 'OZONE',
                        ),
                      ),
                    ),
                  ),
                  SizedBox(width: 16.0),
                  Container(
                    height: MediaQuery.sizeOf(context).width / 2.3,
                    width: MediaQuery.sizeOf(context).width / 2.3,
                    child: GestureDetector(
                      onTap: () {
                        onPopupClick('Population', data['population']['etc']['source'],data['population']['value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['population']['etc']['severity'],
                          label: 'Population',
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16.0),
              Row(
                children: [
                  Container(
                    height: MediaQuery.sizeOf(context).width / 2.3,
                    width: MediaQuery.sizeOf(context).width / 2.3,
                    child: GestureDetector(
                      onTap: () {
                        onPopupClick('SO2', data['so2']['etc']['source'],data['so2']['value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['so2']['etc']['severity'],
                          label: 'SO2',
                        ),
                      ),
                    ),
                  ),

                  SizedBox(width: 16.0),
                  Stack(
                    children: [
                      Container(
                        height: MediaQuery.sizeOf(context).width / 2.3,
                        width: MediaQuery.sizeOf(context).width / 2.3,
                        decoration: BoxDecoration(

                          image: DecorationImage(
                            image: AssetImage('assets/rainy-day.png'),
                            fit: BoxFit.cover,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                      ),

                      ClipRRect(
                        borderRadius: BorderRadius.circular(10.0),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                          child: Container(
                            height: MediaQuery.sizeOf(context).width / 2.3,
                            width: MediaQuery.sizeOf(context).width / 2.3,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(10.0),
                              border: Border.all(
                                color: Colors.white,
                                width: 2.0,
                              ),
                            ),
                            child: Center(
                              child: Text(
                                "Precipitation rate:\n${doubleToStringAsFixed(data["soil_data"]["value"]["res"][9]["Precipitation_rate_surface_6_Hour_Average"], 6)} mm",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),

                ],
              ),
              SizedBox(height: 16.0),
              Row(
                children: [
                  Stack(
                    children: [
                      Container(
                        height: MediaQuery.sizeOf(context).width / 2.3,
                        width: MediaQuery.sizeOf(context).width / 2.3,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/wind.png'),
                            fit: BoxFit.cover,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10.0),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                          child: Container(
                            height: MediaQuery.sizeOf(context).width / 2.3,
                            width: MediaQuery.sizeOf(context).width / 2.3,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(10.0),
                              border: Border.all(
                                color: Colors.white,
                                width: 2.0,
                              ),
                            ),
                            child: Center(
                              child: Text(
                                "Wind Speed: ${data["soil_data"]["etc"]["u_component_of_wind_height_above_ground_stat"]["severity"]}\nWind Direction: ${data["era5"]["value"]['res']["wind_direction"]}",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),

                  SizedBox(width: 16.0),

                  Stack(
                    children: [
                      Container(
                        height: MediaQuery.sizeOf(context).width / 2.3,
                        width: MediaQuery.sizeOf(context).width / 2.3,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/pressure.png'),
                            fit: BoxFit.cover,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10.0),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                          child: Container(
                            height: MediaQuery.sizeOf(context).width / 2.3,
                            width: MediaQuery.sizeOf(context).width / 2.3,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(10.0),
                              border: Border.all(
                                color: Colors.white,
                                width: 2.0,
                              ),
                            ),
                            child: Center(
                              child: Text(
                                'Pressure: \n${doubleToStringAsFixed(data["soil_data"]["value"]["res"][10]["Pressure_surface"], 2)} mm',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),

                ],
              ),
              SizedBox(height: 16.0),
              Row(
                children: [
                  Stack(
                    children: [
                      Container(
                        height: MediaQuery.sizeOf(context).width / 2.3,
                        width: MediaQuery.sizeOf(context).width / 2.3,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/temp.png'),
                            fit: BoxFit.cover,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10.0),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                          child: Container(
                            height: MediaQuery.sizeOf(context).width / 2.3,
                            width: MediaQuery.sizeOf(context).width / 2.3,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(10.0),
                              border: Border.all(
                                color: Colors.white,
                                width: 2.0,
                              ),
                            ),
                            child: Center(
                              child: Text(
                                "Temperature\n${doubleToStringAsFixed(data["soil_data"]["value"]["res"][13]["Temperature_height_above_ground"],2)} Kelvin",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(width: 16.0),
                  Stack(
                    children: [
                      Container(
                        height: MediaQuery.sizeOf(context).width / 2.3,
                        width: MediaQuery.sizeOf(context).width / 2.3,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/humidity.png'),
                            fit: BoxFit.cover,
                          ),
                          borderRadius: BorderRadius.circular(10.0),
                        ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10.0),
                        child: BackdropFilter(
                          filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                          child: Container(
                            height: MediaQuery.sizeOf(context).width / 2.3,
                            width: MediaQuery.sizeOf(context).width / 2.3,
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(10.0),
                              border: Border.all(
                                color: Colors.white,
                                width: 2.0,
                              ),
                            ),
                            child: Center(
                              child: Text(
                                "Specific Humidity:\n${doubleToStringAsFixed(data["soil_data"]["value"]["res"][12]["Specific_humidity_height_above_ground"],5)} kg/kg",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold,
                                ),

                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              SizedBox(height: 30,),
              Text(
                "Plants that can be grown",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 25.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Container(
                height: MediaQuery.sizeOf(context).height / 2,
                width: MediaQuery.sizeOf(context).width,
                child: Column(
                  children: List.generate(data['plant_data'].length, (index) {
                    String plantName = data['plant_data'][index];
                    String imageUrl = getPlantImageUrl(plantName);

                    return Card(
                      elevation: 5.0,
                      margin: EdgeInsets.symmetric(vertical: 2.0, horizontal: 4.0),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      child: ListTile(
                        title: Text(
                          plantName,
                          style: TextStyle(
                            color: Colors.black,
                            fontSize: 20.0,
                          ),
                        ),
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(5.0),
                          child: Image.network(
                            imageUrl,
                            width: 50.0,
                            height: 50.0,
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                    );
                  }),
                ),
              ),


              Text(
                "Vegetation Details",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 25.0,
                  fontWeight: FontWeight.bold,
                ),

              ),
              Container(
                height: MediaQuery.sizeOf(context).height / 3,
                width: MediaQuery.sizeOf(context).width,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    GestureDetector(
                      onTap: () {
                        onPopupClick('NDVI', data['vegetation']['etc']['NDVI']['source'], data['vegetation']['value']['res']['NDVI Value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['vegetation']['etc']['NDVI']['severity'],
                          label: 'NDVI',
                        ),
                      ),
                    ),
                    GestureDetector(
                      onTap: () {
                        onPopupClick('NDWI', data['vegetation']['etc']['NDWI']['source'], data['vegetation']['value']['res']['NDWI Value']);
                      },
                      child: Center(
                        child: SeverityWidget(
                          severity: data['vegetation']['etc']['NDWI']['severity'],
                          label: 'NDWI',
                        ),
                      ),
                    ),
                  ],
                ),
              ),


              SizedBox(height: 20,),
              Column(
                children: [
                  // Previous widgets...

                  SizedBox(height: 20),
                  Text(
                    "Advance Parameters",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  //SliverGridDelegateWithFixedCrossAxisCount

                  Container(
                    height: MediaQuery.sizeOf(context).height / 2,
                    width: MediaQuery.sizeOf(context).width,
                    child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 1,
                          childAspectRatio: MediaQuery.of(context).size.width /
                              (MediaQuery.of(context).size.height /7.9)
                      ),
                      itemCount: data['soil_data']['value']['res'].length,
                      itemBuilder: (BuildContext context, int index) {
                        String paramName = data['soil_data']['value']['res'][index].keys.first;
                        double paramValue = data['soil_data']['value']['res'][index][paramName];

                        return Card(
                          color: Colors.white,
                          elevation: 5.0,
                          margin: EdgeInsets.symmetric(vertical: 8.0, horizontal: 8.0),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(50.0),
                          ),
                          child: ListTile(
                            title: Text(
                              "${paramName.replaceAll('_', ' ')}: ${paramValue.toStringAsFixed(5)}",
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 17.0,
                              ),
                              textAlign: TextAlign.center,
                            ),
                            onTap: () {
                              onPopupClick(paramName.replaceAll('_', ' '), "", paramValue);
                            },
                          ),
                          // ),
                        );

                      },
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20,),


              DropdownButton<String>(
                value: 'Share your moment',
                onChanged: (String? newValue) {
                  if (newValue == 'Take a picture') {
                    _getImageFromCamera();
                  } else if (newValue == 'Share Captured Image') {
                    _shareImage();
                  }
                },
                items: ['Share your moment', 'Take a picture', 'Share Captured Image']
                    .map((String option) {
                  return DropdownMenuItem<String>(
                    value: option,
                    child: Text(option),
                  );
                }).toList(),
                icon: Icon(Icons.arrow_drop_down, color: Colors.white),
              ),

              SizedBox(height: 16.0),

              if (_image != null)
                Screenshot(
                  key: screenshotKey,
                  controller: screenshotController,
                  child:Container(
                    height: MediaQuery.of(context).size.height/2.5,
                    width: MediaQuery.of(context).size.width/2.5,
                    child: Stack(
                      children: [
                        Positioned.fill(
                          child: Container(
                            height: MediaQuery.of(context).size.height,
                            width: MediaQuery.of(context).size.width,
                            child: Image.asset(
                              'assets/custom_frame.png',
                              fit: BoxFit.contain,
                            ),
                          ),
                        ),
                        Positioned(
                          top: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            height: MediaQuery.of(context).size.height / 3.5,
                            width: MediaQuery.of(context).size.width,
                            child: Padding(
                              padding: EdgeInsets.only(top: 75.0),
                              child: Image.file(
                                _image!,
                                fit: BoxFit.contain,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              SizedBox(height: 20,),
              Column(
                children: [
                  FloatingActionButton(
                    onPressed: () async {
                      await _saveDataToFile();
                    },
                    child: Icon(Icons.download),
                  ),
                  SizedBox(height: 8.0),
                  Text(
                    "Download Data",
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                ],
              ),

            ],

          ),
        ),
      ),
    );
  }
}
