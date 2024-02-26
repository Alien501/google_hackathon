class Weather {
  final String endpoint;
  final String method;
  final String description;

  Weather({
    required this.endpoint,
    required this.method,
    required this.description,
  });

  factory Weather.fromJson(Map<String, dynamic> json) {
    return Weather(
      endpoint: json['Endpoint'],
      method: json['method'],
      description: json['description'],
    );
  }
}
