import 'package:flutter/material.dart';
import 'dart:ui' as ui;



class PopupContent extends StatelessWidget {
  final String title;
  final String content;
  final double value;
  String doubleToStringAsFixed(double value, int fractionDigits) {
    return value.toStringAsFixed(fractionDigits);
  }

  PopupContent({required this.title, required this.content, required this.value});

  String getImagePath(String title) {
    Map<String, String> imagePaths = {
      'CO': 'assets/co.png',
      'Formaldehyde': 'assets/form.png',
      'Population': 'assets/pop1.png',
      'Ozone': 'assets/ozo.png',
      'SO2': 'assets/so2.png',
    };

    return imagePaths[title] ?? 'assets/default_image.jpg';
  }

  @override
  Widget build(BuildContext context) {
    return BackdropFilter(
      filter: ui.ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
      child: AlertDialog(
        backgroundColor: Colors.black45,
          shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10.0),
          side: BorderSide(
            color: Color(0xFF00FFCE),
            width: 2.0,
          ),
          ),
        title: Column(
          children: [
            Column(
              children: [
                Text(title,
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),

                SizedBox(height: 10,),
                Image.asset(
                    getImagePath(title),
                    height: 200.0,
                    width: 200.0,
                  ),
                Text(doubleToStringAsFixed(value,5),
                  style: TextStyle(
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ],
        ),
        content: Text(content,
          style: TextStyle(
          color: Colors.white,
        ),
        ),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: Text('Close',
              style: TextStyle(
                color: Color(0xFF00FFCE),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
