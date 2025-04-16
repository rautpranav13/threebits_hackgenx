import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'flutter_flow/flutter_flow_util.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {
    prefs = await SharedPreferences.getInstance();
    _safeInit(() {
      _energyConsumed = prefs.getDouble('ff_energyConsumed') ?? _energyConsumed;
    });
  }

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  late SharedPreferences prefs;

  double _energyConsumed = 0.0;
  double get energyConsumed => _energyConsumed;
  set energyConsumed(double value) {
    _energyConsumed = value;
    prefs.setDouble('ff_energyConsumed', value);
  }

  double _temperature = 0.0;
  double get temperature => _temperature;
  set temperature(double value) {
    _temperature = value;
  }

  double _humididty = 0.0;
  double get humididty => _humididty;
  set humididty(double value) {
    _humididty = value;
  }

  bool _motionDetected = false;
  bool get motionDetected => _motionDetected;
  set motionDetected(bool value) {
    _motionDetected = value;
  }

  double _ambientLight = 0.0;
  double get ambientLight => _ambientLight;
  set ambientLight(double value) {
    _ambientLight = value;
  }
}

void _safeInit(Function() initializeField) {
  try {
    initializeField();
  } catch (_) {}
}

Future _safeInitAsync(Function() initializeField) async {
  try {
    await initializeField();
  } catch (_) {}
}
