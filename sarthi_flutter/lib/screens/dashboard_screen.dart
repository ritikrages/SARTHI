import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SARTHI Dashboard'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Center(
        child: Text(
          'Futuristic Dashboard Coming Soon!',
          style: TextStyle(fontSize: 24, color: Colors.white.withOpacity(0.8)),
        ),
      ),
    );
  }
}
