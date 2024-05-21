import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:math';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ICU Monitoring',
      debugShowCheckedModeBanner: false,
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int simulatedHeartRate = 70;
  Timer? timer;
  TextEditingController patientIdController = TextEditingController();
  TextEditingController patientNameController = TextEditingController();
  bool isSendingData = false;
  int steps = 0;

  @override
  void initState() {
    super.initState();
  }

  void startSendingHeartRate() async {
  timer?.cancel(); // Cancel any ongoing timer
  timer = Timer.periodic(Duration(seconds: 2), (timer) async {
    setState(() {
      isSendingData = true;
    });
      // Regular steps
      simulatedHeartRate = 60 + Random().nextInt(40); // Simulate heart rate between 60 and 100
      await sendHeartRate(simulatedHeartRate);
      print('Sent heart rate: $simulatedHeartRate');


    setState(() {
      isSendingData = false;
    });
  });
}

  void stopSendingHeartRate() {
    timer?.cancel();
    setState(() {
      isSendingData = false;
    });
  }

  Future<http.Response> sendHeartRate(int heartRate) async {
    final url = Uri.parse('https://test-bjyo.onrender.com/receive_data/${patientIdController.text}/$heartRate');
    final response = await http.post(url);
    if(response.statusCode == 200) {
      print('Sent heart rate: $heartRate');
    } else {
      print('Failed to send heart rate. Error: ${response.statusCode}');
    }
    return response;
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ICU Monitoring', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 26),),
        centerTitle: true,
        backgroundColor: Colors.black,
      ),
      body: Center(
        child: ListView(
          padding: EdgeInsets.all(16.0),
          children: <Widget>[
            SizedBox(height: 30.0),
            TextFormField(
              controller: patientIdController,
              decoration: InputDecoration(
                labelText: "Patient ID",
                hintText: 'Enter Patient ID',
                hintStyle: TextStyle(color: Color(0xFF787878)),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                filled: true,
                fillColor: Color.fromARGB(255, 250, 242, 242),
              ),
            ),
            
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                if (!isSendingData) {
                  setState(() {
                    isSendingData = true;
                  });
                  startSendingHeartRate();
                } else {
                  stopSendingHeartRate();
                }
              },
              child: Text(isSendingData ? 'Stop Sending' : 'Start Sending',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20.0,
                ),
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color.fromARGB(255, 255, 181, 97),
                foregroundColor: Color.fromARGB(216, 255, 158, 47),
              ),
            ),
            Row(
              children: [
                Text("Heart Rate: ", style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold)),
                isSendingData? Text('$simulatedHeartRate', style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),) : Container(),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
