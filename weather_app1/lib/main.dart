import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';

import 'views/welcome_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: FirebaseOptions(
      apiKey: "AIzaSyDjf-BGdj_Dq7mQATmk1fubUbpj5C05LEQ",
      appId: "1:716696653768:android:35506c04f092d785f17afd",
      messagingSenderId: "716696653768",
      projectId: "weather-app-login-f0745",
    ),
  );
  runApp(MyApp());
}


class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'API Viewer App',
      home: WelcomePage(),
    );
  }
}
