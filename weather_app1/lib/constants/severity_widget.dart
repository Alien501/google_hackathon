import 'package:flutter/material.dart';

class SeverityWidget extends StatelessWidget {
  final String severity;
  final String label;

  const SeverityWidget({Key? key, required this.severity, required this.label})
      : super(key: key);

  Color getColor(String severity) {
    switch (severity) {
      case 'high':
        return Color(0xFF0000);
      case 'normal':
        return Color(0x00A3FF);
      case 'low':
        return Color(0x00FF0A);
      default:
        return Colors.black;
    }
  }

  TextStyle getTextStyle(String severity) {
    Color color = getColor(severity);
    return TextStyle(
      color: color,
      fontSize: 16.0,
      fontWeight: FontWeight.bold,
      shadows: [
        Shadow(
          blurRadius: 2.0,
          color: color,
          offset: Offset(1.0, 1.0),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    Color color = getColor(severity).withOpacity(1);
    String severityText = severity.toUpperCase();
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Container(
          height: MediaQuery
              .of(context)
              .size
              .width / 2.3,
          width: MediaQuery
              .of(context)
              .size
              .width / 2.3,
          decoration: BoxDecoration(
            color: color.withOpacity(0.3),
            borderRadius: BorderRadius.circular(10.0),
            border: Border.all(color: color, width: 2),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Center(
                child: Text(
                  label.toLowerCase() != "ozone"
                      ? "Presence of $label".toUpperCase()
                      : "Pollutants in $label".toUpperCase(),
                  style: TextStyle(
                    color: Colors.grey.shade300,
                    fontSize: 15.0,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),

              ),
              SizedBox(height: 16.0),
              Center(
                child: Text(
                  "Severity",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              SizedBox(height: 8.0),
              Center(
                child: Text(
                  severityText,
                  style: TextStyle(
                    color: color,
                    fontSize: 16.0,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}