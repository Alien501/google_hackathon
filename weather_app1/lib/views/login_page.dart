import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'report_preview_page.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleSignIn _googleSignIn = GoogleSignIn();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xff7461e5),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to our\n Environmental Reporting App!',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () async {
                try {
                  final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
                  final GoogleSignInAuthentication? googleAuth = await googleUser?.authentication;
                  final AuthCredential credential = GoogleAuthProvider.credential(
                    accessToken: googleAuth?.accessToken,
                    idToken: googleAuth?.idToken,
                  );
                  final UserCredential userCredential = await _auth.signInWithCredential(credential);
                  final User? user = userCredential.user;

                  print('Signed in as ${user?.displayName}');
                  if (user != null) {
                    Navigator.push(context,MaterialPageRoute(builder: (context) => ReportPreviewPage(user: user)),);
                  }
                } catch (e) {
                  print(e);
                }
              },
              icon: Image.asset(
                'assets/google_icon.png',
                width: 24,
                height: 24,
              ),
              label: Text('Sign in with Google'),
              style: ElevatedButton.styleFrom(
                primary: Colors.white,
                onPrimary: Color(0xff7461e5),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }
}