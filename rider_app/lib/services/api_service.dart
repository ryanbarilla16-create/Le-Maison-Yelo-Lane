import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/order_model.dart';

class ApiService {
  static Future<Map<String, List<OrderModel>>> fetchDeliveries(int riderId) async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/rider/deliveries?rider_id=$riderId'),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return {
        'available': (data['available'] as List)
            .map((o) => OrderModel.fromJson(o))
            .toList(),
        'active': (data['active'] as List)
            .map((o) => OrderModel.fromJson(o))
            .toList(),
        'completed': (data['completed'] as List)
            .map((o) => OrderModel.fromJson(o))
            .toList(),
      };
    } else {
      throw Exception('Failed to load deliveries');
    }
  }

  static Future<bool> acceptOrder(int orderId, int riderId) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/rider/accept/$orderId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'rider_id': riderId}),
    );
    return response.statusCode == 200;
  }

  static Future<bool> updateStatus(int orderId, int riderId, String status, {double? amountTendered, String? proofUrl}) async {
    final Map<String, dynamic> body = {
      'delivery_status': status,
      'rider_id': riderId,
    };
    if (amountTendered != null) body['amount_tendered'] = amountTendered;
    if (proofUrl != null) body['proof_of_delivery_url'] = proofUrl;

    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/rider/update/$orderId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(body),
    );
    return response.statusCode == 200;
  }

  static Future<Map<String, dynamic>> fetchSummary(int riderId) async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/rider/summary/$riderId'),
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load summary');
    }
  }

  static Future<void> updateLocation(int riderId, double lat, double lng) async {
    await http.post(
      Uri.parse('${AppConfig.baseUrl}/rider/location'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'rider_id': riderId,
        'latitude': lat,
        'longitude': lng,
      }),
    );
  }
}
