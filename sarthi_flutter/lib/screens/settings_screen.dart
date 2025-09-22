import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Center(
        child: Text(
          'Settings Page Coming Soon!',
          style: TextStyle(fontSize: 24, color: Colors.white.withOpacity(0.8)),
        ),
      ),
    );
  }
}
