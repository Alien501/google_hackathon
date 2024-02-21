import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'login_page.dart';

class WelcomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Color(0xff7461e5),
        body: Center(
          child: Container(
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                SizedBox(height: 20,),
                Container(
                  // padding: EdgeInsets.fromLTRB(37, 16.58, 43, 8),
                  margin: EdgeInsets.fromLTRB(10, 10, 10, 0),
                  height: MediaQuery.of(context).size.height / 2.5,
                  width: MediaQuery.of(context).size.width,
                   child: Image.asset("assets/World.png",
                    fit: BoxFit.cover,
                    ),
                ),
                SizedBox(height: 50,),
                Container(
                  // padding: EdgeInsets.fromLTRB(37, 16.58, 43, 8),
                  margin: EdgeInsets.fromLTRB(10, 10, 10, 22),
                  padding: EdgeInsets.fromLTRB(50, 40, 50, 30),
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Color(0xffffffff),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Container(
                        margin: EdgeInsets.fromLTRB(6, 0, 0, 5),
                        child: Text(
                          'Welcome to',
                          textAlign: TextAlign.center,
                          style: GoogleFonts.montserrat(
                            fontSize: 25,
                            fontWeight: FontWeight.w400,
                            height: 0.2175,
                            color: Color(0xff000000),
                          ),
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.fromLTRB(6, 0, 0, 26),
                        child: RichText(
                          textAlign: TextAlign.center,
                          text: TextSpan(
                            style: GoogleFonts.inter(
                              fontSize: 35,
                              fontWeight: FontWeight.w400,
                              height: 0.2,
                              color: Color(0xff6151c3),
                            ),
                            children: [
                              TextSpan(
                                text: 'TerraSense',
                                style: GoogleFonts.montserrat(
                                  fontSize: 35,
                                  fontWeight: FontWeight.w700,
                                  height: 1.2,
                                  color: Color(0xff6151c3),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.fromLTRB(0, 0, 0, 40),
                        constraints: BoxConstraints(
                          // maxWidth: 286,
                        ),
                        child: Text(
                          'Explore global map of wind, weather, and ocean conditions',
                          textAlign: TextAlign.center,
                          style: GoogleFonts.montserrat(
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            height: 1.8160332574,
                            color: Color(0xff080713),
                          ),
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.fromLTRB(11, 0, 11, 20),
                        child: TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/page2');
                          },
                          style: TextButton.styleFrom(
                            padding: EdgeInsets.zero,
                          ),
                          child: Container(
                            width: double.infinity,
                            height: 60,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(30),
                            ),
                            child: ElevatedButton(
                              onPressed: () {
                                print("get started");
                                Navigator.push(context,MaterialPageRoute(builder: (context) => LoginPage(),),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                padding: EdgeInsets.zero,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(30),
                                ),
                                backgroundColor: Color(0xff6151c3),
                              ),
                              child: Container(
                                width: double.infinity,
                                height: double.infinity,
                                child: Center(
                                  child: Text(
                                    'Get started',
                                    textAlign: TextAlign.center,
                                    style: GoogleFonts.montserrat(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w500,
                                      height: 1.2175,
                                      color: Color(0xffffffff),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                      Container(
                        margin: EdgeInsets.fromLTRB(0, 0, 1, 0),
                        child: RichText(
                          textAlign: TextAlign.center,
                          text: TextSpan(
                            style: GoogleFonts.anekDevanagari(
                              fontSize: 14,
                              fontWeight: FontWeight.w400,
                              height: 1.171875,
                              color: Color(0xff6b6a71),
                            ),
                            children: [
                              TextSpan(
                                text: 'Already have an account ?',
                                style: GoogleFonts.montserrat(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  height: 1.2175,
                                  color: Color(0xff393942),
                                ),
                              ),
                              TextSpan(
                                text: ' Log in',
                                style: GoogleFonts.montserrat(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  height: 1.2175,
                                  color: Color(0xff6151c3),
                                ),
                                recognizer: TapGestureRecognizer()
                                  ..onTap = () {
                                    Navigator.pushNamed(context, '/login');
                                  },
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

const double fem = 1.0;
const double ffem = 1.0;
