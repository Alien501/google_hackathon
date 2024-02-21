import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService(this.baseUrl);

  Future<List<Map<String, dynamic>>> fetchData(String endpoint) async {
    final response = await http.get(Uri.parse('$baseUrl$endpoint'));

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      if (responseData is List) {
        return List<Map<String, dynamic>>.from(responseData);
      } else {
        throw Exception('Invalid response data format');
      }
    } else {
      throw Exception('Failed to load data. Status code: ${response.statusCode}');
    }
  }
}